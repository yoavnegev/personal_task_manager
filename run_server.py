import uvloop
import logging

from api.handler import TaskItemView
from aiohttp import web

app_name = "task_items"


def get_app() -> web.Application:
    app = web.Application()
    app.router.add_post('/task_item/', TaskItemView)
    app.router.add_get('/task_item/{task_item_id}/', TaskItemView)
    app.router.add_delete('/task_item/', TaskItemView)
    app.router.add_put('/task_item/', TaskItemView)
    return app


def main():
    uvloop.install()
    app = get_app()
    logging.info(f"{app_name} is starting, listening on port 8000")
    web.run_app(app, port=8000)


if __name__ == '__main__':
    main()
