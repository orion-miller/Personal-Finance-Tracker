import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys

def setup_logging():
    log_filename = f"app_{datetime.now():%Y%m%d_%H%M%S}.log"
    
    # Basic configuration
    logging.basicConfig(
        level=logging.DEBUG,  # or DEBUG during development
        format='%(asctime)s | %(levelname)-7s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            RotatingFileHandler(
                log_filename,
                maxBytes=10*1024*1024,      # 10MB
                backupCount=5,               # keep 5 old files
                encoding='utf-8'
            ),
            # Optional: also see logs in console during development
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Optional: get a named logger for your app
    logger = logging.getLogger("MyPySide6App")
    return logger

# ────────────────────────────────────────────────────────────────


# # You can still redirect print() if you want/need:
# class PrintLogger:
#     def write(self, text):
#         if text.strip():
#             logger.info(text.rstrip())
#     def flush(self):
#         pass

# sys.stdout = PrintLogger()    # uncomment if you want print() → log