from flask import Flask, request

from tg_bot.core import Roykesistant
from utils.config import get_config
from utils.SecurityGuard import SecurityGuard

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/send", methods=["POST"])
def send():
    base_64_iv = request.form.get("iv")
    base64_ciphered_meesage = request.form.get("encrypted_message")
    key = get_config()["key"]

    return_msg = {"success": False, "msg": ""}

    with SecurityGuard() as security_guard:
        result = security_guard.authentication(base_64_iv, base64_ciphered_meesage, key)

        if not result["success"]:
            return_msg["msg"] = result["msg"]
            return return_msg

        try:
            tg_bot.send_message(result["data"])
        except:
            return_msg["msg"] = "can't send message"
            return return_msg

    return_msg["success"] = True
    return return_msg


if __name__ == "__main__":
    tg_bot = Roykesistant()

    try:
        app.run(host="0.0.0.0", port=11539)
    finally:
        tg_bot.shutdown()
