import random

c_moves = ["rock", "paper", "scissors"]

computer = c_moves[random.randint(0,2)]

player = False

while player == False:
    player = input("enter your move: ")
    if computer == player:
        print("its a tie")
    elif player == 'rock':
        if computer == 'paper':
            print("you loose, computer wins!")
        else:
            print("you win")
    elif player == 'paper':
        if computer == 'scissors':
            print("you loose, computer wins")
        else:
            print("you win")
    elif player == 'scissors':
        if computer == 'rock':
            print("you loose, computer wins")
        else:
            print("you win")
 #   new_game = input("do want to play another round? (y/n) ")
 #   if new_game == 'y':
  #      player = False
  #  else:
   #     print("thanks for playing")
   #     break;
     
   