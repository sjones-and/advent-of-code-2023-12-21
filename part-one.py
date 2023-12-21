#!/usr/bin/env python3

import os
from time import perf_counter_ns

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
        Position.all = {(x,y): Position(value, x, y) for y,row in enumerate(input_stream) for x,value in enumerate(row.strip())}

    Position.wire_up_all_neighbours()
    for _ in range(64):
        Position.move_all()
    
    answer = len([position for position in Position.all.values() if position.value == 'O'])
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
