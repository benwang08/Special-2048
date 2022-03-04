from math import fabs
from operator import or_, truediv
from shutil import move
from game_class import Board
import time
import random
import msvcrt


debugging = True
restart = True

while restart == True:
    print (r"""
                      _       _ 
                     (_)     | |
  ___ _ __   ___  ___ _  __ _| |
 / __| '_ \ / _ \/ __| |/ _` | |
 \__ \ |_) |  __/ (__| | (_| | |
 |___/ .__/ \___|\___|_|\__,_|_|
     | |                        
  ___|_|___  _  _   ___         
 |__ \ / _ \| || | / _ \        
    ) | | | | || || (_) |       
   / /| | | |__   _> _ <        
  / /_| |_| |  | || (_) |       
 |____|\___/   |_| \___/  """)

    print ("\n\n")
    for i in range(50):
        if debugging == False:
            time.sleep(0.05)
        print("*", end = "", flush = True)
    print("\n")

    print ("\nWelcome to special 2048, a game inspired by 2048 with special features and gamemodes")
    if debugging == False:
        time.sleep(3)
    print (r"""
    There exist 3 game modes...
    For each game mode, the user specifies the dimensions of the board from 4 (standard) to 10

    Classic: standard 2048, combine like pieces using arrow keys and try to reach 2048
            if the board is full with no more possible moves, the game is over.

    Scramble: like standard 2048, but the board might randomly scramble itself between
            moves. Reach 2048 to win.

    Special: this game mode has 3 powerups
            (2x) - Each number has a random chance to double, excluding numbers 1024 or higher
            (Wipe) - Wipes the board of all "2" and "4" numbers
            (Lifesaver) - Can only be bought once per game. resets the board back 10 moves.
                        This powerup is used automatically if no possible moves remain.
            
            The price of each powerup is determined by the dimensions of the board.
            The goal tile is determined by the dimensions of the board.
    """)

    for i in range(50):
        if debugging == False:
            time.sleep(0.1)
        print("*", end = "", flush = True)
    print("\n")

    start = " "

    while(start != "s" and start != "S"):
        start = input("\nInput 'S' to begin: ")

    print("\nGame modes: (1)-Classic  (2)-Scramble  (3)-Special")
    mode = input("Please select a mode: ")
    while (not mode.isnumeric() or int(mode) < 1 or int(mode) > 3):
        mode = input("Invalid mode selected, please select a mode (1-3): ")

    mode = int(mode)

    if mode == 1:
        print(r"""
                                                                         
  ,ad8888ba,   88                                    88              
 d8"'    `"8b  88                                    ""              
d8'            88                                                    
88             88  ,adPPYYba,  ,adPPYba,  ,adPPYba,  88   ,adPPYba,  
88             88  ""     `Y8  I8[    ""  I8[    ""  88  a8"     ""  
Y8,            88  ,adPPPPP88   `"Y8ba,    `"Y8ba,   88  8b          
 Y8a.    .a8P  88  88,    ,88  aa    ]8I  aa    ]8I  88  "8a,   ,aa  
  `"Y8888Y"'   88  `"8bbdP"Y8  `"YbbdP"'  `"YbbdP"'  88   `"Ybbd8"'  
                                                                     
                                                                     """)
    elif mode == 2:
            print(r"""                                                        
  ####    ####   #####     ##    #    #  #####   #       ###### 
 #       #    #  #    #   #  #   ##  ##  #    #  #       #      
  ####   #       #    #  #    #  # ## #  #####   #       #####  
      #  #       #####   ######  #    #  #    #  #       #      
 #    #  #    #  #   #   #    #  #    #  #    #  #       #      
  ####    ####   #    #  #    #  #    #  #####   ######  ###### """)

    else:
        print(r"""
 ___                                   _   
(  _`\                       _        (_ ) 
| (_(_) _ _      __     ___ (_)   _ _  | | 
`\__ \ ( '_`\  /'__`\ /'___)| | /'_` ) | | 
( )_) || (_) )(  ___/( (___ | |( (_| | | | 
`\____)| ,__/'`\____)`\____)(_)`\__,_)(___)
       | |                                 
       (_)                                 
    """)
    print ("\n")
    for i in range(50):
        if debugging == False:
            time.sleep(0.015)
        print("*", end = "", flush = True)
    print("\n")
    print("\nSelect the dimensions of the board...")
    dimension = (input("Input one number from '4' to '10' for the dimension of the board: "))
    while not dimension.isnumeric() or int(dimension) < 4 or int(dimension) > 10:
        dimension = (input("Invalid input, please input one number from 4 to 10: "))

    dimension = int(dimension)

    print("Selected dimension:", dimension, "x", dimension)

    print("")
    for i in range(50):
        if debugging == False:
            time.sleep(0.05)
        print("*", end = "", flush = True)
    print("")
    cost = 0
    target = 2048

    if mode == 1 or mode == 2:
        print("\nControls: arrow keys to move tiles.")
    else:
        print("\nControls: arrow keys to move tiles.")
        print("\n-Option to purchase powerups and use powerups will be given during rounds")
        if (dimension < 6):
            print("-Cost of power ups will be a 256 tile, selected randomly")
            print("-The winning tile will be 4096")
            cost = 256
            target = 4097
        else:
            print("Cost of power ups will be a 512 tile, selected randomly")
            print("The winning tile will be 8192")
            cost = 512
            target = 8192

    print("")
    for i in range(50):
        if debugging == False:
            time.sleep(0.05)
        print("*", end = "", flush = True)
    print("\n")

    start = input("'B' to begin: ")
    while start != "b" and start != "B":
        start = input("'B' to begin: ")

    game = Board(dimension)
    gameOver = False
    moveCount = 0
    twox_pu, wipe_pu, ls_pu = 0,0,0
    LS = False
    skip = False
    specialMoved = True
    temp = None
    while not gameOver:
        if skip != True or specialMoved == True:
            game.spawn()
        skip = False
        specialMoved = True
        game.drawBoard()
        if (mode == 3):
            print("BUY POWERUPS? (q): 2x power up   (w): Wipe power up   (e): Lifesaver power up")
            print("USE POWERUPS? (z): 2x,", twox_pu, "available   (x): Wipe,", wipe_pu,
            "available   (c): Lifesaver,", ls_pu, "available")

            while msvcrt.kbhit():
                flush = ord(msvcrt.getch())
                flush = ord(msvcrt.getch())

            temp = game.getMove(True)
            skip = True

            if temp == "b1" or temp == "b2":
                specialMoved = False
                if game.removeValue(cost) == False:
                    print("COULD NOT AFFORD POWER UP!")
                else:
                    if temp == "b1":
                        twox_pu += 1
                        print ("sucessfully bought 2x power up, ", end = "")
                    else:
                        wipe_pu += 1
                        print ("sucessfully bought Wipe power up, ", end = "")
                    print ("one", cost, "tile deducted")
                    time.sleep(2)

            if temp == "b3":
                specialMoved = False
                if LS == True:
                    "COULD NOT BUY LifeSaver, ALREADY BOUGHT!"
                elif game.removeValue(cost) == False:
                    print("COULD NOT AFFORD POWER UP!")
                else:
                    LS = True
                    ls_pu += 1
                    print ("sucessfully bought Lifesaver power up, ", end = "")
                    print ("one", cost, "tile deducted")
                    time.sleep(2)


            if temp == "u1" or temp == "u2" or temp == "u3":
                specialMoved = False

                if temp == "u1" and twox_pu > 0:
                    twox_pu -= 1
                    game.randomDoubler()
                    print ("sucessfully used 2x power up")
                elif temp == "u2" and wipe_pu > 0:
                    wipe_pu -= 1
                    game.removeLows()
                    print ("sucessfully used Wipe power up")
                elif temp == "u3" and ls_pu > 0:
                    ls_pu -= 1
                    game.lifeSaver()
                    print ("sucessfully used Lifesaver power up")
                else:
                    print("COULD NOT USE POWER UP - INSUFFICIENT QUANTITY\n\n")
                    if debugging == False:
                        time.sleep(1.2)
                    continue

        if not skip:
            moveCount += 1
            while msvcrt.kbhit():
                flush = ord(msvcrt.getch())
                flush = ord(msvcrt.getch())
            game.setMove(game.getMove(False))
        if skip and specialMoved == True:
            game.saveBoard()
            moveCount += 1
            game.setMove(temp)

        if mode == 2:
            token = random.randint(1,10)
            if token == 10:
                game.scramble()
                print("*" * 10 + "BOARD HAS BEEN SCRAMBLED!" + "*" * 10)

        if skip and specialMoved == False:
            if debugging == False:
                time.sleep(1.2)
            print ("\n")
        else:
            test = game.checkOver(target)
            if test == "lost":
                if mode == 3 and ls_pu == 1:
                    print("no more possible moves, Lifesaver automatically used\n")
                    specialMoved = True
                    time.sleep(1.5)
                    game.lifeSaver();
                    ls_pu -= 1;
                else:
                    game.drawBoard()
                    print("\n")
                    gameOver = True
                    print(r"""
                 __ __   ___   __ __      _       ___    _____ ______ 
                |  |  | /   \ |  |  |    | |     /   \  / ___/|      |
                |  |  ||     ||  |  |    | |    |     |(   \_ |      |
                |  ~  ||  O  ||  |  |    | |___ |  O  | \__  ||_|  |_|
                |___, ||     ||  :  |    |     ||     | /  \ |  |  |  
                |     ||     ||     |    |     ||     | \    |  |  |  
                |____/  \___/  \__,_|    |_____| \___/   \___|  |__|  
                                                      """)
                    time.sleep(2)
                    print("\nNo more possible moves. Final move count:", moveCount)
            if test == "win":
                game.drawBoard()
                print("\n")
                print(r"""
             _  _  _____  __  __    _    _  ____  _  _ /\
            ( \/ )(  _  )(  )(  )  ( \/\/ )(_  _)( \( ))(
             \  /  )(_)(  )(__)(    )    (  _)(_  )  ( \/
             (__) (_____)(______)  (__/\__)(____)(_)\_)() """)
                time.sleep(2)
                print("\nFinal move count:", moveCount)
                gameOver = True

    for i in range(50):
        if debugging == False:
            time.sleep(0.1)
        print("*", end = "", flush = True)
    print("")
    quit = input("'R' to restart, any other entry to quit: ")
    if (quit != "R" and quit != 'r'):
        restart = False
    




        



    








