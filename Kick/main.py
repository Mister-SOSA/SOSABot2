import sys
import os
import importlib
import logging
import asyncio

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from utils.bot_instance import run_client

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

for component in os.listdir(os.path.join(os.path.dirname(__file__), "components/events")):
    if component.endswith(".py") and not component.startswith("_"):
        importlib.import_module(f"components.events.{component[:-3]}")
        print(f"Loaded {component[:-3]}")


while True:
    try:    
        run_client()
        
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
        
    except TypeError as e:
        print(f'[red]>> TypeError: {e}[/red]')
        print(f'[red]>> Restarting...[/red]')
        asyncio.sleep(2)
        continue