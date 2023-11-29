import pytest
import asyncio


# Something is very wrong in the initialisation of asyncio loop using httpx
# and pytest-asyncio. This is a workaround for endpoints only.
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
