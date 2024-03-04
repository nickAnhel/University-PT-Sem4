from accessify import private
from exceptions import MaxWeightException, ImbalanceException


class Plate:
    def __init__(self, weight: int) -> None:
        self.__weight: int = weight

    @property
    def weight(self) -> int:
        return self.__weight

    def __radd__(self, other) -> int:
        if not isinstance(other, int):
            raise TypeError("Left operand must be 'int'")
        return self.weight + other


class Bar:
    def __init__(self, max_weight: int) -> None:
        self.__max_weight: int = max_weight
        self.__left_side: list[Plate] = []
        self.__right_side: list[Plate] = []

    @property
    def max_weight(self) -> int:
        return self.__max_weight

    def total_weight(self) -> int:
        return self._get_side_weight() + self._get_side_weight(is_left=False)

    def balance_factor(self) -> int:
        return abs(self._get_side_weight() - self._get_side_weight(False))

    def add_to_left(self, plate: Plate) -> None:
        self._validate_bar(plate)
        self._validate_bar_balance(plate, "left")
        self.__left_side.append(plate)

    def add_to_right(self, plate: Plate) -> None:
        self._validate_bar(plate)
        self._validate_bar_balance(plate, "right")
        self.__right_side.append(plate)

    def print_bar(self) -> None:
        for plate in self.__left_side:
            print(f"={plate.weight}", end="")

        print("=|=============|=", end="")

        for plate in self.__right_side:
            print(f"{plate.weight}=", end="")

        print()

    @private
    def _get_side_weight(self, is_left: bool = True) -> int:
        plates: list[Plate] = self.__left_side if is_left else self.__right_side

        total_weight = 0
        for plate in plates:
            total_weight += plate.weight

        return total_weight

    @private
    def _validate_bar(self, plate: Plate) -> None:
        if self.total_weight() + plate.weight > self.max_weight:
            raise MaxWeightException("Maximum weight exceeded")

    @private
    def _validate_bar_balance(self, plate: Plate, side: str) -> None:
        if side == "left":
            if (
                abs(
                    self._get_side_weight()
                    + plate.weight
                    - self._get_side_weight(False)
                )
                >= 20
            ):
                raise ImbalanceException("Balancing allowed level exceeded")
        else:
            if (
                abs(
                    self._get_side_weight()
                    - plate.weight
                    - self._get_side_weight(False)
                )
                >= 20
            ):
                raise ImbalanceException("Balancing allowed level exceeded")
