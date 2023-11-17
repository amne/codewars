class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.queues = list(list(q) for q in queues)
        self.capacity = capacity
        self.inside = []
        self.visited = []
        pass

    def done(self):
        q1 = [q for q in self.queues if len(q)]
        return not(q1 and self.inside)

    def continue_up(self, currentFloor):
        # how many people inside want to go higher
        # are there people higher or on the current floor that want the elevator?
        higher_inside = [x for x in self.inside if x > currentFloor]
        higher_currentFloor = [x for x in self.queues[currentFloor] if x > currentFloor]
        higher_queues = [x for (i, x) in zip(range(len(self.queues)), self.queues) if i > currentFloor and x]
        return higher_queues or higher_inside or higher_currentFloor

    def continue_down(self, currentFloor):
        # how many people inside want to go lower
        # are there people lower or on the current floor that want the elevator?
        lower_inside = [x for x in self.inside if x < currentFloor]
        lower_currentFloor = [x for x in self.queues[currentFloor] if x < currentFloor]
        lower_queues = [x for (i, x) in zip(range(len(self.queues)), self.queues) if i < currentFloor and x]
        return lower_queues or lower_inside or lower_currentFloor

    def move(self, currentFloor, direction):
        # visited = are we stopping on this floor?
        visited = False
        try:
            self.inside.index(currentFloor)
            visited = True
            self.inside = [p for p in self.inside if p != currentFloor]
        except ValueError as e:
            pass

        # if we're going up but there's no reason, go down (and vice versa)
        if (direction > 0 and not self.continue_up(currentFloor)) or (direction < 0 and not self.continue_down(currentFloor)):
            # if there's no reason to go up or down .. stay
            if not self.continue_up(currentFloor) and not self.continue_down(currentFloor):
                direction = 0
            else:
                direction = direction * -1

        for x in self.queues[currentFloor]:
            if (direction > 0 and x > currentFloor) or (direction < 0 and x < currentFloor):
                # there are people on this floor that called the lift
                visited = True
                # but we're full
                if len(self.inside) == self.capacity:
                    break

                # just a weird way to move people from the queue inside the lift
                i = self.queues[currentFloor].index(x)
                self.queues[currentFloor] = self.queues[currentFloor][0:i] + self.queues[currentFloor][i + 1:]
                self.inside.append(x)

        # if we stopped at this floor then "add it to the list, dde fam"
        if visited:
            self.visited.append(currentFloor)

        # move only if we're not staying.
        #    - Captain Obvious
        if direction:
            self.move(currentFloor + direction, direction)

    def theLift(self):
        self.move(0, 1)

        # empty building
        if not self.visited:
            self.visited = [0]

        # pad the list with the ground floor
        if self.visited[0] != 0:
            self.visited = [0] + self.visited
        if self.visited[-1] != 0:
            self.visited = self.visited + [0]

        return self.visited

# x = [[], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
x = [[],[],[],[],[],[],[]]
liftx = Dinglemouse(x, 5)
print(liftx.theLift())


#    G   1   2          3   4   5   6
a = ((), (), (5, 5, 5), (), (), (), ())

#    G   1   2       3   4   5   6
b = ((), (), (1, 1), (), (), (), ())

#    G   1     2     3   4     5   6
c = ((), (3,), (4,), (), (5,), (), ())

#    G   1     2   3   4     5     6
d = ((), (0,), (), (), (2,), (3,), ())

# lifta = Dinglemouse(a, 5)
# liftb = Dinglemouse(b, 5)
# liftc = Dinglemouse(c, 5)
# liftd = Dinglemouse(d, 5)


# print(lifta.theLift())
# print(liftb.theLift())
# print(liftc.theLift())
# print(liftd.theLift())
