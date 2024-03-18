from accessify import private


# fmt: off
class ImbalanceError(Exception): ...
class MaxWeightExcessError(Exception): ...
class NegativeOrZeroWeightError(Exception): ...
# fmt: on


class Plate:
    """
    Represents a plate.

    Attributes:
    ----------
    weight : int
        Contains the weight of the plate.
    """

    def __init__(self, weight: int) -> None:
        self.__weight: int = self._validate_weight(weight)

    @property
    def weight(self) -> int:
        """Get the weight of the plate."""
        return self.__weight

    def __radd__(self, other: int) -> int:
        """
        Add the weight of the playte to the integer.

        Parametrs:
        ---------
        other : int
            The integer to add the weight to.

        Raises:
        ------
        TypeError
            If the lefy operand is not an integer.

        Returns:
        -------
        int
            The sum of the weight and the integer.
        """
        if not isinstance(other, int):
            raise TypeError("Left operand must be 'int'")
        return self.__weight + other

    @private
    def _validate_weight(self, weight: int) -> int:
        """
        Validate the weight.

        Parametrs:
        ---------
        weight : int
            Weight of the plate.

        Returns:
        -------
        weight : int
            Weight if it's correct.

        Raises:
        ------
        NegativeOrZeroWeightError
            If weight less than or equal to zero.
        """
        if weight <= 0:
            raise NegativeOrZeroWeightError("Weight must be greater than zero")
        return weight


