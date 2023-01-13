import threading

from execution_system.execution_system_configuration import ExecutionSystemConfiguration


class SystemModeTracker:
    __lock = threading.RLock()
    __session_num = 0
    development_mode = True

    def __init__(self, conf: ExecutionSystemConfiguration):
        self.__execution_window_length = conf.execution_window_length
        self.__monitoring_window_length = conf.monitoring_window_length

    def is_session_in_monitoring_window(self) -> bool:
        with self.__lock:
            # Check if the system is in development mode
            if self.development_mode:
                return False
            # Check if session is inside monitoring window
            self.__session_num = (self.__session_num + 1) % \
                                 (self.__execution_window_length + self.__monitoring_window_length)
            return self.__session_num >= self.__execution_window_length
