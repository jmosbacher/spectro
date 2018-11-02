import signal
import asyncio
from asyncio import sleep, Queue
from concurrent.futures import ThreadPoolExecutor
#from curio import Queue
from datetime import datetime
import json
import logging

log = logging.getLogger(__name__) # Log under current position in hierarchy

class InstrumentServer:
    def __init__(self, instrument):
        self.inst = instrument
        self.requests = Queue()

    async def execute_requests(self):
        while True:
            try:
                res_q, name, req = await self.requests.get()
                if req is None:
                    log.info('Shutting down request excuter.')
                    break
                else:
                    try:
                        res = getattr(self.inst, name)(**req)
                    except:
                        log.info(f'Requested service {name} not available, ignored.')
                        continue
                    if res:
                        await res_q.put((name,res))

            except:
                log.info(f'Exception executing request {name}')