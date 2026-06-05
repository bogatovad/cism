from fastapi import FastAPI, Depends
from src.frameworks_and_drivers.http_web_fastapi.depends import (
    task_controller_dependency,
)
from src.interface_adapters.controllers.task import TaskController


app = FastAPI()


@app.get("/")
async def create_task(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.create_task()
    return {"Hello": "World"}
