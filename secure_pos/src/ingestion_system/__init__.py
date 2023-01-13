import logging

from ingestion_system.ingestion_system_controller import IngestionSystemController

if __name__ == "__main__":
    # Configure logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Start system
    system = IngestionSystemController()
    system.run()
