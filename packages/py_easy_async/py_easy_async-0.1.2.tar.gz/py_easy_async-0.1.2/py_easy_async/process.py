import threading
import queue
import uuid


class AsyncProcess(threading.Thread):

    _process = None
    _callback = None

    def set_process(self, process):
        if not callable(process):
            pass  # @todo raise error

        self._process = process

    def set_callback(self, callback):
        if not callable(callback):
            pass  # @todo raise error

        self._callback = callback

    def run(self):
        results = self._process()

        if callable(self._callback):
            self._callback(results)


class Thread(threading.Thread):

    _messageQueue = None
    _message_handler = None

    _stopped = False

    _debug = False

    def _debug_msg(self, msg):
        if self._debug:
            print(msg)

    def set_debug(self, debug):
        self._debug = debug

    def init_communications(self):
        self._messageQueue = queue.Queue()

    def message(self, message):
        self._messageQueue.put(message)

    def set_handler(self, handler):
        if not callable(handler):
            pass  # @todo raise error

        self._message_handler = handler

    def stop(self):
        self._stopped = True

    def processor(self, message):
        self._debug_msg("%s: processing message" % self._name)

        self._message_handler(message)

    def run(self):
        self._debug_msg("%s: starting..." % self._name)

        while not self._stopped:
            try:
                data = self._messageQueue.get(True, 5)
                self.processor(data)
            except queue.Empty:
                continue

        self._debug_msg("%s: exiting..." % self._name)


class ThreadPool:

    _threads = {}

    def debug_thread(self, identifier):
        self._threads[identifier].set_debug(True)

    def stop_debug_thread(self, identifier):
        self._threads[identifier].set_debug(False)

    def get_thread(self, identifier):
        return self._threads[identifier]

    def stop_thread(self, identifier):
        self._threads[identifier].stop()

    def message(self, identifier, message):
        self._threads[identifier].message(message)

    def run_thread(self, message_handler, name=None, group=None):
        thread_identifier = str(uuid.uuid4())

        if name is None:
            name = thread_identifier

        thread = Thread(name=name, group=group)
        thread.init_communications()
        thread.set_handler(message_handler)

        thread.start()

        self._threads[thread_identifier] = thread

        return thread_identifier
