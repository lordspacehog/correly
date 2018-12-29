import asyncio
from contextlib import suppress
import functools
import logging
from queue import Queue
import signal
from threading import Event
from vyper import v
from .config import init_config
from .models import process_readings
from .mqtt import IoTController

logging.basicConfig(level=logging.INFO)

ExitEvent = Event()

async def shutdown(sig, loop):
    logging.info('caught %s', sig.name)
    tasks = [task for task in asyncio.Task.all_tasks() if task is not
             asyncio.tasks.Task.current_task()]
    list(map(lambda task: task.cancel(), tasks))
    ExitEvent.set()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def main():
    init_config()

    mqtt_endpoint = v.get_string('mqtt_endpoint')
    print(mqtt_endpoint)
    db_uri = v.get_string('database_uri')
    msg_queue = Queue()

    controller = IoTController(mqtt_endpoint, msg_queue)
    logging.info('listening for events...')
    main_loop = asyncio.get_event_loop()

    main_loop.add_signal_handler(
        signal.SIGINT,
        functools.partial(
            asyncio.ensure_future,
            shutdown(signal.SIGINT, main_loop)
        )
    )

    main_loop.add_signal_handler(
        signal.SIGTERM,
        functools.partial(
            asyncio.ensure_future,
            shutdown(signal.SIGTERM, main_loop)
        )
    )

    asyncio.ensure_future(controller.listen_for_events_coro(), loop=main_loop)
    asyncio.ensure_future(main_loop.run_in_executor(None, process_readings, db_uri, msg_queue, ExitEvent),
                          loop=main_loop)

    try:
        main_loop.run_forever()
    finally:
        main_loop.close()

if __name__ == '__main__':
    main()
