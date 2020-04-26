# EnigmaN36

Brian Jopling, April 2020

### Description:

An implementation of the 1930s Enigma Machine, utilizing both letters and 
numbers (36 possible characters instead of 26). Written in `python3`.

Notable differences include:

1. A _permutator_ is used instead of a plugboard.
   - Permutator is configured with 10 digits, 0123456789, transposed.
   - Input, processed 10 characters at a time, is permutated based on the 
   initial configuration and its corresponding indices.
   - e.g. If the initial configuration of the permutator is 3145692870 and 
   the input is "RUBBERDUCK", the permutator returns "BUERDKBCUR".

2. Consequently, no reflector is used. The output of the left-most wheel is 
   treated as the output of the substitution stage.
   
3. Rather than iterate the left and middle wheels based on 360 degree turns 
   of the wheel to their right, the wheels will adhere to the following:
   - The right-most wheel turns for each character typed (like the real Enigma
   Machine).
   - The middle wheel turns for every seven characters typed.
   - The left-most wheel turns for every five characters typed.
   
4. As stated in the description, both letters and numbers are viable for input 
   and encrypted output, unlike the real Enigma Machine.

### Usage:

1. Populate `permutator.config` with the initial 10-digit permutation 
   configuration.

    e.g. `echo "5463720819" > permutator.config`


2. Populate `rotor.config` with an initial mapping of wheel rotations and 
   their corresponding characters.


3. Encrypt a message with `engima.py`.

    e.g. `python3 enigma.py -e "RUBBERDUCK"`

4. Decrypt a message with `enigma.py`.

    e.g. `python3 enigma.py -d "BERGMSGQ3T`


### Encryption flow

1. Inputted text is passed, 10 characters at a time, to the permutator.
2. The permutator transposes the inputted text based on the 10-digit string 
provided in `permutator.config`.
3. The 10-character permutation is passed to the rotors, starting from the 
right-most wheel and ending at the left-most wheel. Each wheel substitutes 
each character of the inputted text based on the mapping of `rotor.config`.
4. The final output is the encrypted string.


### Decryption flow

1. Inputted encrypted text is passed to the rotors, starting from the 
left-most wheel and ending at the right-most wheel. Each wheel substitutes 
each character of the inputted text based on the mapping of `rotor.config`.
2. The output of the left-most wheel is passed, 10 characters at a time, to 
the permutator.
3. The permutator transposes the inputted text based on the 10-digit string 
provided in `permutator.config`.
4. The final output is the decrypted string.


