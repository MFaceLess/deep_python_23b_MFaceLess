import unittest
import threading
import socket
import time
import server


class TestServerDown(unittest.TestCase):
    def test_not_correct_values1(self):
        with self.assertRaises(ValueError) as err:
            _ = server.MasterServer('127.0.0.1', 8888, -1, 5)

        self.assertEqual("Values must be above zero", str(err.exception))

    def test_not_correct_values2(self):
        with self.assertRaises(ValueError) as err:
            _ = server.MasterServer('127.0.0.1', 8888, 5, 0)

        self.assertEqual("Values must be above zero", str(err.exception))


class TestServer(unittest.TestCase):
    def setUp(self):
        server.SERVER_ON = True
        self.host = '127.0.0.1'
        self.port = 8888
        self.num_workers = 10
        self.top_k = 5
        self.server = server.MasterServer(
            self.host, self.port, self.num_workers, self.top_k)

    def tearDown(self):
        self.server.executor.shutdown()

    def test_multiple_clients(self):
        server_thread = threading.Thread(target=self.server.start)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(1)

        num_clients = 5
        clients = []
        for _ in range(num_clients):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            clients.append(client)

        time.sleep(1)

        for client in clients:
            self.assertTrue(client.fileno() != -1)

        for client in clients:
            client.close()

        server.SERVER_ON = False
        server_thread.join()

    def test_worker_counter1(self):
        server_thread = threading.Thread(target=self.server.start)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(1)

        num_clients = 5
        clients = []
        for _ in range(num_clients):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            clients.append(client)

        time.sleep(1)

        actual_worker_count = threading.active_count() - 2
        self.assertEqual(
            actual_worker_count, min(
                self.num_workers, num_clients))

        for client in clients:
            client.close()

        server.SERVER_ON = False
        server_thread.join()

    def test_worker_counter2(self):
        server_thread = threading.Thread(target=self.server.start)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(1)

        num_clients = 40
        clients = []
        for _ in range(num_clients):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            clients.append(client)

        time.sleep(1)

        actual_worker_count = threading.active_count() - 2
        self.assertEqual(
            actual_worker_count, min(
                self.num_workers, num_clients))

        for client in clients:
            client.close()

        server.SERVER_ON = False
        server_thread.join()


# class TestWorker(unittest.TestCase):
#     def setUp(self):
#         server.SERVER_ON = True
#         self.host = '127.0.0.1'
#         self.port = 8085
#         self.num_workers = 5
#         self.top_k = 2
#         self.server = server.MasterServer\
# (self.host, self.port, self.num_workers, self.top_k)

#         self.num_thread = 4
#         self.client = client.Client\
# (self.host, self.port, "urls.txt", self.num_thread)

#     def tearDown(self):
#         self.client.executor.shutdown()
#         self.server.executor.shutdown()

    # def test_runing_server(self):
        # server_thread = threading.Thread(target=self.server.start)
        # # server_thread.daemon = True
        # server_thread.start()

        # time.sleep(1)

        # with mock.patch('server.Worker.scarpy') as mock_fetch:
        #     mock_fetch.return_value = {"word1": 10, "word2": 5}
        #     url = f"http://example.com/\n"
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM)\
        #  as client_socket:
        #         client_socket.connect((self.host, self.port))
        #         client_socket.send(url.encode('utf-8'))
        #         response = client_socket.recv(1024*10)
        #         data = json.loads(response)
        #         print(f"{url}: {data}")

        # server.SERVER_ON = False
        # server_thread.join()

        # server_thread = threading.Thread(target=self.server.start)
        # server_thread.daemon = True
        # server_thread.start()

        # client_thread = threading.Thread(target=self.client.read_urls)
        # client_thread.daemon = True
        # client_thread.start()

        # client_thread.join()

        # server.SERVER_ON = False
        # server_thread.join()


if __name__ == '__main__':
    unittest.main()
