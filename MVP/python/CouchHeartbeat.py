"""
 CouchDB heartbeat
 Check database and if not running, restart
 Restarting CouchDB does not always go clear, reboot is better
"""

import os
from LogUtil import Logger

class CouchHeartbeat(object):
    """Heartbeat object    """

    logger = None

    def __init__(self):
        """Standard constructor
        Get and hold a Python logger
        """
        self._logger = Logger('CouchHeartbeat', Logger.INFO, "/home/pi/MVP/logs/heartbeat.log")

    def check(self, port):
        """Ping the database
        Should return the welcome message
        Throws an exception if cannot make a connection to the database

        Args:
            port: port the database is communicating on
        Returns:
            None
        Raises:
            None
        """
        cmd = 'curl -X GET http://localhost:5984'
        ret = os.system(cmd)
        if ret == 0:
                self._logger.info('localhost Couch is Up')
        else:
            self._logger.error('Couch is Down')
            self.restart()

    def restart(self):
        """System restart (reboot)
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        cmd = 'sudo reboot'
        self.logger.warning('System restart: %s' % (cmd))
        os.system(cmd)

def test():
    """Standard test function

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    heartbeat = CouchHeartbeat()
    heartbeat.check('5984')

if __name__ == "__main__":
    test()

