#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 2023

@author: iluzioDev

This script implements a generator for GPS-L1C/A Codes.
"""
import re
import lfsr

from colorama import Fore

ROW = '■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■'

G2_TAPS = ['2&6', '3&7', '4&8', '5&9', '1&9', '2&10', '1&8', '2&9', '3&10', '2&3', '3&4', '5&6', '6&7', '7&8', '8&9',
           '9&10', '1&4', '2&5', '3&6', '4&7', '5&8', '6&9', '1&3', '4&6', '5&7', '6&8', '7&9', '8&10', '1&6', '2&7', '3&8', '4&9']

def highlight_bits(sequence, polynomial, color, taps = False):
  """Highlights the bits of a given sequence according to a given polynomial.

  Args:
      sequence (str | list): Sequence to be highlighted.
      polynomial (list): Polynomial to be used in order to highlight the sequence. If taps is True, this parameter must be taps exponents.
      color (str): Color to be used in order to highlight the sequence. 
      taps (bool, optional): Indicates if polynomial is taps or not. Defaults to False.

  Returns:
      None | str: None if the parameters are invalid, otherwise the highlighted sequence.
  """
  if type(sequence) is str:
    sequence = [x for x in sequence]

  if type(sequence) is not list or type(polynomial) is not list or type(color) is not str:
    return None

  if not taps:
    if polynomial[0]:
      for i in polynomial[1:]:
        sequence[int(i) - 1] = color + sequence[int(i) - 1] + Fore.RESET
    else:
      for i in polynomial[1:]:
        sequence[len(sequence) - int(i)] = color + sequence[len(sequence) - int(i)] + Fore.RESET
  else:
    for i in polynomial:
      sequence[int(i) - 1] = color + sequence[int(i) - 1] + Fore.RESET
  return sequence

def colorize_sequence(sequence, polynomial, color, taps = None):
  """Colors a given sequence according to a given polynomial.

  Args:
      sequence (str): Sequence to be colorized.
      polynomial (list): Polynomial to be used in order to colorize the sequence.
      color (str): Color to be used.
      taps (list, optional): Taps digits to highlight. Defaults to None.

  Returns:
      None | str: None if the parameters are invalid, otherwise the colorized sequence.
  """
  if type(sequence) is not str or type(polynomial) is not list or type(color) is not str:
    return None

  if taps:
    sequence = highlight_bits([x for x in sequence], taps, Fore.YELLOW, True)
  sequence = highlight_bits([x for x in sequence], polynomial, color)
  
  return  ''.join(sequence)

def initialize_values(g1_pol, g2_pol):
  """Initializes the values of the generator.

  Args:
      g1_pol (str): G1 polynomial.
      g2_pol (str): G2 polynomial.

  Returns:
      str, str, str, list, list: CA sequence, G1 sequence, G2 sequence, G1 polynomial, G2 polynomial. 
  """
  ca_sequence = ''
  G1 = G2 = '1' * 10
  return ca_sequence, G1, G2, lfsr.str_to_polynomial(g1_pol), lfsr.str_to_polynomial(g2_pol)

def set_polynomial(polynomial):
  """Sets a new polynomial.

  Args:
      polynomial (str): Polynomial to be set.

  Returns:
      str: New polynomial.
  """
  new_pol = input('Introduce new polynomial -> ')
  new_pol = lfsr.str_to_polynomial(new_pol)
  if new_pol == None:
    print(ROW)
    print('Invalid polynomial!')
  else:
    polynomial = lfsr.polynomial_to_str(new_pol)
  return polynomial

def GPS_L1CA_generator(prn_id, n, g1_pol, g2_pol):
  """Generates a GPS-L1C/A code given a PRN ID, a number of bits to generate and the G1 and G2 polynomials.

  Args:
      prn_id (int | str): PRN ID to use.
      n (int | str): Number of bits to generate.
      g1_pol (str): G1 polynomial.
      g2_pol (str): G2 polynomial.

  Returns:
      None | str: None if the parameters are invalid, otherwise the generated code.
  """
  if type(prn_id) is str:
    prn_id = int(prn_id)
    
  if type(n) is str:
    n = int(n)
  
  if (type(prn_id) is not int or type(n) is not int) or (prn_id not in range(1, 33) or n <= 0):
    return None
  
  ca_sequence, G1, G2, g1_pol, g2_pol = initialize_values(g1_pol, g2_pol)

  print('■ G1\t\tFB1\tG2\t\tFB2\tCA\t\t■')
  print(ROW)
  for i in range(n):
    taps = G2_TAPS[prn_id - 1].split('&')
    taps_xor = int(G2[int(taps[0]) - 1]) ^ int(G2[int(taps[1]) - 1])
    if g1_pol[0]:
      ca_code = str(int(G1[len(G1) - 1]) ^ taps_xor)
    else:
      ca_code = str(int(G1[0]) ^ taps_xor)
    ca_sequence += ca_code

    new_G1, feedback1 = lfsr.shift(G1, g1_pol)
    new_G2, feedback2 = lfsr.shift(G2, g2_pol)
    
    G1, G2 = colorize_sequence(G1, g1_pol, Fore.BLUE), colorize_sequence(G2, g2_pol, Fore.BLUE, taps)
    
    print('■ ' + G1 + '\t' + feedback1 + '\t' + G2 +
          '\t' + feedback2 + '\t' + Fore.GREEN + ca_code + Fore.RESET + '\t\t■')

    G1, G2 = new_G1, new_G2

  return ca_sequence

def main():
  """Main function of the program. Users can choose between generating a GPS L1C/A code or checking G2 taps by prn id.
  """
  g1_pol = '1 + x3 + x10'
  g2_pol = '1 + x2 + x3 + x6 + x8 + x9 + x10'
  while True:
    print(ROW)
    print('■         WELCOME TO THE GPS L1C/A CODE GENERATOR!              ■')
    print(ROW)
    print('It is quite simple to use this program, just input a pseudorandom')
    print('noise (prn) id, it must be a number between 1 and 32, and the')
    print('number of bits you want to generate (positive integer).')
    print(ROW)
    print('What do you want to do?')
    print('[1] Generate GPS L1C/A Code.')
    print('[2] Check G2 Taps by prn id.')
    print('[3] Check G1 and G2 polynomials.')
    print('[4] Change G1 polynomial.')
    print('[5] Change G2 polynomial.')
    print('[0] Exit.')
    print(ROW)
    option = input('Option  ->  ')
    print(ROW)

    if int(option) not in range(6):
      print('Invalid option!')
      continue

    if option == '0':
      print('See you soon!')
      print(ROW)
      break

    if option == '1':
      prn_id = input('Introduce a prn id (1-32) -> ')
      print(ROW)
      n = input('Introduce number of bits to generate -> ')
      print(ROW)
      gps_l1ca_code = GPS_L1CA_generator(prn_id, n, g1_pol, g2_pol)
      print(ROW)
      print('\t\tGPS L1C/A Code:', Fore.GREEN + gps_l1ca_code + Fore.RESET)

    if option == '2':
      print('■                          G2 TAPS                              ■')
      print(ROW)
      print('|                                                               |')
      for i in range(1, (len(G2_TAPS) / 2) + 1):
        print('|\tPRN ID: ' + str(i) + ' -> ' +
              G2_TAPS[i - 1] + '\t\tPRN ID: ' + str(i + (len(G2_TAPS) / 2)) + ' -> ' + G2_TAPS[(len(G2_TAPS) / 2) - 1] + '\t|')
      print('|                                                               |')
      
    if option == '3':
      print('G1 polynomial: ' + lfsr.polynomial_to_str(lfsr.str_to_polynomial(g1_pol)))
      print('G2 polynomial: ' + lfsr.polynomial_to_str(lfsr.str_to_polynomial(g2_pol)))
      
    if option == '4':
      g1_pol = set_polynomial(g1_pol)
    
    if option == '5':
      g2_pol = set_polynomial(g2_pol)
      
  return

if __name__ == '__main__':
  main()
