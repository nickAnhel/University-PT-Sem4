import re
from functools import singledispatchmethod
from accessify import private


# fmt: off
class WrongRestrationNumberError(Exception): ...
class MaxCarsCountExcessError(Exception): ...
# fmt: on


class Car:
    """
    Represents a car.

    Attributes:
    ----------
    manufacturer : str
        Contains the manufacturer of the car.
    model : str
        Contains the model of the car.
    registration_number : str
        Contains the registration_number of the car.
    """
    registration_numbers: set[str] = set()

    def __init__(self, manufacturer: str, model: str, registration_number: str) -> None:
        self.__manufacturer: str = manufacturer
        self.__model: str = model
        self.__registration_number: str = self._validate_registration_number(registration_number)
        self.registration_numbers.add(registration_number)

    @property
    def manufacturer(self) -> str:
        """Get the manufacturer of the car."""
        return self.__manufacturer

    @property
    def model(self) -> str:
        """Get the model of the car."""
        return self.__model

    @property
    def registration_number(self) -> str:
        """Get the registration_number of the car."""
        return self.__registration_number

    def __str__(self) -> str:
        """Get the string representation of the car."""
        return f"{self.__manufacturer} {self.__model} n. {self.__registration_number}"

    @private
    def _validate_registration_number(self, number: str) -> str:
        """
        Validate the registration_number of the car.

        Parametrs:
        ---------
        number : str
            Registration number of the car.

        Returns:
        -------
        str
            Registration number if it's correct.

        Raises:
        ------
        WrongRestrationNumberError
            If registration_number of the car is not unique or does not match the pattern 'LdddLL'.
        """
        if number in self.registration_numbers:
            raise WrongRestrationNumberError("Registration number must be unique")

        pattern: re.Pattern[str] = re.compile(r"[A-Z]{1}\d{3}[A-Z]{2}")
        if not pattern.match(number):
            raise WrongRestrationNumberError("Registration number pattern must be 'LdddLL'")

        return number


class Parking:
    """
    Represents a parking.

    Attributes:
    ----------
    max_cars_count : int
        Contains the maximum cars count that can fit in the parking.

    Methods:
    -------
    def get_parked_cars_count() -> int:
        Return the total weight of the plates on the barbell.
    def get_car_by_registration_number(number: str) -> Car | None:
        Return the car by registration number.
    def register_car_parking(car: Car) -> None:
        Register the parked car.
    def register_car_pleave(arg: Car | str) -> None:
        Register the parked car leave.
    def print_parking() -> None:
        Print the string representation of the parking.
    """
    def __init__(self, max_car_count: int) -> None:
        self.__max_cars_count: int = self._validate_max_car_count(max_car_count)
        self.__parked_cars: list[Car] = []

    @property
    def max_cars_count(self) -> int:
        """Get the maximum cars count that can fit in the parking"""
        return self.__max_cars_count

    def get_parked_cars_count(self) -> int:
        """Get the number of cars parked"""
        return len(self.__parked_cars)

    def get_car_by_registration_number(self, number: str) -> Car | None:
        """
        Get the car by registration number.

        Parametrs:
        ---------
        number : str
            The registration number of the car.
        """
        for car in self.__parked_cars:
            if car.registration_number == number:
                return car
        return None

    def register_car_parking(self, car: Car) -> None:
        """
        Register the parked car.

        Parametrs:
        ---------
        car : Car
            Car that parked in the parking.

        Raises:
        ------
        MaxCarsCountExcessError
            If there is no parking space for the car.
        """
        if len(self.__parked_cars) + 1 >= self.__max_cars_count:
            raise MaxCarsCountExcessError("Number of parking spaces exceeded")

        self.__parked_cars.append(car)

    @singledispatchmethod
    def register_car_leave(self, arg) -> None:
        """
        Register the parked car leave.

        Parametrs:
        ---------
        arg : Car | str
            Car that leaved the parking.

        Raises:
        ------
        TypeError
            If arg is not Car or str.
        """
        raise TypeError(f"Argument must be of type 'Car' or 'str', not {type(arg)}")

    @register_car_leave.register
    def _(self, car: Car) -> None:
        if not self.__parked_cars:
            print("Parking is empty")
            return

        if car not in self.__parked_cars:
            print("Car is not parked")
            return

        self.__parked_cars.remove(car)

    @register_car_leave.register
    def _(self, registration_number: str) -> None:
        if not self.__parked_cars:
            print("Parking is empty")
            return

        car: Car | None = self.get_car_by_registration_number(registration_number)
        if car not in self.__parked_cars:
            print("Car is not parked")
            return

        self.__parked_cars.remove(car)

    def print_parking(self) -> None:
        """Print the string representation of the parking."""
        if not self.__parked_cars:
            print("Parking is empty")
            return

        print("\nParking")
        for _, car in enumerate(self.__parked_cars):
            print(f"| {car.registration_number} |")

        for _ in range(self.__max_cars_count - len(self.__parked_cars)):
            print("| ______ |")
        print()

    def __str__(self) -> str:
        """Get the string representation of the parking."""
        if not self.__parked_cars:
            return "Parking is empty"

        result = ["\nParking"]

        for car in self.__parked_cars:
            result.append(f"\n| {car.registration_number} |")

        for _ in range(self.__max_cars_count - len(self.__parked_cars)):
            result.append("\n| ______ |")

        return "".join(result) + "\n"

    @private
    def _validate_max_car_count(self, max_car_count: int) -> int:
        """
        Validate the max cars count.

        Parametrs:
        ---------
        max_car_count : int
            The maximum cars count that can fit in the parking.

        Returns:
        -------
        int
            Maximum cars count if it's correct.

        Raises:
        ------
        TypeError
            If maximum cars count less than or equal to zero.
        """
        if max_car_count <= 0:
            raise TypeError("Maximum cars count must be greater than zero")
        return max_car_count
