import sys
import os
import importlib
import logging

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from utils.bot_instance import client, run_client

logging.getLogger("httpx").setLevel(logging.WARNING)

for component in os.listdir(os.path.join(os.path.dirname(__file__), "components/events")):
    if component.endswith(".py") and not component.startswith("_"):
        importlib.import_module(f"components.events.{component[:-3]}")
        print(f"Loaded {component[:-3]}")
    
run_client()