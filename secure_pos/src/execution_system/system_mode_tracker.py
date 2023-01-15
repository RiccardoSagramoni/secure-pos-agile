import threading

from execution_system.execution_system_configuration import ExecutionSystemConfiguration


class SystemModeTracker:
    """
    Class responsible to track if the toolchain is in development, execution or monitoring mode.
    All the methods are thread-safe.
    """
    __lock = threading.RLock()
    __session_num = 0
    development_mode = True

    def __init__(self, conf: ExecutionSystemConfiguration):
        self.__execution_window_length = conf.execution_window_length
        self.__monitoring_window_length = conf.monitoring_window_length

    def is_session_in_monitoring_window(self) -> bool:
        """
        Check if a given session is inside the monitoring window.
        :return: True if the session is in monitoring, False otherwise.
        """
        with self.__lock:
            # Check if the system is in development mode
            if self.development_mode:
                return False
            # Check if session is inside monitoring window
            self.__session_num = (self.__session_num + 1) % \
                                 (self.__execution_window_length + self.__monitoring_window_length)
            return self.__session_num >= self.__execution_window_length
