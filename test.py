from utils.config import get_config
from utils.security_guard import SecurityGuard
from utils.database import  get_connection
from datetime import datetime
import time

# config = get_config()
# security_guard = SecurityGuard()

# iv, encypt_message = security_guard.encrypt_message(
#     "xxx service is dead!", config["key"]
# )
# print(iv, encypt_message)

if __name__ == "__main__":
    config = get_config()
    security_guard = SecurityGuard()
    iv, encypt_message = security_guard.encrypt_message(
    "xxx service is dead!", config["key"]
    )
    print(security_guard.authentication(iv, encypt_message, config["key"]))
    print(time.time())
    print(iv, encypt_message)
    # insert_data()
    # get_connection()