from redis import StrictRedis
from .models import TaskItem


TASK_ITEMS = "task_items"


class RedisStore:

    def __init__(self, host, port):
        self.redis = StrictRedis(host=host, port=port, db=0)

    def flushdb(self):
        self.redis.flushdb()

    # TaskItems
    def save_task_item(self, task_item: TaskItem):
        self.redis.hset(TASK_ITEMS, str(task_item.id), task_item.title)

    def get_sorted_task_items(self):
        all_task_items = self.redis.hgetall(TASK_ITEMS)
        return [all_task_items[key] for key in sorted(all_task_items.keys(), reverse=True)]

    def delete_task_item(self, task_item_id: float):
        self.redis.hdel(TASK_ITEMS, str(task_item_id))

    def update_task_item(self, task_item_id, title: str):
        task_item = self.redis.hset(TASK_ITEMS, str(task_item_id), title)
        return task_item

