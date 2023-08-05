#!/usr/bin/env python3

import outfancy
import random
import sys
from time import sleep

motor = outfancy.render.Table()
motor_oneline = outfancy.render.Oneline()

color_list = ['\x1b[0;30m', '\x1b[0;31m', '\x1b[0;32m', '\x1b[0;33m', '\x1b[0;34m', '\x1b[0;35m', '\x1b[0;36m', '\x1b[0;37m', '\x1b[0;39m', '\x1b[0;40m', '\x1b[0;41m', '\x1b[0;42m', '\x1b[0;43m', '\x1b[0;44m', '\x1b[0;45m', '\x1b[0;46m', '\x1b[0;47m', '\x1b[0;49m', '\x1b[0;90m', '\x1b[0;91m', '\x1b[0;92m', '\x1b[0;93m', '\x1b[0;94m', '\x1b[0;95m', '\x1b[0;96m', '\x1b[0;97m', '\x1b[0;99m', '\x1b[0;100m', '\x1b[0;101m', '\x1b[0;102m', '\x1b[0;103m', '\x1b[0;104m', '\x1b[0;105m', '\x1b[0;106m', '\x1b[0;107m', '\x1b[0;109m', '\x1b[1;30m', '\x1b[1;31m', '\x1b[1;32m', '\x1b[1;33m', '\x1b[1;34m', '\x1b[1;35m', '\x1b[1;36m', '\x1b[1;37m', '\x1b[1;39m', '\x1b[1;40m', '\x1b[1;41m', '\x1b[1;42m', '\x1b[1;43m', '\x1b[1;44m', '\x1b[1;45m', '\x1b[1;46m', '\x1b[1;47m', '\x1b[1;49m', '\x1b[1;90m', '\x1b[1;91m', '\x1b[1;92m', '\x1b[1;93m', '\x1b[1;94m', '\x1b[1;95m', '\x1b[1;96m', '\x1b[1;97m', '\x1b[1;99m', '\x1b[1;100m', '\x1b[1;101m', '\x1b[1;102m', '\x1b[1;103m', '\x1b[1;104m', '\x1b[1;105m', '\x1b[1;106m', '\x1b[1;107m', '\x1b[1;109m']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

words = 'En un lugar de la mancha de cuyo nombre no quiero acordarme, no ha mucho tiempo vivia un hidalgo de los de lanza en astillero, adarga antigua, rocin flaco y galgo corredor.'
words = words.split(' ')

def x_random_letters(number=2):
    letters = ''
    for x in range(number):
        letters += random.choice(alphabet)
    return letters


def test():
    dataset = []
    # width = random.randint(0, 20)
    # color = random.choice(color_list)
    width = 10
    for x in range(10):
        # color = random.choice(color_list)
        # row_data_type = random.choice(['number', 'text'])
        row = []
        for y in range(width):
            color = random.choice(color_list)
            # field = color + x_random_letters(random.randint(0, 20))
            field = color + random.choice(words)
            row.append(field + '\x1b[0;39m')
        dataset.append(tuple(row))

    print(motor.render(dataset, width=False))


def test_oneline():
    # width = random.randint(0, 20)
    # color = random.choice(color_list)
    width = 10
    # row_data_type = random.choice(['number', 'text'])
    row = []
    for y in range(width):
        color = random.choice(color_list)
        # field = color + x_random_letters(random.randint(0, 20))
        field = color + random.choice(words)
        row.append(field + '\x1b[0;39m')

    print(motor_oneline.render(row, width=False))


def test_oneline_2(x):
    # width = random.randint(0, 20)
    # color = random.choice(color_list)
    width = 10
    # row_data_type = random.choice(['number', 'text'])
    row = []
    for y in range(width):
        # color = random.choice(color_list)
        # field = color + x_random_letters(random.randint(0, 20))
        # field = color + x * ' ' + '*' + (x - 1) * ' '
        field = x * ' ' + '*' + (x - 1) * ' '
        row.append(field + '\x1b[0;39m')

    print(motor_oneline.render(row, width=False))


def test_oneline_3(x=None):
    # width = random.randint(0, 20)
    # color = random.choice(color_list)
    width = 3
    # row_data_type = random.choice(['number', 'text'])
    row = []
    for y in range(width):
        if x == None:
            x = random.randint(0, 10)
        # color = random.choice(color_list)
        # field = color + x_random_letters(random.randint(0, 20))
        # field = color + x * ' ' + '*' + (x - 1) * ' '
        field = x * ' ' + '+' + (11 - x) * ' '
        # field = x * ' ' + str(x) + (11 - x) * ' '
        reversed_field = '\x1b[0;96m' + field[::-1] + '\x1b[0;39m'
        # field = field + reversed_field
        field = field + reversed_field
        #field = field[:x] + '*' + field[x + 1:]
        row.append(field + '\x1b[0;39m')

    sleep(0.03)
    print(motor_oneline.render(row, width=False))

def create_animation_list(lenght=20):
    animation_list = []
    for x in range(lenght):
        animation_list.append(random.randint(0, lenght / 2))
    return animation_list

if __name__ == '__main__':
    while True:
        '''
        for x in range(40):
            test()
        for x in range(320):
            test_oneline()
        '''
        # len(animation_list) --> 22
        # animation_list = [0, 3, 8, 25, 8, 10, 8, 2, 8, 2, 0, 0, 2, 8, 2, 8, 10, 8, 2, 8, 2, 0]
        # animation_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        '''
        animation_list = create_animation_list()
        for x in animation_list:
            test_oneline_3(x)
        '''
        # x = random.randint(0, 10)
        test_oneline_3()
    sys.exit(0)