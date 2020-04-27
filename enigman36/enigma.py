#!/usr/bin/env python3

"""enigma.py
   Author: Brian Jopling, April 2020
   Usage: enigma.py [-d ENCRYPTED_TEXT][-e TEXT_TO_ENCRYPT]
   Sample: ./enigma.py -e "RUBBERDUCK"
           ./enigma.py -d "RMFXSRLZMX"
"""

#############
#  IMPORTS  #
#############

import argparse
import sys


#############
#  GLOBALS  #
#############

PERMUTATOR_CONFIG_FILE = "permutator.config"
ROTOR_CONFIG_FILE = "rotor.config"

parser = argparse.ArgumentParser(description='Encrypt or decrypt using the Enigma Machine!')
IS_DEBUG = True

LEFT_WHEEL = "LEFT"
RIGHT_WHEEL = "RIGHT"
MIDDLE_WHEEL = "MIDDLE"

# Mapping of chars to integer values used for modular arithmetic of rotors.
CHAR_SET = {
    "A": {
        LEFT_WHEEL: "2",
        MIDDLE_WHEEL: "0",
        RIGHT_WHEEL: "3"
    },
    "B": {
        LEFT_WHEEL: "y",
        MIDDLE_WHEEL: "l",
        RIGHT_WHEEL: "5"
    },
    "C": {
        LEFT_WHEEL: "z",
        MIDDLE_WHEEL: "x",
        RIGHT_WHEEL: "h"
    },
    "D": {
        LEFT_WHEEL: "0",
        MIDDLE_WHEEL: "1",
        RIGHT_WHEEL: "e"
    },
    "E": {
        LEFT_WHEEL: "1",
        MIDDLE_WHEEL: "2",
        RIGHT_WHEEL: "f"
    },
    "F": {
        LEFT_WHEEL: "a",
        MIDDLE_WHEEL: "8",
        RIGHT_WHEEL: "g"
    },
    "G": {
        LEFT_WHEEL: "w",
        MIDDLE_WHEEL: "h",
        RIGHT_WHEEL: "d"
    },
    "H": {
        LEFT_WHEEL: "i",
        MIDDLE_WHEEL: "b",
        RIGHT_WHEEL: "q"
    },
    "I": {
        LEFT_WHEEL: "p",
        MIDDLE_WHEEL: "3",
        RIGHT_WHEEL: "8"
    },
    "J": {
        LEFT_WHEEL: "k",
        MIDDLE_WHEEL: "n",
        RIGHT_WHEEL: "m"
    },
    "K": {
        LEFT_WHEEL: "s",
        MIDDLE_WHEEL: "r",
        RIGHT_WHEEL: "2"
    },
    "L": {
        LEFT_WHEEL: "n",
        MIDDLE_WHEEL: "o",
        RIGHT_WHEEL: "k"
    },
    "M": {
        LEFT_WHEEL: "3",
        MIDDLE_WHEEL: "k",
        RIGHT_WHEEL: "l"
    },
    "N": {
        LEFT_WHEEL: "t",
        MIDDLE_WHEEL: "d",
        RIGHT_WHEEL: "j"
    },
    "O": {
        LEFT_WHEEL: "e",
        MIDDLE_WHEEL: "t",
        RIGHT_WHEEL: "n"
    },
    "P": {
        LEFT_WHEEL: "r",
        MIDDLE_WHEEL: "7",
        RIGHT_WHEEL: "s"
    },
    "Q": {
        LEFT_WHEEL: "m",
        MIDDLE_WHEEL: "c",
        RIGHT_WHEEL: "u"
    },
    "R": {
        LEFT_WHEEL: "u",
        MIDDLE_WHEEL: "6",
        RIGHT_WHEEL: "w"
    },
    "S": {
        LEFT_WHEEL: "c",
        MIDDLE_WHEEL: "p",
        RIGHT_WHEEL: "o"
    },
    "T": {
        LEFT_WHEEL: "5",
        MIDDLE_WHEEL: "i",
        RIGHT_WHEEL: "v"
    },
    "U": {
        LEFT_WHEEL: "v",
        MIDDLE_WHEEL: "v",
        RIGHT_WHEEL: "r"
    },
    "V": {
        LEFT_WHEEL: "6",
        MIDDLE_WHEEL: "j",
        RIGHT_WHEEL: "x"
    },
    "W": {
        LEFT_WHEEL: "x",
        MIDDLE_WHEEL: "4",
        RIGHT_WHEEL: "z"
    },
    "X": {
        LEFT_WHEEL: "7",
        MIDDLE_WHEEL: "a",
        RIGHT_WHEEL: "c"
    },
    "Y": {
        LEFT_WHEEL: "f",
        MIDDLE_WHEEL: "u",
        RIGHT_WHEEL: "i"
    },
    "Z": {
        LEFT_WHEEL: "q",
        MIDDLE_WHEEL: "w",
        RIGHT_WHEEL: "9"
    },
    "0": {
        LEFT_WHEEL: "o",
        MIDDLE_WHEEL: "m",
        RIGHT_WHEEL: "t"
    },
    "1": {
        LEFT_WHEEL: "l",
        MIDDLE_WHEEL: "e",
        RIGHT_WHEEL: "7"
    },
    "2": {
        LEFT_WHEEL: "4",
        MIDDLE_WHEEL: "9",
        RIGHT_WHEEL: "b"
    },
    "3": {
        LEFT_WHEEL: "8",
        MIDDLE_WHEEL: "5",
        RIGHT_WHEEL: "p"
    },
    "4": {
        LEFT_WHEEL: "g",
        MIDDLE_WHEEL: "q",
        RIGHT_WHEEL: "a"
    },
    "5": {
        LEFT_WHEEL: "d",
        MIDDLE_WHEEL: "s",
        RIGHT_WHEEL: "0"
    },
    "6": {
        LEFT_WHEEL: "9",
        MIDDLE_WHEEL: "z",
        RIGHT_WHEEL: "1"
    },
    "7": {
        LEFT_WHEEL: "b",
        MIDDLE_WHEEL: "g",
        RIGHT_WHEEL: "y"
    },
    "8": {
        LEFT_WHEEL: "j",
        MIDDLE_WHEEL: "y",
        RIGHT_WHEEL: "6"
    },
    "9": {
        LEFT_WHEEL: "h",
        MIDDLE_WHEEL: "f",
        RIGHT_WHEEL: "4"
    }
}

