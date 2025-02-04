import random


with open('instructions_test.txt', 'w') as file:
    for _ in range(100):
        valid_op_codes = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
        signs = ['+', '-']

        sign = random.randint(0, 1)
        x = random.randint(0, len(valid_op_codes)-1)
        y = random.randint(0, 99)

        file.write(signs[sign] + str((valid_op_codes[x]*100) + y) + '\n')

    
