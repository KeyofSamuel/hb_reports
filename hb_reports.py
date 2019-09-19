#!/usr/bin/python

## -- HomeBank Report Generator -- ##
 
# -- Imports -- #
import sys
import os
import pwd
import yaml
import logging
import logging.handlers
 
import legacy_complete_report
import monthly_report

# -- Define Variables -- #

menu_actions  = {}

# -- Menu Functions -- #
 
# Main menu
def main_menu():
    os.system('clear')
    
    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Run a Monthly Report")
    print("1. Menu 1")
    print("11. Menu 1")
    print("12. Menu 2")
    print("99 BETA - Complete LEGACY Monthly Report")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
    return
 
# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return
 
# Menu 1
def menu1():
    print("Hello Menu 1 !\n")
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return
 
 
# Menu 2
def menu2():
    print("Hello Menu 2 !\n")
    print("9. Back")
    print("0. Quit") 
    choice = input(" >>  ")
    exec_menu(choice)
    return
 
# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()
 
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': monthly_report.Monthly_Report,
    '11': menu1,
    '12': menu2,
    '9': back,
    '99': legacy_complete_report.Complete_Report_NEW,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
