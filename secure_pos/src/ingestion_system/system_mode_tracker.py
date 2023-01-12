import threading

from ingestion_system.configuration import Configuration


class SystemModeTracker:
    """
    Class responsible to track if the toolchain is
    in development, execution or monitoring mode.
    All the methods are thread-safe.
    """
    __lock = threading.RLock()
    __session_num = 0
    __session_register = {}
    
    def __init__(self, conf: Configuration):
        self.__development_mode = conf.is_development_mode
        self.__execution_window_length = conf.execution_window_length
        self.__monitoring_window_length = conf.monitoring_window_length
    
    def __get_phase_window_period(self) -> int:
        """
        Get the period of the alternation between
        the execution and the monitoring phase.
        :return: the period
        """
        return self.__execution_window_length + self.__monitoring_window_length
    
    def register_record_arrival(self, session_id: str) -> None:
        """
        Register the arrival of a record. If the record's session is not registered yet,
        the counter of received sessions is assigned to the current session and then increased.
        :param session_id: id of the session
        """
        # The counter is required only after the development
        if self.__development_mode:
            return
        # Add session to register if it does not exist
        with self.__lock:
            if session_id not in self.__session_register:
                # Register session arrival
                self.__session_register[session_id] = self.__session_num
                self.__session_num = (self.__session_num + 1) % self.__get_phase_window_period()
    
    def is_session_in_monitoring_window(self, session_id: str) -> bool:
        """
        Check if a given session is inside the monitoring window.
        :param session_id: id of the session
        :return: True if the session is in monitoring, False otherwise.
        """
        # Check if the system is in development mode
        if self.__development_mode:
            return False
        
        with self.__lock:
            # Check if session is registered
            if session_id not in self.__session_register:
                raise ValueError(f"Session {session_id} has not been registered")
            # Check if session is inside monitoring window
            return self.__session_register[session_id] >= self.__execution_window_length
    
    def is_label_required(self, session_id: str) -> bool:
        """
        Check if a label is necessary for the current session.
        :param session_id: id of the session
        :return: True if a label is required, False otherwise
        """
        with self.__lock:
            return self.__development_mode or \
                self.is_session_in_monitoring_window(session_id)
    
    def unregister_session(self, session_id: str) -> None:
        """
        Remove a session from the dict.
        :param session_id: id of the session.
        """
        if session_id in self.__session_register:
            self.__session_register.pop(session_id)
