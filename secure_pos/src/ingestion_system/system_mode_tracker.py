import threading

from ingestion_system.configuration import Configuration


class SystemModeTracker:
    __lock = threading.RLock()
    __session_num = 0
    __session_register = {}
    
    def __init__(self, conf: Configuration):
        self.__development_mode = conf.is_development_mode
        self.__execution_window_length = conf.execution_window_length
        self.__monitoring_window_length = conf.monitoring_window_length
    
    def register_record_arrival(self, json_records: dict) -> None:
        if self.__development_mode:
            return
        session_id = json_records['session_id']
        # Add session to register if it does not exist
        with self.__lock:
            if session_id not in self.__session_register:
                # Register session arrival
                self.__session_register[session_id] = self.__session_num
                self.__session_num += 1
    
    def is_session_in_monitoring_window(self, session_id: str) -> bool:
        # Check if the system is in development mode
        if self.__development_mode:
            return False
        
        with self.__lock:
            # Check if session is registered
            if session_id not in self.__session_register:
                raise ValueError("Session has not been registered")
            # Check if session is inside monitoring window
            session_num = self.__session_register[session_id]
            return (session_num % (self.__execution_window_length + self.__monitoring_window_length)) \
                >= self.__execution_window_length
    
    def is_label_required(self, session_id: str) -> bool:
        with self.__lock:
            return self.__development_mode or \
                self.is_session_in_monitoring_window(session_id)
