from utils.config import get_config
from utils.SecurityGuard import SecurityGuard

config = get_config()
security_guard = SecurityGuard()

iv, encypt_message = security_guard.encrypt_message(
    "xxx service is dead!", config["key"]
)
print(iv, encypt_message)
