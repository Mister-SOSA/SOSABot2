""" Just a simple line counter that counts all the lines of code in the project. """

import os

FILE_EXTENSIONS = ['.py', '.json']

def get_lines():
    """ Gets the total number of lines in the project, optimized version. """
    total_lines = 0
    for root, _, files in os.walk('/home/ubuntu/SOSABot2'):
        for file in files:
            if file.endswith(tuple(FILE_EXTENSIONS)):
                with open(os.path.join(root, file), 'r') as f:
                    total_lines += sum(1 for _ in f)
    return total_lines
