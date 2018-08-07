#!/usr/bin/python3

def ParseYorN(_input):
    """ Outputs a bool, True if
        user has answered Yes.
    """
    correct = False
    while not correct:
        _input = _input.lower()
        _input = _input.strip()
        if _input == "n":
            result = False
            correct = True
        elif _input == "y":
            result = True
            correct = True
        else:
            _input = input("Incorrect Input, please use Y or N: ")
            
    return result