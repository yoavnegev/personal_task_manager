import json
import random
import time
import attr


@attr.s(auto_attribs=True)
class TaskItem:
    title: str
    above: float = None
    below: float = None
    id: float = attr.ib() if not above and not below else random.uniform(below, above)

    @id.default
    def _id_uuid(self):
        return time.time()

    @classmethod
    def from_dict(cls, task_item_data: dict):
        task_item = cls(title=task_item_data['title'],
                        above=task_item_data['payload'],
                        below=task_item_data.get('failure_reason', ''))

        if 'id' in task_item_data:
            task_item.id = task_item_data['id']
        return task_item

    def serialize(self, use_json=False):
        data = dict(task_item_id=self.id,
                    title=self.title,
                    above=self.above,
                    below=self.below)

        return json.dumps(data) if use_json else data
