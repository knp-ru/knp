import time

import yaml
import signal
from .attacker import Attacker
from .reporter import Reporter
import logging
import multiprocessing as mp


class AttackRunner:

    def __init__(self, config_file):
        self._kill_event, self._start_attack_event = mp.Event(), mp.Event()
        self._config = self.load_config(config_file)
        self._num_ps = self._config["threads"]
        self._logging_queue = mp.Queue()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.init_logger(self._config['logging'])
        self._config['logger'] = self.logger
        self._config['report_queue'] = mp.Queue()
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self._attackers = [Attacker(self._config, self._start_attack_event, self._kill_event) for _ in range(self._num_ps)]

    def exit_gracefully(self, signum, frame):
        self._kill_event.set()

    @staticmethod
    def load_config(config_file):
        with open(config_file) as yf:
            conf = yaml.full_load(yf)
        return conf

    def init_logger(self, logging_config):
        logging_level = logging_config.get("level", logging.INFO)
        log_name = logging_config.get("log_name", "ddoser")
        self.logger.setLevel(logging_level)
        sh = logging.StreamHandler()
        sh.setLevel(logging_level)
        fh = logging.FileHandler(f"output/{log_name}.log")
        fh.setLevel(logging_level)
        fmt = logging.Formatter('[%(asctime)s] {%(processName)s %(levelname)s}: %(message)s')
        sh.setFormatter(fmt)
        fh.setFormatter(fmt)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def gather_reports(self):
        report_queue = self._config['report_queue']
        all_reports = []
        while not report_queue.empty():
            all_reports.append(report_queue.get())
        final_report = Reporter(
            "runner",
            num_requests=sum(map(lambda r: r.num_requests, all_reports)),
            failed_requests=sum(map(lambda r: r.failed_requests, all_reports)),
            num_sessions=sum(map(lambda r: r.num_sessions, all_reports))
        )
        return final_report

    def run_attack(self):
        self.logger.info("""
██████╗░██████╗░░█████╗░░██████╗███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
██║░░██║██║░░██║██║░░██║╚█████╗░█████╗░░██████╔╝
██║░░██║██║░░██║██║░░██║░╚═══██╗██╔══╝░░██╔══██╗
██████╔╝██████╔╝╚█████╔╝██████╔╝███████╗██║░░██║
╚═════╝░╚═════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝
""")
        list(map(Attacker.start, self._attackers))
        self._start_attack_event.set()
        list(map(Attacker.join, self._attackers))
        final_report = self.gather_reports()
        self.logger.info(f"""Done running attack, some stats:
                        Total requests: {final_report.num_requests}
                        Total sessions: {final_report.num_sessions}
                        Total failed requests: {final_report.failed_requests}
                        """)
