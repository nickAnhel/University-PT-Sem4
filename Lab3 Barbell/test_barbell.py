import pytest
from barbell import ImbalanceError, MaxWeightExcessError, Plate, Bar, NegativeOrZeroWeightError


# Fixtires
@pytest.fixture(name="plate_10")
def fixture_plate_10() -> Plate:
    return Plate(10)


@pytest.fixture(name="plate_20")
def fixture_plate_20() -> Plate:
    return Plate(20)


@pytest.fixture(name="plate_30")
def fixture_plate_30() -> Plate:
    return Plate(30)


@pytest.fixture(name="bar_150")
def fixture_bar_150() -> Bar:
    return Bar(150)


# Plate tests
@pytest.mark.plate
def test_plate_init(plate_10):
    assert plate_10.weight == 10


@pytest.mark.plate
def test_plate_validate_weight():
    with pytest.raises(NegativeOrZeroWeightError):
        Plate(0)
    with pytest.raises(NegativeOrZeroWeightError):
        Plate(-10)


@pytest.mark.plate
def test_plate_radd(plate_10):
    assert 10 + plate_10 == 20
    with pytest.raises(TypeError):
        "1" + plate_10


# Bar tests
@pytest.mark.bar
def test_bar_init(bar_150) -> None:
    assert bar_150.max_weight == 150


@pytest.mark.bar
def test_bar_validate_max_weight() -> None:
    with pytest.raises(NegativeOrZeroWeightError):
        Bar(0)
    with pytest.raises(NegativeOrZeroWeightError):
        Bar(-150)


@pytest.mark.bar
def test_bar_balance_factor(bar_150, plate_10, plate_20) -> None:
    bar_150.add_to_left(plate_10)
    bar_150.add_to_right(plate_20)
    assert bar_150.get_balance_factor() == 10

    bar_150.add_to_left(plate_10)
    assert bar_150.get_balance_factor() == 0

    bar_150.add_to_left(plate_10)
    assert bar_150.get_balance_factor() == 10


@pytest.mark.bar
def test_bar_add(bar_150, plate_10) -> None:
    bar_150.add_to_left(plate_10)
    assert bar_150.get_total_weight() == 10
    assert bar_150.get_balance_factor() == 10

    bar_150.add_to_right(plate_10)
    assert bar_150.get_total_weight() == 20
    assert bar_150.get_balance_factor() == 0

    bar_150.add(plate_10)
    assert bar_150.get_total_weight() == 30
    assert bar_150.get_balance_factor() == 10


@pytest.mark.bar
def test_bar_pop(bar_150, plate_10) -> None:
    bar_150.add(plate_10)
    bar_150.add(plate_10)

    left_plate: Plate = bar_150.pop_left()
    assert isinstance(left_plate, Plate)
    assert left_plate.weight == Plate(10).weight
    assert bar_150.get_total_weight() == 10

    right_plate: Plate = bar_150.pop_right()
    assert isinstance(right_plate, Plate)
    assert right_plate.weight == Plate(10).weight
    assert bar_150.get_total_weight() == 0


@pytest.mark.bar
def test_bar_max_weight_excess() -> None:
    bar = Bar(30)
    plate = Plate(40)
    with pytest.raises(MaxWeightExcessError):
        bar.add(plate)


@pytest.mark.bar
def test_bar_imbalance_error(bar_150, plate_10, plate_30):
    bar_150.add(plate_10)
    with pytest.raises(ImbalanceError):
        bar_150.add(plate_30)
