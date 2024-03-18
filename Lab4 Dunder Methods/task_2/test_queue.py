from my_queue import Queue


q1 = Queue([1, 2, 3])
q1.push(4)

for item in q1:
    print(item)

print(q1.pop())
print(q1)
print(len(q1))

print(Queue([1, 2]) + Queue([3, 4]))

q2 = Queue([4, 5])
q2 += q1
print(q2)
print(q1)

if q1:
    print("True")
