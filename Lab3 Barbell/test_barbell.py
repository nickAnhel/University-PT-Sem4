from barbell import Bar, Plate


new_bar = Bar(150)
new_bar.add_to_left(Plate(10))
new_bar.add_to_right(Plate(10))

new_bar.add_to_left(Plate(15))
new_bar.add_to_right(Plate(15))

new_bar.add_to_left(Plate(15))
new_bar.add_to_right(Plate(15))

new_bar.print_bar()

plates = [Plate(10), Plate(11), Plate(12)]
print(sum(plates))
