"""
A blackjack simulator with 2 or more AI players and playable main character.
"""


import random

class PlayerAccount:
    def __init__(self,money):
        self.money = float(money)

def PutPunctuation():
    print(".")
    print(".")
    print(".")
    print(".")

#the deck
deck = [[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11]]
#shuffle the deck after you play
def Shuffle():
    deck = [[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11]]
#draw a card from the simulated deck
def DrawCard():
    i = random.randint(0,3)
    while len(deck[i])<1:
        i = random.randint(0,3)
    j = random.randint(0,len(deck[i])-1)
    card=deck[i][j]
    deck[i].remove(card)
    if i==0:
        print("The drawn card is diamond ",card)
    elif i==1:
        print("The drawn card is spade ",card)
    elif i==2:
        print("The drawn card is hearth ",card)
    elif i==3:
        print("The drawn card is club ",card)
    return card
#plays for the player
def PlayerPlay():
    inGame=True
    inLoop=True
    card1 = DrawCard()
    s = card1
    cardsDrawn=1
    while inGame:
        inLoop = True
        card = DrawCard();
        s+=card
        cardsDrawn+=1
        print("Your total is ",s)
        if s==22 and cardsDrawn==2:
            return 21
        elif s>21:
            inGame=False
        elif s==21:
            print("You won!")
            inGame=False
        elif s<21:
            while inLoop:
                x = str(input("What to do? "))
                if x=="Draw":
                    inLoop= False
                elif x=="Hold" and s>=14:
                    inGame=False
                    inLoop = False
                elif x=="Hold" and s<14:
                    print("You can't hold now.")
                    inLoop = False
                else:
                    print("Wrong command, try again!")
    PutPunctuation()
    return s
#plays for the AI player
def AIPlay():
    aiPlay = True
    sai= DrawCard()+DrawCard()
    if(sai==21 or sai==22):
        return 21
    while aiPlay:
        if sai>21:
            break
        elif sai==21:
            break
        elif sai>=18:
            return sai
        elif sai <18 and sai >15:
            thing = random.randint(1,2)
            if not thing ==1:
                return sai
        cardai = DrawCard()
        sai+=cardai    
    return sai
play = True
s = 0
def PrintRules():
    print("How to play:")
    print("Your goal is to make the sum of 21 from your drawn cards-then you automatically win!")
    print("The first two 11's count as 21 as well.") 
    print("Caution! If you get past 21 with your total, then you lose automatically.")
    print("If you have more points from the cards in total than 13 then you can stop; now the bank and the AI players will draw cards as well.")
    print("The highest number wins! Beware of the bank, if you make equall with him, you lose!")
    print("At the start of the game:")
    print("   -You have to input number of ai players from 2 up to 8(including the bank).")
    print("   -At the start of every round, you have to define the cost of the round(if you write \"All In\", then you will send all of your money); it will be removed from your money; if you win, you get back the cost*players/how many AI players have the same sum as you.") 
    print("Commands at your turn:")
    print("   -Draw-draw a new card")
    print("   -Hold-stop at the current cards and the sum of them")
    print("   -For yes/no questions, the commands Yes and No should be used respectively.")
    
#Main part of the program
y = input("Show game rules and help?(Yes/No) ")
if y =="Yes":
    PrintRules()
numberOfAI=int(input("How many AI's do you want in your game? "))-1
if numberOfAI>8:
    print("Maximum number of AI is 8; setting it to this value.")
    numberOfAI=7
elif numberOfAI <2:
    print("Minimum number of AI is 2; setting it to this value.")
    numberOfAI = 1
AIPlayers=[]
player =PlayerAccount(100)
print("Your money is",player.money,"dollars.")
while play:
    #gets money input
    if player.money==0:
        break
    cost = input("How much do you want to spend on this round? ")
    if cost=="All In":
        print("You gave in every last cent of yours(",player.money,"dollars).")
        cost = player.money
        player.money=0
    elif float(cost) > player.money:
        print("You don't have enough money for this.")
        cost = input("How much would you like to spend? ")
    else:
        player.money -=float(cost)
    Shuffle()
    toDivideBy=1
    s=PlayerPlay()
    playerWins= True
    AIWins=False
    bankWins=False
    print("Bank plays now!")
    bank = AIPlay()
    print("Bank's score is",bank,"points.")
    if bank==21:
            bankWins = True
            playerWins=False
    if s<22 and not bankWins:
        for i in range(0,numberOfAI):
            print("AI's turn!")
            print("These are the AI's cards: ")
            AIPlayers.append(AIPlay())
            print("AI has",AIPlayers[i],"points.")
        toCheck = s
        for i in range(0,numberOfAI):
            if (AIPlayers[i]>=toCheck or AIPlayers[i]>toCheck) and AIPlayers[i]<22:
                if s==AIPlayers[i]:
                    toDivideBy+=1
                else:
                    toCheck=AIPlayers[i]
                    AIWins=True
                    playerWins=False
        if toCheck<=bank and bank<22:
            AIWins=False
            bankWins=True
            playerWins=False
    else:
        AIWins=True
        toCheck=1
        for i in range(0,numberOfAI):
            print("AI's turn!")
            print("These are the AI's cards: ")
            AIPlayers.append(AIPlay())
            print("AI has ",AIPlayers[i],"points.")
            if AIPlayers[i]>toCheck and AIPlayers[i]<22:
                toCheck = AIPlayers[i]
        playerWins = False
        for i in range(0,numberOfAI):
            if AIPlayers[i]<=bank and bank<22 and AIPlayers[i]<22:
                bankWins=True
                AIWins = False           
    if AIWins:
        print("AI wins with", toCheck,"points.")
    elif playerWins:
        print("You win with",s,"points.")
        print("You get",float(int((float(cost)*(numberOfAI+1))/toDivideBy)),"dollars")
        player.money +=float(int((float(cost)*(numberOfAI+1))/toDivideBy))
    elif bankWins:
        print("Bank wins with",bank,"points.")
    print("You have", player.money,"dollars.")
    y = str(input("Wanna play more? "))
    inLoop = True
    while inLoop:
        if y == "No":
            y =input("That's pretty sad. Are you sure? ")
            if y=="Yes":
                inLoop = False
                play = False
            elif y=="No":
                deck = [[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11]]
                inLoop = False
                print("Good choice! Then let's play another round!")
                inGame=True
                s=0
        elif y=="Yes":
            deck = [[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11],[2,3,4,5,6,7,8,9,10,11]]
            inLoop = False
            inGame=True
            s=0
            sai=0
        else:
            print("Wrong command, try again!")
            y = str(input("So wanna play another round? "))
             
