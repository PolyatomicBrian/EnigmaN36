# EnigmaN36

Brian Jopling, April 2020

### Description:

An implementation of the 1930s Enigma Machine, with some twists,
including the utilization of both letters and numbers (36 possible 
characters instead of 26). Written in `python3`.

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


2. Populate `rotor.config` with a 3-character string pertaining to the initial 
   values of the wheels.

   e.g. `echo "BRJ" > rotor.config` corresponds to:

    - Left Wheel starting at "B"

    - Middle Wheel starting at "R"

    - Right Wheel starting at "J"


3. Encrypt a message with `engima.py`.

    e.g. `python3 enigma.py -e "RUBBERDUCK"`

4. Decrypt a message with `enigma.py`.

    e.g. `python3 enigma.py -d "20ULMP7C4Y"`




