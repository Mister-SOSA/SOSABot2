from kick import Client, Credentials
from utils.totp_handler import gen_otp
import os 

KICK_USERNAME = os.environ.get("KICK_BOT_USERNAME")
KICK_PASSWORD = os.environ.get("KICK_BOT_PASSWORD")

client = Client()

credentials = Credentials(
    username=KICK_USERNAME,
    password=KICK_PASSWORD,
    one_time_password=gen_otp()
)

def run_client():
    client.run(credentials)