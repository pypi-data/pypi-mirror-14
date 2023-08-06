# -*- coding: utf-8 -*-
import logging
import math
import threading
import time

from datetime import datetime

import ephem
import pytz

from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.orbital import pinpoint


logger = logging.getLogger('satnogsclient')


class Worker:
    """Class to facilitate as a worker for rotctl/rigctl."""

    # loop flag
    _stay_alive = False

    # end when this timestamp is reached
    _observation_end = None

    # frequency of original signal
    _frequency = None

    observer_dict = {}
    satellite_dict = {}

    def __init__(self, ip, port, time_to_stop=None, frequency=None, sleep_time=1):
        """Initialize worker class."""
        self._IP = ip
        self._PORT = port
        self._SLEEP_TIME = sleep_time
        if frequency:
            self._frequency = frequency
        if time_to_stop:
            self._observation_end = time_to_stop

    @property
    def is_alive(self):
        """Returns if tracking loop is alive or not."""
        return self._stay_alive

    @is_alive.setter
    def is_alive(self, value):
        """Sets value if tracking loop is alive or not."""
        self._stay_alive = value

    def trackobject(self, observer_dict, satellite_dict):
        """
        Sets tracking object.
        Can also be called while tracking to manipulate observation.
        """
        self.observer_dict = observer_dict
        self.satellite_dict = satellite_dict

    def trackstart(self):
        """
        Starts the thread that communicates tracking info to remote socket.
        Stops by calling trackstop()
        """
        self.is_alive = True
        logger.info('Tracking initiated')
        if not all([self.observer_dict, self.satellite_dict]):
            raise ValueError('Satellite or observer dictionary not defined.')

        self.t = threading.Thread(target=self._communicate_tracking_info)
        self.t.daemon = True
        self.t.start()

        return self.is_alive

    def send_to_socket(self):
        # Needs to be implemented in freq/track workers implicitly
        raise NotImplementedError

    def _communicate_tracking_info(self):
        """
        Runs as a daemon thread, communicating tracking info to remote socket.
        Uses observer and satellite objects set by trackobject().
        Will exit when observation_end timestamp is reached.
        """
        sock = Commsocket(self._IP, self._PORT)
        sock.connect()

        # track satellite
        while self.is_alive:

            # check if we need to exit
            self.check_observation_end_reached()

            p = pinpoint(self.observer_dict, self.satellite_dict)
            if p['ok']:
                self.send_to_socket(p, sock)
                time.sleep(self._SLEEP_TIME)

        sock.disconnect()

    def trackstop(self):
        """
        Sets object flag to false and stops the tracking thread.
        """
        logger.info('Tracking stopped.')
        self.is_alive = False

    def check_observation_end_reached(self):
        if datetime.now(pytz.utc) > self._observation_end:
            self.trackstop()


class WorkerTrack(Worker):
    def send_to_socket(self, p, sock):
        # Read az/alt and convert to radians
        az = p['az'].conjugate() * 180 / math.pi
        alt = p['alt'].conjugate() * 180 / math.pi

        msg = 'P {0} {1}\n'.format(az, alt)
        logger.debug('Rotctld msg: {0}'.format(msg))
        sock.send(msg)


class WorkerFreq(Worker):
    def send_to_socket(self, p, sock):
        doppler_calc_freq = self._frequency * (1 - (p['rng_vlct'] / ephem.c))
        msg = 'F {0}\n'.format(doppler_calc_freq)
        logger.debug('Initial frequency: {0}'.format(self._frequency))
        logger.debug('Rigctld msg: {0}'.format(msg))
        sock.send(msg)
