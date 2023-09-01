import os


DEPLOY_SH_PATH = os.getenv("DEPLOY_SH_PATH")

TEST_SH_PATH = os.getenv("TEST_SH_PATH")

LOG_PATH = os.getenv("LOG_PATH")

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")

RUN_TEST_SH_PATH = os.getenv("RUN_TEST_SH_PATH")

# from pydantic import BaseSettings

# class Setting(BaseSettings):
#     deploy_sh_path: str
#     test_sh_path: str
#     log_path: str
#     mail_host: str
#     mail_user: str
#     mail_pass: str
#     run_test_sh_path: str
    

# @lru_cache()
# def get_setting():
#     return Setting()
