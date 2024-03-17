""" This file includes utility functions for server and client.
"""
import argparse
from effect.do import do
from effect import Effect, sync_perform, sync_performer
from effect import ComposedDispatcher, TypeDispatcher, base_dispatcher

def within_range(lower, upper, value):
    """ Parameters: lower: An integer value.
                    upper: An integer value.
                    value: A string of an integer value.
        Return: Boolean of whether value is within the 
        range [lower, upper)
        
        This function checks whether value is with the range of 
        [lower, upper).
    """
    try:
        v = int(value)
    except ValueError:
        return Effect(Intent(ValueError("Value is not an integer.")))
    if lower <= v < upper:
        return Effect(Intent(v))
    else:
        return Effect(Intent(ValueError("Value is not within range.")))

class Intent(object):
    def __init__(self, thing):
        self.thing = thing

#NOTE TO SELF: This perform function can be expanded as need.
#I doubt there will be a need to however.
@sync_performer
def perform_intent(dispatcher, intent):
    """
    """
    if isinstance(intent.thing, BaseException):
        raise intent.thing
    return intent.thing

DISPATCHER = ComposedDispatcher([TypeDispatcher({
    Intent: perform_intent
}), base_dispatcher])

def process_args():
    """ Parameters: None
        Returns: An argparse.Namespace object of arguments.

        This function reads in arguments and returns them.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "shift",
        type=lambda s: sync_perform(DISPATCHER, within_range(0, 26, s)),
        help=("An integer of the amount to shift alphabet by. "
              "This value must be in the range [0...26)")
    )
    return parser.parse_args()

def char_mapping(char, shift, run_encryption):
    """ Parameters: char: String of a single character.
                    shift: Integer of the amount to shift alphabet by.
                    run_encryption: Boolean of whether to run encryption
                    or not.
        Return: The corresponding encrypted or decrypted character.
        
        This function maps between characters for the caesar cipher.
    """
    alphabet_size = 26
    if not char.isalpha():
        return char
    start_letter = "A" if char.isupper() else "a"
    right_shift = 1 if run_encryption else -1
    return chr((ord(char) - ord(start_letter) + (shift * right_shift)) %
                alphabet_size + ord(start_letter))

def encrypt(plaintext, shift):
    """ Parameters: plaintext: String of plaintext.
                    shift: Integer of the amount to shift alphabet by.
        Return: String of ciphertext.

        This function takes in a string and a shift and outputs the 
        corresponding ciphertext.
    """
    return "".join([char_mapping(char, shift, True) for char in plaintext])

def decrypt(ciphertext, shift):
    """ Parameters: ciphertext: String of ciphertext.
                    shift: Integer of the amount to shift alphabet by.
        Return: String of plaintext.

        This function takes in a string and a shift and outputs the 
        corresponding plaintext.
    """
    return "".join([char_mapping(char, shift, False) for char in ciphertext])
