from datetime import datetime
from uuid import UUID


def test_constructor_test_entity():
    """
    Test the constructor of the Test entity in the
    template_api.models module.
    """
    from app.models import Test

    test = Test(
        UUID("00000000-0000-0000-0000-000000000000"),
        UUID("00000000-0000-0000-0000-000000000001"),
        datetime(2021, 1, 1),
        True,
        {"name": "template_api", "type": "1"},
    )

    assert test.id == UUID("00000000-0000-0000-0000-000000000000")
    assert test.part_id == UUID("00000000-0000-0000-0000-000000000001")
    assert test.timestamp == datetime(2021, 1, 1)
    assert test.data == {"name": "template_api", "type": "1"}
    assert test.successful is True


def test_constructor_part_entity():
    """
    Test the constructor of the Part entity.

    It should create a Part object with the given name,
    modified timestamp, and ID.
    """
    from app.models import Part

    part = Part(
        UUID("00000000-0000-0000-0000-000000000000"),
        "part_1",
        datetime(2021, 1, 1),
    )

    assert part.id == UUID("00000000-0000-0000-0000-000000000000")
    assert part.name == "part_1"
    assert part.modified_timestamp == datetime(2021, 1, 1)
