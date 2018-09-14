import asyncio
import requests
from datetime import datetime

import asyncio
from aiohttp import ClientSession


url = 'http://localhost:8000/api/v1/cars/?page={page}&page_size=10'
urls = []
for i in range(1, 728):
    urls.append(url.format(page=i))


start = datetime.now()
responses = []
for url in urls:
    response = requests.get(url)
    responses.append(response)
finish = datetime.now()
print(len(responses))
print(finish - start)


start = datetime.now()
async def get_all(urls):
    loop = asyncio.get_event_loop()
    futures = []
    for url in urls:
        future = loop.run_in_executor(None, requests.get, url)
        futures.append(future)

    responses = await asyncio.gather(*futures)
    return responses


loop = asyncio.get_event_loop()
print(len(loop.run_until_complete(get_all(urls))))

finish = datetime.now()
print(finish - start)


start = datetime.now()
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_all2(urls):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

loop = asyncio.get_event_loop()
print(len(loop.run_until_complete(get_all2(urls))))

finish = datetime.now()
print(finish - start)



start = datetime.now()
async def fetch2(semaphore, session, url):
    async with semaphore:
        async with session.get(url) as response:
            return await response.json()

async def get_all3(urls):
    sem = asyncio.Semaphore(value=50)
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch2(sem, session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

loop = asyncio.get_event_loop()
print(len(loop.run_until_complete(get_all3(urls))))

finish = datetime.now()
print(finish - start)


loop.close()
