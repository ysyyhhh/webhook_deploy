import logging
import os
import time
from loguru import logger
import sys

import webhook_deploy.config as config


def reconfig_log():
    # -----------------------log-----------------------------------------
    # LOG_DIR = os.path.join(os.getcwd(), 'log')
    if(config.LOG_PATH != None):
        LOG_DIR = config.LOG_PATH
        LOG_DIR = os.path.join(LOG_DIR, time.strftime("%Y-%m-%d")+'.log')
    else:
        LOG_DIR = os.path.join(os.getcwd(), 'log', time.strftime("%Y-%m-%d")+'.log')
       
    LOG_FORMAT = '<level>{level: <8}</level>  <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>'

    def format_record(record: dict) -> str:
        format_string = LOG_FORMAT
        if record["extra"].get("payload") is not None:
            record["extra"]["payload"] = pformat(
                record["extra"]["payload"], indent=4, compact=True, width=88
            )
            format_string += "\n<level>{extra[payload]}</level>"

        format_string += "{exception}\n"
        return format_string

    logger.configure(
            handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}])
    logger.add(LOG_DIR, encoding='utf-8', rotation="9:46")
    
    logger.debug('log is loaded')
    
    return logger

logger = reconfig_log()