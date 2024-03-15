from parking import Parking, Car

park = Parking(10)
park.register_car_parking(Car("a", "v", "A111AA"))
park.register_car_parking(Car("a", "v", "B222BB"))
park.register_car_parking(Car("a", "v", "C333CC"))
park.register_car_parking(Car("a", "v", "D444DD"))

park.print_parking()

park.register_car_leave("A111AA")
print(park)
