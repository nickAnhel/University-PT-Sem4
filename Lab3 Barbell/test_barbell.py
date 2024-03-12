from barbell import Bar, Plate
# from barbell import ImbalanceError


new_bar = Bar(150)

new_bar.add_to_left(Plate(10))
new_bar.add_to_right(Plate(10))

new_bar.add_to_left(Plate(15))
new_bar.add_to_right(Plate(15))

new_bar.add_to_left(Plate(19))
new_bar.add_to_right(Plate(19))

print(new_bar)
