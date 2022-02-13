import multiprocessing as mp
import logging
import queue


class LoggerProcess(mp.Process):

    def __init__(self, logging_config, logging_queue, kill_event):
        super().__init__()
        self.logger = logging.getLogger("ddoser_logger_process")
        self._kill_event = kill_event
        self._logging_queue = logging_queue
        self.init_logger(logging_config)

    @property
    def kill(self):
        return self._kill_event.is_set()

    def run(self):
        while not self.kill:
            if not self._logging_queue.empty():
                self.logger.handle(self._logging_queue.get())

    def join(self, timeout=None):
        while not self._logging_queue.empty():
            try:
                self.logger.handle(self._logging_queue.get(timeout=0.01))
            except queue.Empty:
                continue
        super().join(timeout)
