"""
Set of helper methods that are used in multiple Atari games
"""


def _convert_number(number):
    """
    Almost every Atari Game displays the time/score in hexadecimal numbers, while the ram extraction
    displays it as an integer.
    This results in a required conversion from the extracted ram number (in dec) to a hex number, which we then display
    as a dec number.

    e.g.: game shows 10 seconds, but the ram display saves it as 16
    """
    number_str = str(hex(number))
    number_list = [*number_str]
    number_str = ""
    count = 0
    for x in number_list:
        if count > 1:
            number_str += x
        count += 1
    return int(number_str)


def number_to_bitfield(n):
    """
    Convert number to 8 bit bitfield.

    Games like SpaceInvaders or Breakout use the bit representation of the number in the RAM to display or not display
    the objects. In most cases a 1 means the objects is displayed and a 0 means the object is not displayed.
    In SpaceInvaders the bit sequence needs to be reversed.
    """
    lst = [1 if digit == '1' else 0 for digit in bin(n)[2:]]
    buffer = [0] * (8 - len(lst))
    buffer.extend(lst)
    return buffer


def bitfield_to_number(b, flip=False):
    """
    Convert Bitfield to a number.
    """
    exp = len(b)-1
    if flip:
        exp = 0
    res = 0
    for bit in b:
        if bit == 1:
            res = res + pow(2, exp)

        if flip:
            exp = exp + 1
        else:
            exp = exp - 1

    return res
