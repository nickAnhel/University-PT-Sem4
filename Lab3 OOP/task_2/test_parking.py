import pytest
from parking import MaxCarsCountExcessError, Parking, Car, RegistrationNumberError


# Car tests
@pytest.mark.car
def test_car_init() -> None:
    car = Car("Honda", "A1", "A111BC")
    assert car.manufacturer == "Honda"
    assert car.model == "A1"
    assert car.registration_number == "A111BC"


@pytest.mark.car
def test_car_to_str() -> None:
    car = Car("Honda", "A2", "A222BC")
    assert str(car) == "Honda A2 n. A222BC"


@pytest.mark.car
def test_car_validate_registration_number() -> None:
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A3", "A222BC")
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A4", "a111bc")
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A4", "123abc")
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A4", "")
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A4", "a")
    with pytest.raises(RegistrationNumberError):
        Car("Honda", "A4", "a123aaa")


# Parking tests
@pytest.mark.parking
def test_parking_init() -> None:
    p = Parking(10)
    assert p.max_cars_count == 10


@pytest.mark.parking
def test_parking_validate_max_cars_count() -> None:
    with pytest.raises(TypeError):
        Parking(0)
    with pytest.raises(TypeError):
        Parking(-10)


@pytest.mark.parking
def test_parking_register_car_parking() -> None:
    p = Parking(10)
    p.register_car_parking(Car("BMW", "B1", "B111CD"))
    assert p.get_parked_cars_count() == 1

    p.register_car_parking(Car("BMW", "B1", "B222CD"))
    assert p.get_parked_cars_count() == 2


@pytest.mark.parking
def test_parking_max_cars_count_excess_error() -> None:
    p = Parking(1)
    p.register_car_parking(Car("BMW", "B1", "B333CD"))
    with pytest.raises(MaxCarsCountExcessError):
        p.register_car_parking(Car("BMW", "B1", "B444CD"))


@pytest.mark.parking
def test_parking_get_car_by_registration_number() -> None:
    p = Parking(10)
    p.register_car_parking(Car("BMW", "B1", "B555CD"))
    car = p.get_car_by_registration_number("B555CD")
    assert car.manufacturer == "BMW"
    assert car.model == "B1"
    assert car.registration_number == "B555CD"


@pytest.mark.parking
def test_parking_register_car_leave() -> None:
    p = Parking(10)
    car_1 = Car("BMW", "B1", "B666CD")
    car_2 = Car("BMW", "B1", "B777CD")
    p.register_car_parking(car_1)
    p.register_car_parking(car_2)

    p.register_car_leave(car_1)
    assert p.get_parked_cars_count() == 1

    p.register_car_leave("B777CD")
    assert p.get_parked_cars_count() == 0

    with pytest.raises(TypeError):
        p.register_car_leave(1)


@pytest.mark.parking
def test_parking_to_str() -> None:
    p1 = Parking(5)
    p1.register_car_parking(Car("BMW", "B1", "B888CD"))
    p1.register_car_parking(Car("BMW", "B1", "B999CD"))
    assert str(p1) == "\nParking\n| B888CD |\n| B999CD |\n| ______ |\n| ______ |\n| ______ |\n"
