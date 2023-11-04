import asyncio
import argparse
import aiohttp


def parse_args():
    parser = argparse.ArgumentParser(description='URL fetcher')
    parser.add_argument(
        'num_requests',
        type=int,
        help='Number of concurrent requests')
    parser.add_argument('url_file', type=str, help='File containing URLs')
    args = parser.parse_args()
    if args.num_requests <= 0:
        raise ValueError("Value <= then 0")
    return args


async def fetch_url(url, sem):
    async with aiohttp.ClientSession() as session:
        async with sem:
            async with session.get(url) as resp:
                # print(f'{url} - {resp.status}')
                return url, resp.status


async def fetch_worker(que, sem):
    while True:
        url = await que.get()
        try:
            result = await fetch_url(url, sem)
            return result
        finally:
            que.task_done()


async def read_urls(file_path, num_req):
    que = asyncio.Queue()
    sem = asyncio.Semaphore(num_req)
    workers = []
    results = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            await que.put(url)

            task = asyncio.create_task(fetch_worker(que, sem))
            workers.append(task)

    # await que.join()
    while workers:
        done, _ = await asyncio.wait(workers,
                                     return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            result = await task
            results.append(result)
            print(f"Result: {result[0]} - {result[1]}")
            workers.remove(task)

    for worker in workers:
        worker.cancel()

    return results


async def main():
    args = parse_args()
    num_requests = args.num_requests
    url_file = args.url_file

    result = await read_urls(url_file, num_requests)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
