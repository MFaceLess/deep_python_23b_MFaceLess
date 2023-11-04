import unittest
from unittest.mock import patch
import asyncio
from aioresponses import aioresponses
import fetcher


class TestFetcher(unittest.TestCase):
    @patch('sys.argv', ['test_fetcher.py', '5', 'example.txt'])
    def test_parse_args_valid_input(self):
        args = fetcher.parse_args()
        self.assertEqual(args.num_requests, 5)
        self.assertEqual(args.url_file, 'example.txt')

    @patch('sys.argv', ['test_fetcher.py', '0', 'example.txt'])
    def test_parse_args_invalid_num_requests(self):
        with self.assertRaises(ValueError) as err:
            fetcher.parse_args()
        self.assertEqual("Value <= then 0", str(err.exception))


class TestAsync(unittest.TestCase):
    def test_fetch_url(self):
        url = "test_url"
        expected_status = 200

        with aioresponses() as mock_session:
            mock_session.get(url, status=expected_status)
            result = asyncio.run(fetcher.fetch_url(url, asyncio.Semaphore(1)))

        self.assertEqual(result, (url, expected_status))


class TestFetchWorker(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    async def fetch_worker_single_url(self, url, expected_status):
        with aioresponses() as mock_session:
            mock_session.get(url, status=expected_status)

            que = asyncio.Queue()
            sem = asyncio.Semaphore(1)
            que.put_nowait(url)

            result = await fetcher.fetch_worker(que, sem)

            self.assertEqual(result, (url, expected_status))

    def test_fetch_worker_single_url(self):
        url = "test_url"
        expected_status = 200

        self.loop.run_until_complete(
            self.fetch_worker_single_url(
                url, expected_status))

    async def fetch_worker_multiple_urls(self, urls, expected_status):
        with aioresponses() as mock_session:
            for url in urls:
                mock_session.get(url, status=expected_status)

            que = asyncio.Queue()
            sem = asyncio.Semaphore(len(urls))
            for url in urls:
                que.put_nowait(url)

            results = await \
                asyncio.gather(*[fetcher.fetch_worker(que, sem) for _ in urls])

            for url, status in results:
                self.assertEqual(status, expected_status)

    def test_fetch_worker_multiple_urls(self):
        urls = ["test_url1", "test_url2"]
        expected_status = 200

        self.loop.run_until_complete(
            self.fetch_worker_multiple_urls(
                urls, expected_status))


class TestSem(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    async def fetch_worker_single_url(self, url, expected_status, event):
        with aioresponses() as mock_session:
            mock_session.get(url, status=expected_status)

            que = asyncio.Queue()
            sem = asyncio.Semaphore(1)
            que.put_nowait(url)

            result = await fetcher.fetch_worker(que, sem)
            event.set()

            return result

    async def fetch_worker_multiple_urls(self, urls, expected_status, event):
        with aioresponses() as mock_session:
            for url in urls:
                mock_session.get(url, status=expected_status)

            que = asyncio.Queue()
            sem = asyncio.Semaphore(len(urls))
            for url in urls:
                que.put_nowait(url)

            results = await \
                asyncio.gather(*[fetcher.fetch_worker(que, sem) for _ in urls])
            event.set()

            return results

    def test_fetch_worker_single_url(self):
        url = "test_url"
        expected_status = 200
        event = asyncio.Event()

        async def run_test():
            result = await \
                self.fetch_worker_single_url(url, expected_status, event)
            self.assertEqual(result, (url, expected_status))

        self.loop.run_until_complete(run_test())
        self.assertTrue(event.is_set())

    def test_fetch_worker_multiple_urls(self):
        urls = ["test_url1", "test_url2"]
        expected_status = 200
        event = asyncio.Event()

        async def run_test():
            results = await \
                self.fetch_worker_multiple_urls(urls, expected_status, event)
            for _, status in results:
                self.assertEqual(status, expected_status)

        self.loop.run_until_complete(run_test())
        self.assertTrue(event.is_set())


if __name__ == '__main__':
    unittest.main()
