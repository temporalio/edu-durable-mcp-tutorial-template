import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from activities import make_nws_request
from workflow import GetForecast

async def main():
    # Connect to Temporal service
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="weather-task-queue", # Task queue that your Worker is listening to.
        workflows=[GetForecast], # Register the Workflow on your Worker
        activities=[make_nws_request], # Register the Activities on your Worker
    )

    print("Worker started. Listening for workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())