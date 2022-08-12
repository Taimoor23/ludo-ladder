#-----------------Boilerplate Code Start-----------
from multiprocessing.sharedctypes import Value
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image


screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
dice = None

rollButton = None

def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xpos=30
    for box in range(0,11):
        if box == 0:
            boxLabel= Label(gameWindow, font=('Helvetica',30),width=1,height=1,relief='ridge',borderwidth=0,bg='red')
            boxLabel.place(x=xpos,y=screen_height/2-100)
            leftBoxes.append(boxLabel)
            xpos+=45
        else:
            boxLabel= Label(gameWindow, font=('Helvetica',30),width=1,height=1,relief='ridge',borderwidth=0,bg='white')
            boxLabel.place(x=xpos,y=screen_height/2-100)
            leftBoxes.append(boxLabel)
            xpos+=60

def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xpos=850
    for box in range(0,11):
        if box == 10:
            boxLabel= Label(gameWindow, font=('Helvetica',30),width=1,height=1,relief='ridge',borderwidth=0,bg='yellow')
            boxLabel.place(x=xpos,y=screen_height/2-100)
            leftBoxes.append(boxLabel)
            xpos+=35
        else:
            boxLabel= Label(gameWindow, font=('Helvetica',30),width=1,height=1,relief='ridge',borderwidth=0,bg='white')
            boxLabel.place(x=xpos,y=screen_height/2-100)
            leftBoxes.append(boxLabel)
            xpos+=60             

def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)



def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    
    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    leftBoard()
    rightBoard()
    finishingBox()

    global rollButton
    rollButton=Button(gameWindow,text='Roll dice',font=('Chalkboard SE',15),bg='grey',command=rollDice,fg='black',width=20,height=5)
    global playerTurn
    global playerType
    global playerName
    if(playerType=='player1'and playerTurn):
        rollButton.place(x=screen_width/2-80,y=screen_height/2+400)
    else:
        rollButton.pack_forget()
    # Creating Dice with value 1
    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def rollDice():
    global SERVER
    global playerType
    global rollButton
    global playerTurn

    diceChoices=['/2680','/2681','/2682','/2683','/2684','/2685']
    value=random.choice(diceChoices)
    rollButton.destroy()
    playerTurn=False
    if (playerType=='player1'):
        SERVER.send(f'{value}player2turn'.encode())
    if (playerType=='player2'):
        SERVER.SEND(F'{value}player1turn'.encode())

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())
    gameWindow()
def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow=Tk()
    nameWindow.title('LUDO LADDER')
    nameWindow.attributes('-fullscreen',True)

    screen_width=nameWindow.winfo_screenwidth()
    screen_height=nameWindow.winfo_height()
    img=Image.open('./assets/background.png')
    resize_image=img.resize((1600,900),Image.ANTIALIAS)
    bg=ImageTk.PhotoImage(resize_image)
    canvas1=Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill='both',expand=True)
    canvas1.create_image(0,0,image=bg,anchor='nw')
    canvas1.create_text(screen_width/2,screen_height/3+200,text='Enter name',font=('Chalkboard SE',100),fill='white')
    nameEntry=Entry(nameWindow,width=15,justify='center',font=('Chalkboard SE',50),bg='white')
    nameEntry.place(x=screen_width/2-220,y=screen_height/4+350)
    button=Button(nameWindow,text='Save',font=('Chalkboard SE',30),width=15,command=saveName,height=2,bg='#80deea',bd=3)
    button.place(x=screen_width/2-150,y=screen_height/2+500)
    nameWindow.resizable(True,True)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()
    
    




def recivedMsg():
    pass
  

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    
    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
