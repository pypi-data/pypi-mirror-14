#!/usr/bin/env python3

import outfancy
import random
import sys
import datetime

motor = outfancy.render.Oneline()

color_list = ['\x1b[0;30m', '\x1b[0;31m', '\x1b[0;32m', '\x1b[0;33m', '\x1b[0;34m', '\x1b[0;35m', '\x1b[0;36m', '\x1b[0;37m', '\x1b[0;39m', '\x1b[0;40m', '\x1b[0;41m', '\x1b[0;42m', '\x1b[0;43m', '\x1b[0;44m', '\x1b[0;45m', '\x1b[0;46m', '\x1b[0;47m', '\x1b[0;49m', '\x1b[0;90m', '\x1b[0;91m', '\x1b[0;92m', '\x1b[0;93m', '\x1b[0;94m', '\x1b[0;95m', '\x1b[0;96m', '\x1b[0;97m', '\x1b[0;99m', '\x1b[0;100m', '\x1b[0;101m', '\x1b[0;102m', '\x1b[0;103m', '\x1b[0;104m', '\x1b[0;105m', '\x1b[0;106m', '\x1b[0;107m', '\x1b[0;109m', '\x1b[1;30m', '\x1b[1;31m', '\x1b[1;32m', '\x1b[1;33m', '\x1b[1;34m', '\x1b[1;35m', '\x1b[1;36m', '\x1b[1;37m', '\x1b[1;39m', '\x1b[1;40m', '\x1b[1;41m', '\x1b[1;42m', '\x1b[1;43m', '\x1b[1;44m', '\x1b[1;45m', '\x1b[1;46m', '\x1b[1;47m', '\x1b[1;49m', '\x1b[1;90m', '\x1b[1;91m', '\x1b[1;92m', '\x1b[1;93m', '\x1b[1;94m', '\x1b[1;95m', '\x1b[1;96m', '\x1b[1;97m', '\x1b[1;99m', '\x1b[1;100m', '\x1b[1;101m', '\x1b[1;102m', '\x1b[1;103m', '\x1b[1;104m', '\x1b[1;105m', '\x1b[1;106m', '\x1b[1;107m', '\x1b[1;109m']

words = 'En un lugar de la mancha de cuyo nombre no quiero acordarme, no ha mucho tiempo vivia un hidalgo de los de lanza en astillero, adarga antigua, rocin flaco y galgo corredor.'
words = words.split(' ')

def test():
    dataset = []
    width = random.randint(1, 10)
    for x in range(1):
        color = random.choice(color_list)
        row_data_type = random.choice(['number', 'text'])
        row = []
        for y in range(width):
            field = color + random.choice(words)
            row.append(field)
        dataset.append(tuple(row))

    print(motor.render(dataset))
    ya = datetime.datetime.now()
    print(ya.second)


if __name__ == '__main__':
    ciclo = 0
    while True:
        test()
        print(ciclo)
        ciclo += 1
    sys.exit(0)