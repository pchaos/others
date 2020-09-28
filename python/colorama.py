#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorama import init, Fore, Back 
init()
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Fore.RESET + Back.RESET)
print('back to normal now')
