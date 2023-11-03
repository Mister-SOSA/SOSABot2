import pytz
import datetime
from common.utils.configutil import fetch_convar

TIMEZONE = fetch_convar("TIMEZONE")

def get_timestamp():
    return datetime.datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
