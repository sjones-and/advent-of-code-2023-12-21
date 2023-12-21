#!/usr/bin/env python3

import os
from time import perf_counter_ns
from numpy.polynomial import Polynomial

class Position:
    all = {}
    neighbours = [(1,0),(0,1),(-1,0),(0,-1)]

    def wire_up_all_neighbours():
        for position in Position.all.values():
            position.wire_up_neighbours()

    def move_all():
        start_positions = [position.reset() for position in Position.all.values() if position.value == 'O']
        for position in start_positions:
            position.move()

    def __init__(self, value, x, y):
        self.x = x
        self.y = y
        self.value = value
        if value == 'S':
            self.value = 'O'
        self.visitable_neighbours = []

    def wire_up_neighbours(self):
        for neighbour_offset in Position.neighbours:
            if neighbour := Position.all.get((neighbour_offset[0]+self.x, neighbour_offset[1]+self.y), None):
                if neighbour.value != '#':
                    self.visitable_neighbours.append(neighbour)

    def reset(self):
        self.value = '.'
        return self
    
    def move(self):
        for position in self.visitable_neighbours:
            position.value = 'O'

def answer(input_file):
    start = perf_counter_ns()

    with open(input_file, 'r') as input_stream:
        start_x, start_y =  [(x, y) for y,row in enumerate(input_stream) for x,value in enumerate(row.strip()) if value == 'S'][0]
        input_stream.seek(0)
        data = input_stream.read().replace('S','.').split('\n')
        row_len = len(data[0])
        row_count = len(data)
        data = [row * 9 for row in data]
        data = data * 9
        Position.all = {(x,y): Position(value, x, y) for y,row in enumerate(data) for x,value in enumerate(row.strip())}
        Position.all[((row_len * 4) + start_x, (row_count * 4) + start_y)].value = 'O'

    Position.wire_up_all_neighbours()

    x_values = []
    y_values = []

    max_x = (row_len * 9) // 2
    for x in range(max_x):
        Position.move_all()
        if (x + 1) % row_len == ((row_len - 1) // 2):
            x_values.append(x + 1)
            y_values.append(len([position for position in Position.all.values() if position.value == 'O']))
    
    model = Polynomial.fit(x_values, y_values, 2)
    answer = int(round(model(26501365),0))
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
