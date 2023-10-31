import argparse
import socket
import threading
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

IP = '127.0.0.1'
PORT = 8888
SIZE = 1024
FORMAT = 'utf-8'

TOTAL_URL = 0
SERVER_ON = True
LOCK = threading.Lock()


class Worker:
    def __init__(self, conn, num_of_common_words):
        self.conn = conn
        self.num_of_common_words = num_of_common_words

    def run(self):
        # global LOCK
        # global semaphore
        global TOTAL_URL

        with self.conn:
            # semaphore.acquire()
            print(f"Worker IN, current_thread_id: \
{threading.current_thread().native_id}")
            url = self.conn.recv(SIZE).decode(FORMAT)
            result = self.scarpy(url, self.num_of_common_words)

            LOCK.acquire()
            TOTAL_URL += 1
            print(f"Worker Processed {url}, Total URLs: {TOTAL_URL},\
current_thread_id: {threading.current_thread().native_id}")
            LOCK.release()

            self.conn.send(json.dumps(result).encode(FORMAT))
            print(f"Worker OUT, current_thread_id: \
{threading.current_thread().native_id}")
            self.conn.close()
        # semaphore.release()

    def scarpy(self, url, num_of_words):
        wlist = []
        sour_text = requests.get(url).text
        t_soup = BeautifulSoup(sour_text, 'html.parser')
        for each_text in t_soup.findAll('ul'):
            cont = each_text.text
            words = cont.lower().split()
            for e_w in words:
                wlist.append(e_w)
        res = self.filter_wlist(wlist, num_of_words)
        return res

    def filter_wlist(self, wordlist, num_of_words):
        cln_lst = []
        for word in wordlist:
            symbols = "!@#$%^&*()_-+={[}]|\\;:\"<>?/., "
            for i in range(len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                cln_lst.append(word)
        result = self.create_dict(cln_lst, num_of_words)
        return result

    @staticmethod
    def create_dict(clean_list, num):
        word_count = {}

        for word in clean_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        count = Counter(word_count)
        top = count.most_common(num)
        result = {}
        for name, counter in top:
            result[name] = counter
        return result


class MasterServer:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        if self.num_workers <= 0 or self.top_k <= 0:
            raise ValueError("Values must be above zero")
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

    def start(self):
        # global SERVER_ON
        socket.setdefaulttimeout(3)
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv.bind((self.host, self.port))
        serv.listen()
        print(
            f"Server listening on \
                {self.host}:{self.port} with {self.num_workers} workers")

        while SERVER_ON:
            try:
                conn, _ = serv.accept()
            except socket.timeout:
                continue
            worker = Worker(conn, self.top_k)
            self.executor.submit(worker.run)

        serv.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master-Worker Server")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        help="Number of workers",
        required=True)
    parser.add_argument(
        "-k",
        "--topk",
        type=int,
        help="Top K words",
        required=True)
    args = parser.parse_args()

    # semaphore = threading.Semaphore(args.workers)

    server = MasterServer(IP, PORT, args.workers, args.topk)
    server.start()
