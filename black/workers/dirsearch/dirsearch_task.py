import aiohttp
import asyncio
import async_timeout

from black.workers.common.async_task import AsyncTask


class DirsearchTask(AsyncTask):
    """ Instance of running dirsearch """

    def __init__(self, task_id, target, params, project_uuid):
        AsyncTask.__init__(self, task_id, 'dirsearch', target, params, project_uuid)

        self.cookies = params['program'][0].get('cookies', None)
        self.headers = params['program'][0].get('headers', None)
        self.session = aiohttp.ClientSession(cookies=self.cookies,
                                             headers=self.headers)

        self.urls_queue = asyncio.Queue()

    async def fill_queue(self, url):
        list_of_files = ["1", "2", "3"]

        for each_file in list_of_files:
            await self.urls_queue.put(url + each_file)

    async def perform_request(self, url):
        resp = await self.session.get(url)

        status_code = resp.status
        length = resp.content_length or len(await resp.text())

        resp.close()

        return (status_code, length)

    def save_callback(self, future):
        if not future.exception():
            url = future.url
            result = future.result()
            status_code = result[0]
            content_length = result[1]
            print("*"*20)
            print(url)
            print(status_code)
            print(content_length)

    async def start(self):
        """ Launch the task and readers of stdout, stderr """
        await self.fill_queue(self.target)

        finished = False
        while not finished:
            futures = []

            # This is done for possible recursive work
            while not self.urls_queue.empty():
                url = await self.urls_queue.get()
                request = asyncio.ensure_future(self.perform_request(url))
                request.url = url
                request.add_done_callback(self.save_callback)

                futures.append(request)

            await asyncio.wait(futures)
            # Some data could appear in the queue (the recursive one)
            if self.urls_queue.empty():
                finished = True

        self.session.close()

    def send_notification(self, command):
        """ Sends 'command' notification to the current process. """
        # if command == 'pause':
        #     self.proc.send_signal(signal.SIGSTOP.value)  # SIGSTOP
        # elif command == 'stop':
        #     self.proc.terminate()  # SIGTERM
        # elif command == 'unpause':
        #     self.proc.send_signal(signal.SIGCONT.value)  # SIGCONT

    async def wait_for_exit(self):
        """ Check if the process exited. If so,
        save stdout, stderr, exit_code and update the status. """
