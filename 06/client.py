import socket
import json
import argparse
from concurrent.futures import ThreadPoolExecutor

IP = '127.0.0.1'
PORT = 8888
SIZE = 1024
FORMAT = 'utf-8'


class Client:
    def __init__(self, server_host, server_port, urls_file, num_threads):
        self.server_host = server_host
        self.server_port = server_port
        self.urls_file = urls_file
        self.executor = ThreadPoolExecutor(max_workers=num_threads)

    def read_urls(self):
        with open(self.urls_file, "r", encoding=FORMAT) as file:
            for line in file:
                url = line.strip()
                self.executor.submit(self.send_request, url)

    def send_request(self, url):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))
        client_socket.send(url.encode(FORMAT))
        response = client_socket.recv(SIZE * 10)
        data = json.loads(response)
        print(f"{url}: {data}")
        client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client")
    parser.add_argument("threads", type=int, help="Number of threads")
    parser.add_argument(
        "urls_file",
        type=str,
        help="Path to the file with URLs")
    args = parser.parse_args()

    # semaphore = threading.Semaphore(args.threads)

    client = Client(IP, PORT, args.urls_file, args.threads)
    client.read_urls()
