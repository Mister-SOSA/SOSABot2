from utils.bot_instance import run_client
import sys
import os
import importlib
import logging
import asyncio
from rich import print

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

for component in os.listdir(os.path.join(os.path.dirname(__file__), "components/events")):
    if component.endswith(".py") and not component.startswith("_"):
        importlib.import_module(f"components.events.{component[:-3]}")
        print(f"[magenta] >> Loaded Event: {component[:-3]}[/magenta]")


while True:
    try:
        run_client()

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

    except RuntimeError as e:
        print(f'[red]>> Runtime Error: {e}[/red]')
        print(f'[red]>> Restarting...[/red]')
        asyncio.sleep(1)
        continue
