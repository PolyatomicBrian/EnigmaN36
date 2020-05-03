#!/usr/bin/env python3

"""enigma.py
   Author: Brian Jopling, April 2020
   Usage: enigma.py [-d ENCRYPTED_TEXT][-e TEXT_TO_ENCRYPT]
   Sample: ./enigma.py -e "RUBBERDUCK"
           ./enigma.py -d "CGN5DPXHLP"
   Prerequisites:
     1. File "rotor.config" must exist and contain a 3 character string.
     2. File "permutator.config" must exist and contain a permutation of digits 0-9.
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

parser = argparse.ArgumentParser(description='Encrypt or decrypt using the EnigmaN36 Machine!')
IS_DEBUG = True

LEFT_WHEEL = "LEFT"
RIGHT_WHEEL = "RIGHT"
MIDDLE_WHEEL = "MIDDLE"

WIRE_MAPPING = {
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

# Populated via init
# Will contain a lookup of character to index, i.e.
#  {"A" : 1, "B": 2, "C": 3, ... }
CHAR_SET = {

}

#############
#  CLASSES  #
#############


class Wheel:
    # Class Vars
    #  - cursor     :  current index of wheel, mapped in WIRE_MAPPING
    #  - name       :  identifier of wheel - LEFT, RIGHT, or MIDDLE
    #  - prev_wheel :  Wheel object of the wheel that's to the right of curr wheel.
    #  - key_count  :  Number of times a key has been pressed.

    def __init__(self, name, starting_value, prev_wheel=None):
        print_debug("Init %s wheel at %s" % (name, starting_value))
        self.cursor = starting_value
        self.name = name
        self.prev_wheel = prev_wheel
        self.key_count = 0

    def iterate(self):
        self.key_count += 1
        # Right: Rotates for each key press.
        # Middle: Rotates for every 7 key presses.
        # Left: Rotates for every 5 key presses.
        if self.name == RIGHT_WHEEL:
            self.do_rotate()
        elif self.name == MIDDLE_WHEEL and self.key_count % 7 == 0:
            self.do_rotate()
        elif self.name == LEFT_WHEEL and self.key_count % 5 == 0:
            self.do_rotate()

    def do_rotate(self):
        # Check if we're at the last numeric value and need to go back to alpha A.
        if self.cursor == '9':
            print_debug("\tRotating %s from %s to %s" % (self.name, self.cursor, "A"))
            self.cursor = 'A'
        # Check if we're at the last alpha value and need to go to numeric 0.
        elif self.cursor == 'Z':
            print_debug("\tRotating %s from %s to %s" % (self.name, self.cursor, "0"))
            self.cursor = '0'
        else:
            print_debug("\tRotating %s from %s to %s" %
                        (self.name, self.cursor, chr(ord(self.cursor) + 1)))
            self.cursor = chr(ord(self.cursor) + 1)

    def encrypt(self, char):
        if self.prev_wheel is not None:
            # Offset = Current Rotor Value offset from A - the previous Rotor Value offset from A.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A") - self.char_to_index(self.prev_wheel.cursor) - self.char_to_index("A")
        else:
            # No previous wheel, so offset is just current rotor value offset from A.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A")
        # Shift the char by the offset calculated above.
        shifted_char = self.index_to_char((self.char_to_index(char) + amount_to_shift) % len(CHAR_SET))
        val = WIRE_MAPPING[shifted_char][self.name].upper()
        print_debug("\t\t%s: Shifted %s by %s to %s and encrypted as %s" %
                    (self.name, char, str(amount_to_shift), shifted_char, val))
        if self.name == LEFT_WHEEL:
            # Lastly, "normalize" output of the left (final) wheel relative to the default
            #   charset to account for the rotation of the wheel.
            # If the wheel was at B (offset of 1), and the value obtained from the left wheel was F, then
            # F is offset by 1 and this needs to be undone to normalize the value. So F becomes E.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A")
            val_final = self.index_to_char((self.char_to_index(val) - amount_to_shift) % len(CHAR_SET))
            print_debug("\t\t%s Final mapping: Shifted %s by %s to %s.\nEncrypted as %s" %
                        (self.name, val, str(amount_to_shift), val_final, val_final))
            val = val_final
        return val

    def decrypt(self, char):
        if self.prev_wheel is not None:
            # Offset = Current Rotor Value offset from A - the previous Rotor Value offset from A.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A") - self.char_to_index(self.prev_wheel.cursor) - self.char_to_index("A")
        else:
            # No previous wheel, so offset is just current rotor value offset from A.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A")
        # Shift the char by the offset calculated above.
        shifted_char = self.index_to_char((self.char_to_index(char) + amount_to_shift) % len(CHAR_SET))
        decrypted = self.decrypt_char(shifted_char)
        print_debug("\t\t%s: Shifted %s by %s to %s and decrypted as %s" %
                    (self.name, char, str(amount_to_shift), shifted_char, decrypted))
        if self.name == RIGHT_WHEEL:
            # Lastly, "normalize" output of the right (final) wheel relative to the default
            #   charset to account for the rotation of the wheel.
            # If the wheel was at B (offset of 1), and the value obtained from the right wheel was F, then
            # F is offset by 1 and this needs to be undone to normalize the value. So F becomes E.
            amount_to_shift = self.char_to_index(self.cursor) - self.char_to_index("A")
            val_final = self.index_to_char((self.char_to_index(decrypted) - amount_to_shift) % len(CHAR_SET))
            print_debug("\t\t%s Final mapping: Shifted %s by %s to %s.\nEncrypted as %s" %
                        (self.name, decrypted, str(amount_to_shift), val_final, val_final))
            decrypted = val_final
        return decrypted

    def index_to_char(self, index):
        return list(CHAR_SET.keys())[list(CHAR_SET.values()).index(index)]

    def char_to_index(self, char):
        return CHAR_SET[char.upper()]

    def decrypt_char(self, char):
        """Performs a reverse lookup of a nested dictionary value to get its
           key. The key in this case is the reverse lookup of the char-to-decrypt
           using the table defined in WIRE_MAPPING"""
        for outer in WIRE_MAPPING:
            for inner in WIRE_MAPPING[outer]:
                iter_char = WIRE_MAPPING[outer][inner]
                if inner == self.name and iter_char.upper() == char.upper():
                    decrypted = outer
                    return decrypted

#############
# FUNCTIONS #
#############


def main(args):
    populate_char_set()
    permutation, rotor_config = read_config_files()
    if args['decrypt']:
        wheels = init_wheels(rotor_config, 'd')
        decrypt(args['decrypt'].upper(), permutation, wheels)
    else:
        wheels = init_wheels(rotor_config, 'e')
        encrypt(args['encrypt'].upper(), permutation, wheels)


def decrypt(ciphertext, permutation, wheels):
    print_debug("Decrypting %s" % ciphertext)
    plaintext = ""
    if len(ciphertext) % len(permutation) != 0:  # len(permutator) is the size of the permutator's config string.
        error_quit("Your ciphertext is not divisible by %d! Did you encrypt properly?" % len(permutation), 400)
    # Iterate over string in increments of the size of the permutator config (10).
    for i in range(0, len(ciphertext), len(permutation)):
        cur_chars = ciphertext[i:i + len(permutation)]
        print_debug("Operating on group of ten chars: %s" % cur_chars)
        transposed_plaintext = ""
        # Use permutator to transpose text.
        for t in cur_chars:
            turn_wheels(wheels)
            transposed_plaintext += wheels[2].decrypt(wheels[1].decrypt(wheels[0].decrypt(t)))
        print_debug("Transposed as %s" % transposed_plaintext)
        plaintext += undo_transpose(transposed_plaintext, permutation)
        print_debug("Undid transposition of %s to %s using %s" % (transposed_plaintext,
                                                                  plaintext[i:i+len(permutation)],
                                                                  permutation))
    print("Decrypted %s: %s" % (ciphertext, plaintext))


def encrypt(plaintext, permutation, wheels):
    print_debug("Encrypting user input %s" % plaintext)
    num_pad = -len(plaintext) % len(permutation)  # Get the number of "X"es
                                                  # required to pad the string
                                                  # it's equal to the size of
                                                  # the permutator's config.
    padded_text = plaintext + "X" * num_pad
    print_debug("Padding %s as %s" % (plaintext, padded_text))
    encrypted_text = ""
    # Iterate over string in increments of the size of the permutator config (10).
    for i in range(0, len(padded_text), len(permutation)):
        cur_chars = padded_text[i:i + len(permutation)]
        print_debug("Operating on group of ten chars: %s" % cur_chars)
        # Use permutator to transpose text.
        transposed_text = transpose(cur_chars, permutation)
        print_debug("Transposed as %s using %s" % (transposed_text, permutation))
        # Type each key individually, which rotates the wheels and encrypts them one-by-one.
        for t in transposed_text:
            turn_wheels(wheels)
            encrypted_text += wheels[0].encrypt(wheels[1].encrypt(wheels[2].encrypt(t)))
    if num_pad == 0:
        print("Encrypted %s: %s" % (plaintext, encrypted_text))
    else:
        print("Encrypted %s (padded as %s): %s" % (plaintext, padded_text, encrypted_text))


def init_wheels(rotor_config, mode):
    if mode == 'e':
        right = Wheel(RIGHT_WHEEL, rotor_config[2])
        mid = Wheel(MIDDLE_WHEEL, rotor_config[1], right)
        left = Wheel(LEFT_WHEEL, rotor_config[0], mid)
    else:
        left = Wheel(LEFT_WHEEL, rotor_config[0])
        mid = Wheel(MIDDLE_WHEEL, rotor_config[1], left)
        right = Wheel(RIGHT_WHEEL, rotor_config[2], mid)
    return [left, mid, right]


def turn_wheels(wheels):
    for w in wheels:
        w.iterate()


def transpose(text, permutation):
    transposed_text = ""
    for i in permutation:
        transposed_text += text[int(i)]
    return transposed_text


def undo_transpose(text, permutation):
    untransposed_text = ""
    for i in range(0, len(permutation)):
        index = permutation.index(str(i))
        untransposed_text += text[index]
    return untransposed_text


def read_config_files():
    with open(PERMUTATOR_CONFIG_FILE) as file:
        permutation = file.read()
        file.close()
    with open(ROTOR_CONFIG_FILE) as file:
        rotor_config = file.read()
        file.close()
    return permutation, rotor_config


def populate_char_set():
    """Populates global variable CHAR_SET with the following mapping definition:
       CHAR_SET = { "A": 0, "B": 1, "C": 2, ... "8": 35, "9": 36 }"""
    global CHAR_SET
    # First populate letters A through Z
    for i in range(0, 26):
        CHAR_SET[chr(ord('A') + i)] = i
    size = len(CHAR_SET)
    # Then populate numbers 0 to 9
    for i in range(0, 10):
        CHAR_SET[str(i)] = size + i
    print_debug("Init CHAR_SET as %s" % str(CHAR_SET))


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
