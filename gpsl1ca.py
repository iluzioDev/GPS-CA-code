#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 2023

@author: iluzioDev

This script implements a generator for GPS-L1C/A Codes.
"""
import re

pp_regex = '^1(\+x([0-9]+)?)+$'

G2_taps = ['2&6', '3&7', '4&8', '5&9', '1&9', '2&10', '1&8', '2&9', '3&10', '2&3', '3&4', '5&6', '6&7', '7&8', '8&9',
           '9&10', '1&4', '2&5', '3&6', '4&7', '5&8', '6&9', '1&3', '4&6', '5&7', '6&8', '7&9', '8&10', '1&6', '2&7', '3&8', '4&9']

def LFSR(sequence, polynomial):
  """Makes a Linear Feedback Shift Register (LFSR) operation in a given sequence.

  Args:
      sequence (str): Sequence to be shifted.
      polynomial (str): Primative polynomial to be used in the operation.

  Returns:
      str | None: Shifted sequence in success, None in failure.
  """
  if type(sequence) is not str or type(polynomial) is not str:
    return None

  polynomial = re.search(pp_regex, polynomial.replace(' ', ''))
  if polynomial == None:
    return None

  polynomial = polynomial.string.split('+')

  feedback = 0
  for j in polynomial:
    if 'x' in j:
      feedback ^= int(sequence[int(j[1:]) - 1], 2)
  sequence = bin(feedback)[-1] + sequence[:-1]
  return sequence, bin(feedback)[-1]

def GPS_L1CA_generator(prn_id, n):
  """Generates a GPS L1C/A code using a specific prn id and a given number of bits to generate.

  Args:
      prn_id (int): Pseudo-random noise id of satellite.
      n (int): Number of bits to generate.

  Returns:
      str | None: Generated code in success, None in failure.
  """
  if (type(prn_id) is not int or type(n) is not int) or (prn_id not in range(1, 33) or n <= 0):
    return None
  
  ca_sequence = ''
  G1 = G2 = '1' * 10

  print('■ G1\t\tXOR\tG2\t\tXOR\tCA\t\t■')
  print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
  for i in range(n):
    taps = G2_taps[prn_id - 1].split('&')
    xor1 = int(G2[int(taps[0]) - 1]) ^ int(G2[int(taps[1]) - 1])
    xor2 = str(int(G1[9]) ^ xor1)
    ca_sequence += xor2

    new_G1, feedback1 = LFSR(G1, '1 + x3 + x10')
    new_G2, feedback2 = LFSR(G2, '1 + x2 + x3 + x6 + x8 + x9 + x10')

    print('■ ' + G1 + '\t' + feedback1 + '\t' + G2 +
          '\t' + feedback2 + '\t' + xor2 + '\t\t■')

    G1 = new_G1
    G2 = new_G2

  return ca_sequence

def main():
  """Main function of the program. Users can choose between generating a GPS L1C/A code or checking G2 taps by prn id.
  """
  while True:
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    print('■         WELCOME TO THE GPS L1C/A CODE GENERATOR!              ■')
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    print('It is quite simple to use this program, just input a pseudorandom')
    print('noise (prn) id, it must be a number between 1 and 32, and the')
    print('number of bits you want to generate (positive integer).')
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    print('What do you want to do?')
    print('[1] Generate GPS L1C/A Code.')
    print('[2] Check G2 Taps by prn id.')
    print('[0] Exit.')
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
    option = input('Option  ->  ')
    print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')

    if int(option) not in range(3):
      print('Invalid option!')
      continue

    if option == '0':
      print('See you soon!')
      print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
      break

    if option == '1':
      prn_id = input('Introduce a prn id (1-32) -> ')
      print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
      n = input('Introduce number of bits to generate -> ')
      print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
      gps_l1ca_code = GPS_L1CA_generator(int(prn_id), int(n))
      print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
      print('\t\tGPS L1C/A Code:', gps_l1ca_code)

    if option == '2':
      print('■                          G2 TAPS                              ■')
      print('■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')
      print('|                                                               |')
      for i in range(1, 17):
        print('|\tPRN ID: ' + str(i) + ' -> ' +
              G2_taps[i - 1] + '\t\tPRN ID: ' + str(i + 16) + ' -> ' + G2_taps[i + 15] + '\t|')
      print('|                                                               |')
  return

if __name__ == '__main__':
  main()
