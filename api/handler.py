import asyncio
import logging

from aiohttp import web
from aiohttp.web import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from datastore.models import TaskItem
from datastore.redis import RedisStore


class TaskItemView(web.View):

    async def post(self) -> Response:
        task_item: TaskItem = await self._parse_request(self.request)
        redis = self.get_redis()
        await self.add_task_item(redis, task_item)
        return web.json_response(task_item.serialize())

    async def get(self) -> Response:
        redis = self.get_redis()
        task_item: TaskItem = await redis.get_sorted_task_items()
        serialized_task = task_item.serialize()
        return web.json_response(serialized_task)

    async def update(self) -> Response:
        redis = self.get_redis()
        task_item: TaskItem = await self._parse_request(self.request)
        await self._send_update_task_item(redis, task_item)
        serialized_task = task_item.serialize()
        return web.json_response(serialized_task)

    async def delete(self) -> Response:
        redis = self.get_redis()
        task_item: TaskItem = await self._parse_request(self.request)
        await self._send_delete_task_item(redis, task_item)
        serialized_task = task_item.serialize()
        return web.json_response(serialized_task)

    @classmethod
    async def add_task_item(cls, redis, task_item):
        await redis.save_task_item(task_item)
        event_loop = asyncio.get_event_loop()
        await event_loop.run_in_executor(None, lambda: cls._send_save_task_item(redis, task_item))
        return task_item

    @staticmethod
    def get_redis():
        return RedisStore(host='localhost', port='6379')

    @staticmethod
    def _send_save_task_item(redis, task_item):
        redis.save_task_item(task_item)

    @staticmethod
    def _send_update_task_item(redis, task_item):
        redis.update_task_item(task_item)

    @staticmethod
    def _send_delete_task_item(redis, task_item):
        redis.delete_task_item(task_item)

    @classmethod
    async def _parse_request(cls, request: Request) -> TaskItem:
        if not await request.text():
            raise HTTPBadRequest(text='No request payload')
        try:
            raw_task = await request.json()
        except Exception as e:
            logging.error('payload is not a valid json', extra={'error': e.__class__.__name__, 'reason': e.args[0]})
            raise HTTPBadRequest(text='payload is not a valid json')
        return TaskItem.from_dict(raw_task)
