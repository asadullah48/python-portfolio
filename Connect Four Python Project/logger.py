import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        filename=f'logs/connect_four_{datetime.now():%Y%m%d}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console_handler)