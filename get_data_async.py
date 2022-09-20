import aiohttp
import asyncio

from config import Config
from parse_data import parse_data


async def get_data(order: dict):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for key, value in order.items():
            await asyncio.sleep(2)
            print(key)
            print(value)
            task = asyncio.create_task(
                get_product_data(session, key, value)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
    return order


counter = 1
async def get_product_data(
        session: aiohttp.ClientSession, index: int, prod_values: dict
):
    ABB_BASE_URL = "https://new.abb.com/products/ru/"
    url = f"{ABB_BASE_URL}{prod_values['article']}"
    async with session.get(url=url, headers=Config.headers) as response:
        if str(response.status).startswith("5"):
            return get_product_data(
                session, index, prod_values
            )
        response_text = await response.text()
        parse_data(response_text)
        with open("index.html", "w") as f:
            f.write(response_text)
        global counter
        print(f"{counter}: {response.status}, {index}")
        counter += 1


def _update_data(data: dict, response: str) -> None:
    new_data = parse_data(response)
