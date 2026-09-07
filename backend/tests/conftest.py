import pytest

from app import main


@pytest.fixture(autouse=True)
def reset_state() -> None:
    """Give every test a clean, empty app.

    The API keeps its notes in module-level state, so without this the
    tests would leak items into each other and pass or fail depending on
    the order pytest happens to run them in.
    """
    main._items.clear()
    main._next_id = 1
    main._total_characters = 0
