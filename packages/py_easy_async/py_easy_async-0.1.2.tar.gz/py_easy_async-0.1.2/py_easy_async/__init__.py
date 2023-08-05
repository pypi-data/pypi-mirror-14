from .process import ThreadPool, AsyncProcess


pool = ThreadPool()


def async(handler, callback=None):
    async_process = AsyncProcess()
    async_process.set_process(handler)

    if callback is not None:
        async_process.set_callback(callback)

    async_process.start()
