from my_queue import MyQueue


q1 = MyQueue([1, 2, 3])
q1.push(4)

for item in q1:
    print(item)

print(q1.pop())
print(q1)
print(len(q1))

print(MyQueue([1, 2]) + MyQueue([3, 4]))

q2 = MyQueue([4, 5])
q2 += q1
print(q2)
print(q1)

if q1:
    print("True")

items = q1.items
items[0] = 100
print(items, q1.items)


print(q1.pop())
print(q1)
