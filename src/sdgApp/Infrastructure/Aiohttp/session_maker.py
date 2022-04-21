import aiohttp
import json
from typing import Dict, Optional
from sdgApp.Infrastructure.conf_parser import get_conf


class SingletonAiohttp:
    aiohttp_client: Optional[aiohttp.ClientSession] = None
    url: str = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=5*60)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout)
            conf = get_conf()
            cls.url = conf['TASK_MANAGER']['TASK_MANAGER_URL']
        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def post(cls, param: Dict):
        client = cls.get_aiohttp_client()
        async with client.post(url=cls.url, json={"task_param":param}) as resp:
            json_result = await resp.json()
        return json_result