#############
#  CLASSES  #
#############


class Wheel:
    # Class Vars
    #  - cursor  :  current index of wheel, mapped in CHAR_SET
    #  - name    :  identifier of wheel - LEFT, RIGHT, or MIDDLE

    def __init__(self, name, starting_value):
        print_debug("Init %s wheel at %s" % (name, starting_value))
        self.cursor = CHAR_SET[starting_value]
        self.name = name

    def iterate(self):
        # DEPRECATED impl, TODO cleanup
        # Check if we're at the last value and need to go back to 0
        if self.cursor == CHAR_SET.keys()[-1]:
            self.cursor = 1
        else:
            self.cursor += 1

    def lookup(self, char):
        # Wheels turn first, then the substitution occurs.
        # self.iterate()
        val = CHAR_SET[char][self.name].upper()
        return val


#############
# FUNCTIONS #
#############


def main(args):
    permutation, rotor_config = read_config_files()
    wheels = init_wheels(rotor_config)
    if args['decrypt']:
        decrypt(args['decrypt'].upper(), permutation, wheels)
    else:
        encrypt(args['encrypt'].upper(), permutation, wheels)


def decrypt(ciphertext, permutation, wheels):
    print_debug("Decrypting %s" % ciphertext)
    transposed_plaintext = ""
    for i in ciphertext:
        transposed_plaintext += wheels[2].lookup(wheels[1].lookup(wheels[0].lookup(i)))
    print_debug("Transposed as %s using %s" % (transposed_plaintext, permutation))
    plaintext = transpose(transposed_plaintext, permutation)
    print("Decrypted %s: %s" % (ciphertext, plaintext))


def encrypt(plaintext, permutation, wheels):
    print_debug("Encrypting %s" % plaintext)
    transposed_text = transpose(plaintext, permutation)
    print_debug("Transposed as %s using %s" % (transposed_text, permutation))
    encrypted_text = ""
    for i in transposed_text:
        encrypted_text += wheels[0].lookup(wheels[1].lookup(wheels[2].lookup(i)))
    print("Encrypted %s: %s" % (plaintext, encrypted_text))


def init_wheels(rotor_config):
    return [Wheel(LEFT_WHEEL, rotor_config[0]),
            Wheel(MIDDLE_WHEEL, rotor_config[1]),
            Wheel(RIGHT_WHEEL, rotor_config[2])]


def transpose(text, permutation):
    transposed_text = ""
    for i in permutation:
        transposed_text += text[int(i)]
    return transposed_text


def read_config_files():
    with open(PERMUTATOR_CONFIG_FILE) as file:
        permutation = file.read()
        file.close()
    with open(ROTOR_CONFIG_FILE) as file:
        rotor_config = file.read()
        file.close()
    return permutation, rotor_config


def usage():
    parser.print_help()


def error_quit(msg, code):
    """Prints out an error message, the program usage, and terminates with an
       error code of `code`."""
    print("\n[!] %s" % msg)
    usage()
    sys.exit(code)


def print_debug(msg):
    """Prints if we are in debug mode."""
    if IS_DEBUG:
        print(msg)


#############
#  PROCESS  #
#############


if __name__ == '__main__':
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--decrypt', help='decrypt specified ciphertext')
    group.add_argument('-e', '--encrypt', help='encrypt specified string')
    args = vars(parser.parse_args())
    main(args)
