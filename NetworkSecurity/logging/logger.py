import logging 
import os
import sys
import datetime as datetime

LOG_FILE= f"{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print(f"ROOT_DIR: {ROOT_DIR}")

log_path= os.path.join(os.getcwd(),'logs-folder')
os.makedirs(log_path,exist_ok=True)

Log_file_path = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename= Log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

if __name__ == "__main__":
   logging.info("✅ Logging system initialized successfully!")