class Bar:
    """
    Represents a barbell.

    Attributes:
    ----------
    max_weight : int
        Contains the maximum weight that the barbell can withstand.

    Methods:
    -------
    def get_total_weight() -> int:
        Return the total weight of the plates on the barbell.

    def get_balance_factor() -> int:
        Return the weight difference between the left and the right sides of the barbell.

    def add_to_left(plate: Plate) -> None:
        Add the plate to the left side of the barbell.

    def add_to_right(plate: Plate) -> None:
        Add the plate to the right side of the barbell.

    def add(plate: Plate) -> None:
        Add the plate to the side of the barbell where the level of balance factor will be minimal.

    def pop_left() -> Plate:
        Remove the last added plate from the left side of the barbell and return it.

    def pop_right() -> Plate:
        Remove the last added plate from the right side of the barbell and return it.

    def print_bar() -> None:
        Print the string representation of the barbell.
    """

    def __init__(self, max_weight: int) -> None:
        self.__max_weight: int = self.__validate_max_weight(max_weight)
        self.__left_plates: list[Plate] = []
        self.__right_plates: list[Plate] = []

    @property
    def max_weight(self) -> int:
        """Get the maximum weight that the barbell can withstand."""
        return self.__max_weight

    def get_total_weight(self) -> int:
        """Get the total weight of the plates on the barbell."""
        return sum(self.__left_plates) + sum(self.__right_plates)

    def get_balance_factor(self) -> int:
        """Get the weight difference modulus between the left and the right sides of the barbell."""
        return abs(sum(self.__left_plates) - sum(self.__right_plates))

    def add_to_left(self, plate: Plate) -> None:
        """
        Add the plate to the left side of the barbell.

        Parametrs:
        ---------
        plate : Plate
            Plate to add to the barbell.

        Raises:
        ------
        MaxWeightExcessError
            If adding a plate will lead to increase in the maximum weight.
        ImbalanceError
            If adding a plate will lead to increase in the acciptable level of imbalance.
        """
        self.__validate_bar(plate)
        self.__validate_bar_balance(plate)
        self.__left_plates.append(plate)

    def add_to_right(self, plate: Plate) -> None:
        """
        Add the plate to the right side of the barbell.

        Parametrs:
        ---------
        plate : Plate
            Plate to add to the barbell.

        Raises:
        ------
        MaxWeightExcessError
            If adding a plate will lead to increase in the maximum weight.
        ImbalanceError
            If adding a plate will lead to increase in the acciptable level of imbalance.
        """
        self.__validate_bar(plate)
        self.__validate_bar_balance(plate, to_left=False)
        self.__right_plates.append(plate)

    def add(self, plate: Plate) -> None:
        """
        Add the plate to the side of the barbell where the level of balance factor will be minimal.

        Parametrs:
        ---------
        plate : Plate
            Plate to add to the barbell.

        Raises:
        ------
        MaxWeightExcessError
            If adding a plate will lead to increase in the maximum weight.
        ImbalanceError
            If adding a plate will lead to increase in the acciptable level of imbalance.
        """
        to_left_balance: int = abs(sum(self.__left_plates) + plate.weight - sum(self.__right_plates))
        to_right_balance: int = abs(sum(self.__left_plates) - plate.weight - sum(self.__right_plates))

        if to_left_balance <= to_right_balance:
            self.add_to_left(plate)
        else:
            self.add_to_right(plate)

    def pop_left(self) -> Plate:
        """
        Remove the last added plate from the left side of the barbell and return it.

        Returns:
        -------
        plate : Plate
            The last plate added to the left side of the barbell.

        Raises:
        ------
        ImabalnceError
            If the removal of the plate would cause the permissible level of imbalance to be exceeded.
        """
        if not self.__left_plates:
            return None

        left_side: list[Plate] = self.__left_plates[:-1]
        if abs(sum(left_side) - sum(self.__right_plates)) >= 20:
            raise ImbalanceError("Balancing allowed level exceeded")

        return self.__left_plates.pop()

    def pop_right(self) -> Plate:
        """
        Remove the last added plate from the right side of the barbell and return it.

        Returns:
        -------
        plate : Plate
            The last plate added to the right side of the barbell.

        Raises:
        ------
        ImabalnceError
            If the removal of the plate would cause the permissible level of imbalance to be exceeded.
        """
        if not self.__right_plates:
            return None

        right_side: list[Plate] = self.__right_plates[:-1]
        if abs(sum(self.__left_plates) - sum(right_side)) >= 20:
            raise ImbalanceError("Balancing allowed level exceeded")

        return self.__right_plates.pop()

    def print_bar(self) -> None:
        """Print the string representation of the barbell."""
        for plate in self.__left_plates[::-1]:
            print(f"={plate.weight}", end="")

        print("=|=============|=", end="")

        for plate in self.__right_plates:
            print(f"{plate.weight}=", end="")

        print()

    def __str__(self) -> str:
        """Get the string representation of the barbell."""
        result = []

        for plate in self.__left_plates[::-1]:
            result.append(f"={plate.weight}")

        result.append("=|=============|=")

        for plate in self.__right_plates:
            result.append(f"{plate.weight}=")

        return "".join(result)

    @private
    def __validate_max_weight(self, weight: int) -> int:
        """
        Validate the max weight.

        Parametrs:
        ---------
        weight : int
            Max weight of the barbell.

        Returns:
        -------
        int
            Max weight if it's correct.

        Raises:
        ------
        NegativeOrZeroWeightError
            If max weight less than or equal to zero.
        """
        if weight <= 0:
            raise NegativeOrZeroWeightError("Weight must be greater than zero")
        return weight

    @private
    def __validate_bar(self, plate: Plate) -> None:
        """
        Validate the barbell with added plate.

        Parametrs:
        ---------
        plate : Plate
            Plate to add on the barbell.

        Raises:
        ------
        MaxWeightExcessError
            If the adding of the plate will lead to increase in the maximum weight.
        """
        if self.get_total_weight() + plate.weight > self.__max_weight:
            raise MaxWeightExcessError("Maximum weight exceeded")

    @private
    def __validate_bar_balance(self, plate: Plate, to_left: bool = True) -> None:
        """
        Validate balance factor of the barbell with added plate.

        Parametrs:
        ---------
        plate : Plate
            Plate to add on the side of the barbell.
        to_left : bool
            Plate is added to the left side.
            Default: True.

        Raises:
        ------
        ImbalanceError
            If adding a plate will lead to increase in the acciptable level of imbalance.
        """
        if to_left:
            side_coef = 1
        else:
            side_coef = -1

        if abs(sum(self.__left_plates) - sum(self.__right_plates) + side_coef * plate.weight) >= 20:
            raise ImbalanceError("Balancing allowed level exceeded")
