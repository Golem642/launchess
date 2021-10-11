#dames, échecs, puissance 4, snake, tetris, petits chevaux, 2048...
import rtmidi
from time import *
import copy

midiin = rtmidi.MidiIn()
available_ports = midiin.get_ports()
for i in range(len(available_ports)): available_ports[i]=available_ports[i][0:7]
try: midiin.open_port(available_ports.index('MIDIIN2'))
except: print("No Launchpad was found for input")
else: print('Launchpad input ready')
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
for i in range(len(available_ports)): available_ports[i]=available_ports[i][0:8]
try: midiout.open_port(available_ports.index('MIDIOUT2'))
except: print("No Launchpad was found for output")
else: print('Launchpad output ready')

#pospad=[[64,65,66,67,96,97,98,99],
#        [60,61,62,63,92,93,94,95],
#        [56,57,58,59,88,89,90,91],
#        [52,53,54,55,84,85,86,87],
#        [48,49,50,51,80,81,82,83],
#        [44,45,46,47,76,77,78,79],
#        [40,41,42,43,72,73,74,75],
#        [36,37,38,39,68,69,70,71]]

def dames(): #problème: grille 10*10. soluce: tout ajouter
    pospad=[[64,65,66,67,96,97,98,99],
        [60,61,62,63,92,93,94,95],
        [56,57,58,59,88,89,90,91],
        [52,53,54,55,84,85,86,87],
        [48,49,50,51,80,81,82,83],
        [44,45,46,47,76,77,78,79],
        [40,41,42,43,72,73,74,75],
        [36,37,38,39,68,69,70,71]]
    plat=[[0,2,0,2,0,2,0,2],
          [2,0,2,0,2,0,2,0],
          [0,2,0,2,0,2,0,2],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def echecs():
    #(changer la couleur des noirs : 103->69 ?)
    #régler les problèmes du rewind (promotion non sauvegardée)
    print("Loading chess game...")
    global midiin
    global midiout
    global colorp1
    colorp1=3
    global colorp2
    colorp2=103
    pospad=[[64,65,66,67,96,97,98,99],
            [60,61,62,63,92,93,94,95],
            [56,57,58,59,88,89,90,91],
            [52,53,54,55,84,85,86,87],
            [48,49,50,51,80,81,82,83],
            [44,45,46,47,76,77,78,79],
            [40,41,42,43,72,73,74,75],
            [36,37,38,39,68,69,70,71]]
    global plat
    plat=[["T2","C2","F2","D2","R2","F2","C2","T2"],
          ["P2","P2","P2","P2","P2","P2","P2","P2"],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["P1","P1","P1","P1","P1","P1","P1","P1"],
          ["T1","C1","F1","D1","R1","F1","C1","T1"]]
    global order
    order=["R","D","F","C","T","P"]
    global record
    record=[]
    def clearPad():
        for i in range(len(pospad)):
            for j in range(len(pospad[0])):
                midiout.send_message([0x90,pospad[i][j],0])
    def indexRequest(name):
        global plat
        pos=[]
        for i in range(len(plat)):
            for j in range(len(plat[0])):
                if plat[i][j]==name: pos.append((i,j))
        return pos
    clearPad()
    global turn
    turn=1
    global selectLine
    def selectLine(turn=1):
        if turn==1:
#            midiout.send_message([144,100,3])
            midiout.send_message([144,101,colorp1])
            midiout.send_message([144,102,colorp1])
            midiout.send_message([144,103,colorp1])
            midiout.send_message([144,104,colorp1])
            midiout.send_message([144,105,colorp1])
            midiout.send_message([144,106,colorp1])
#            midiout.send_message([144,107,3])
        elif turn==2:
#            midiout.send_message([144,100,3])
            midiout.send_message([144,101,colorp2])
            midiout.send_message([144,102,colorp2])
            midiout.send_message([144,103,colorp2])
            midiout.send_message([144,104,colorp2])
            midiout.send_message([144,105,colorp2])
            midiout.send_message([144,106,colorp2])
#            midiout.send_message([144,107,3])
    midiout.send_message([176,99,0])
    def Players():
        for i in range(len(plat)):
            for j in range(len(plat[0])):
                if plat[i][j]!="  ":
                    if plat[i][j][1]=="1":
                        midiout.send_message([0x90,pospad[i][j],colorp1])
                    elif plat[i][j][1]=="2":
                        midiout.send_message([0x90,pospad[i][j],colorp2])
    global printGame
    def printGame():
        global order
        p1pieces=["♔","♕","♗","♘","♖","♙"]
        p2pieces=["♚","♛","♝","♞","♜","♟"]
        print("\n")
        print('----------------------')
        for i in range(len(plat)):
            for j in range(len(plat[0])):
                if plat[i][j]!="  ":
                    if plat[i][j][1]=="1":
                        print('|'+p1pieces[order.index(plat[i][j][0])],end='')
                    elif plat[i][j][1]=="2":
                        print('|'+p2pieces[order.index(plat[i][j][0])],end='')
                else:
                    if j&1==0: print('|     ',end='')
                    elif j&1==1: print('|    ',end='')
            print('|')
            print('----------------------')
    def rewind():
        global plat
        global colorp1
        global colorp2
        global turn
        global order
        base=[["T2","C2","F2","D2","R2","F2","C2","T2"],
              ["P2","P2","P2","P2","P2","P2","P2","P2"],
              ["  ","  ","  ","  ","  ","  ","  ","  "],
              ["  ","  ","  ","  ","  ","  ","  ","  "],
              ["  ","  ","  ","  ","  ","  ","  ","  "],
              ["  ","  ","  ","  ","  ","  ","  ","  "],
              ["P1","P1","P1","P1","P1","P1","P1","P1"],
              ["T1","C1","F1","D1","R1","F1","C1","T1"]]
        def Players():
            for i in range(len(plat)):
                for j in range(len(plat[0])):
                    if plat[i][j]!="  ":
                        if plat[i][j][1]=="1":
                            midiout.send_message([0x90,pospad[i][j],colorp1])
                        elif plat[i][j][1]=="2":
                            midiout.send_message([0x90,pospad[i][j],colorp2])
                    else: midiout.send_message([0x90,pospad[i][j],0])
        midiout.send_message([176, 91, 21])
        midiout.send_message([176, 93, 13])
        midiout.send_message([176, 94, 0])
        touch=0
        pos=len(record)-1
        turn=int(plat[record[-1][1][0]][record[-1][1][1]][1])
        turn=turn-1+(turn==1)*2
        Players()
        while not touch==1:
            msg=midiin.get_message()
            if msg:
                if msg[0][2]!=0 and msg[0][0]==176:
                    touch=msg[0][1]-90
                    if touch==3:
                        rew=copy.deepcopy(base)
                        for i in range(pos):
                            rew[record[i][1][0]][record[i][1][1]]=rew[record[i][0][0]][record[i][0][1]]
                            rew[record[i][0][0]][record[i][0][1]]="  "
                            rew[record[i][1][0]][record[i][1][1]]=order[record[i][2]]+rew[record[i][1][0]][record[i][1][1]][1]
                        plat=copy.deepcopy(rew)
                        pos-=1
                        if pos<-1:
                            pos=-1
                            midiout.send_message([176, 93, 0])
                        else:
                            midiout.send_message([176, 93, 13])
                            turn=turn-1+(turn==1)*2
                        if pos==-1: midiout.send_message([176, 93, 0])
                        midiout.send_message([176, 94, 13])
                        Players()
                        selectLine(turn)
                        printGame()
                    elif touch==4:
                        if pos!=len(record)-1:
                            pos+=1
                            if pos>len(record)-1: pos=len(record)-1
                            plat[record[pos][1][0]][record[pos][1][1]]=plat[record[pos][0][0]][record[pos][0][1]]
                            plat[record[pos][0][0]][record[pos][0][1]]="  "
                            plat[record[pos][1][0]][record[pos][1][1]]=order[record[pos][2]]+plat[record[pos][1][0]][record[pos][1][1]][1]
                            if pos==len(record)-1: midiout.send_message([176, 94, 0])
                            else: midiout.send_message([176, 94, 13])
                            turn=turn-1+(turn==1)*2
                        midiout.send_message([176, 93, 13])
                        selectLine(turn)
                        Players()
                        printGame()
        while len(record)-1!=pos: record.pop(-1)
        midiout.send_message([176, 91, 0])
        midiout.send_message([176, 93, 0])
        midiout.send_message([176, 94, 0])
    global available
    available=[]
    def saveAvailable(x,y,color):
        global midiout
        global available
        midiout.send_message([0x90,pospad[y][x],color])
        available.append(pospad[y][x])
    clearPad()
    midiout.send_message([176, 91, 0])
    midiout.send_message([176, 93, 0])
    midiout.send_message([176, 94, 0])
    midiout.send_message([144,100,0])
    midiout.send_message([144,101,0])
    midiout.send_message([144,102,0])
    midiout.send_message([144,103,colorp2])
    midiout.send_message([144,104,colorp1])
    midiout.send_message([144,105,0])
    midiout.send_message([144,106,0])
    midiout.send_message([144,107,0])
    turn=0
    msg=''
    print("Choose who starts")
    while not turn:
        msg=midiin.get_message()
        if msg:
            if msg[0][1]==104: turn=1
            elif msg[0][1]==103: turn=2
            else: turn=0
    selectLine(turn)
    Players()
    pos=[]
    touch=[]
    stop=0
    rewp1=0
    rewp2=0
    print("Game starting with Player",turn)
    printGame()
    while not stop:
        msg=midiin.get_message()
        if msg:
            msg=msg[0]
#            if msg==[176, 91, 127]:
#                stop=1
            if msg[2]!=0:
                if msg[1]>99:
                    clearPad()
                    Players()
                    selectLine(turn)
                    touch=msg[1]-101
                    if touch>=0 and touch<=5:
                        Players()
                        if turn==1:
                            pos=indexRequest(order[touch]+str(turn))
                            for i in range(len(pos)):
                                midiout.send_message([0x90,pospad[pos[i][0]][pos[i][1]],45])
                            pos=indexRequest(order[touch]+str(turn-1+(turn==1)*2))
                            for i in range(len(pos)):
                                midiout.send_message([0x90,pospad[pos[i][0]][pos[i][1]],5])
                        if turn==2:
                            pos=indexRequest(order[-touch-1]+str(turn))
                            for i in range(len(pos)):
                                midiout.send_message([0x90,pospad[pos[i][0]][pos[i][1]],45])
                            pos=indexRequest(order[-touch-1]+str(turn-1+(turn==1)*2))
                            for i in range(len(pos)):
                                midiout.send_message([0x90,pospad[pos[i][0]][pos[i][1]],5])
                    else:
                        if record:
                            if touch==-1:
                                if rewp1==0:
                                    rewp1=1
                                    midiout.send_message([144,100,9])
                                elif rewp1==1:
                                    rewp1=0
                                    midiout.send_message([144,100,0])
                            if touch==6:
                                if rewp2==0:
                                    rewp2=1
                                    midiout.send_message([144,107,9])
                                elif rewp2==1:
                                    rewp2=0
                                    midiout.send_message([144,107,0])
                            if rewp1 and rewp2:
                                rewind()
                                rewp1=0
                                rewp2=0
                                midiout.send_message([144,107,0])
                                midiout.send_message([144,100,0])
                                selectLine(turn)
                                Players()
                                printGame()
                elif msg[0]==144:
                    clearPad()
                    Players()
                    selectLine(turn)
                    touch=msg[1]
                    try: available.index(touch)
                    except:
                        pos=[]
                        for i in range(len(pospad)):
                            for j in range(len(pospad[0])):
                                if pospad[i][j]==touch: pos=[i,j]
                        choosen=plat[pos[0]][pos[1]]
                        if choosen!="  ":
                            if turn==1:
                                if choosen[1]==str(turn): midiout.send_message([144,order.index(choosen[0])+101,45])
                                else: midiout.send_message([144,order.index(choosen[0])+101,5])
                            elif turn==2:
                                if choosen[1]==str(turn): midiout.send_message([144,-(order.index(choosen[0]))-1+107,45])
                                else: midiout.send_message([144,-(order.index(choosen[0]))-1+107,5])
                        available=[]
                        def horseTest(plat,x,y,addx,addy,turn):
                            if (y+addy<=7 and y+addy>=0) and (x+addx<=7 and x+addx>=0):
                                if plat[y+addy][x+addx]=="  ": return 3
                                elif plat[y+addy][x+addx][1]==str(turn): return turn
                                else: return turn-1+(turn==1)*2
                        if choosen=="P"+str(turn):
                            if turn==1:
                                if pos[0]==6 and plat[pos[0]-2][pos[1]]=="  " and plat[pos[0]-1][pos[1]]=="  ":
                                    midiout.send_message([0x90,pospad[pos[0]-2][pos[1]],21])
                                    available.append(pospad[pos[0]-2][pos[1]])
                                if plat[pos[0]-1][pos[1]]=="  ":
                                    midiout.send_message([0x90,pospad[pos[0]-1][pos[1]],21])
                                    available.append(pospad[pos[0]-1][pos[1]])
                                if pos[1]!=0:
                                    if plat[pos[0]-1][pos[1]-1][1]=='2':
                                        midiout.send_message([0x90,pospad[pos[0]-1][pos[1]-1],5])
                                        available.append(pospad[pos[0]-1][pos[1]-1])
                                if pos[1]!=7:
                                    if plat[pos[0]-1][pos[1]+1][1]=='2':
                                        midiout.send_message([0x90,pospad[pos[0]-1][pos[1]+1],5])
                                        available.append(pospad[pos[0]-1][pos[1]+1])
                            if turn==2:
                                if pos[0]==1 and plat[pos[0]+2][pos[1]]=="  " and plat[pos[0]+1][pos[1]]=="  ":
                                    midiout.send_message([0x90,pospad[pos[0]+2][pos[1]],21])
                                    available.append(pospad[pos[0]+2][pos[1]])
                                if plat[pos[0]+1][pos[1]]=="  ":
                                    midiout.send_message([0x90,pospad[pos[0]+1][pos[1]],21])
                                    available.append(pospad[pos[0]+1][pos[1]])
                                if pos[1]!=0:
                                    if plat[pos[0]+1][pos[1]-1][1]=='1':
                                        midiout.send_message([0x90,pospad[pos[0]+1][pos[1]-1],5])
                                        available.append(pospad[pos[0]+1][pos[1]-1])
                                if pos[1]!=7:
                                    if plat[pos[0]+1][pos[1]+1][1]=='1':
                                        midiout.send_message([0x90,pospad[pos[0]+1][pos[1]+1],5])
                                        available.append(pospad[pos[0]+1][pos[1]+1])
                                        
                        if choosen=="T"+str(turn):
                            done=0
                            for i in range(pos[1]+1,len(pospad[0])):
                                if done==0:
                                    if plat[pos[0]][i]!="  ":
                                        if plat[pos[0]][i][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[pos[0]][i],5])
                                            available.append(pospad[pos[0]][i])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[pos[0]][i],21])
                                        available.append(pospad[pos[0]][i])
                            done=0
                            for i in range(pos[0]+1,len(pospad)):
                                if done==0:
                                    if plat[i][pos[1]]!="  ":
                                        if plat[i][pos[1]][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[i][pos[1]],5])
                                            available.append(pospad[i][pos[1]])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[i][pos[1]],21])
                                        available.append(pospad[i][pos[1]])
                            done=0
                            for i in range(pos[1]-1,-1,-1):
                                if done==0:
                                    if plat[pos[0]][i]!="  ":
                                        if plat[pos[0]][i][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[pos[0]][i],5])
                                            available.append(pospad[pos[0]][i])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[pos[0]][i],21])
                                        available.append(pospad[pos[0]][i])
                            done=0
                            for i in range(pos[0]-1,-1,-1):
                                if done==0:
                                    if plat[i][pos[1]]!="  ":
                                        if plat[i][pos[1]][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[i][pos[1]],5])
                                            available.append(pospad[i][pos[1]])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[i][pos[1]],21])
                                        available.append(pospad[i][pos[1]])
                                        
                        if choosen=="C"+str(turn):
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-1,-2,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-1,pos[0]-2,5)
                                elif ok!=turn: saveAvailable(pos[1]-1,pos[0]-2,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],+1,-2,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+1,pos[0]-2,5)
                                elif ok!=turn: saveAvailable(pos[1]+1,pos[0]-2,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],+2,-1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+2,pos[0]-1,5)
                                elif ok!=turn: saveAvailable(pos[1]+2,pos[0]-1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],+2,+1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+2,pos[0]+1,5)
                                elif ok!=turn: saveAvailable(pos[1]+2,pos[0]+1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],+1,+2,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+1,pos[0]+2,5)
                                elif ok!=turn: saveAvailable(pos[1]+1,pos[0]+2,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-1,+2,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-1,pos[0]+2,5)
                                elif ok!=turn: saveAvailable(pos[1]-1,pos[0]+2,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-2,+1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-2,pos[0]+1,5)
                                elif ok!=turn: saveAvailable(pos[1]-2,pos[0]+1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-2,-1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-2,pos[0]-1,5)
                                elif ok!=turn: saveAvailable(pos[1]-2,pos[0]-1,21)
                        
                        if choosen=="F"+str(turn):
                            diag=1
                            while pos[0]-diag>=0 and pos[1]+diag<=7:
                                if plat[pos[0]-diag][pos[1]+diag]!="  ":
                                    if plat[pos[0]-diag][pos[1]+diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]+diag],5])
                                        available.append(pospad[pos[0]-diag][pos[1]+diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]+diag],21])
                                    available.append(pospad[pos[0]-diag][pos[1]+diag])
                                    diag+=1
                            diag=1
                            while pos[0]+diag<=7 and pos[1]+diag<=7:
                                if plat[pos[0]+diag][pos[1]+diag]!="  ":
                                    if plat[pos[0]+diag][pos[1]+diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]+diag],5])
                                        available.append(pospad[pos[0]+diag][pos[1]+diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]+diag],21])
                                    available.append(pospad[pos[0]+diag][pos[1]+diag])
                                    diag+=1
                            diag=1
                            while pos[0]+diag<=7 and pos[1]-diag>=0:
                                if plat[pos[0]+diag][pos[1]-diag]!="  ":
                                    if plat[pos[0]+diag][pos[1]-diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]-diag],5])
                                        available.append(pospad[pos[0]+diag][pos[1]-diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]-diag],21])
                                    available.append(pospad[pos[0]+diag][pos[1]-diag])
                                    diag+=1
                            diag=1
                            while pos[0]-diag>=0 and pos[1]-diag>=0:
                                if plat[pos[0]-diag][pos[1]-diag]!="  ":
                                    if plat[pos[0]-diag][pos[1]-diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]-diag],5])
                                        available.append(pospad[pos[0]-diag][pos[1]-diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]-diag],21])
                                    available.append(pospad[pos[0]-diag][pos[1]-diag])
                                    diag+=1
                                    
                        if choosen=="R"+str(turn):
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-1,-1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-1,pos[0]-1,5)
                                elif ok!=turn: saveAvailable(pos[1]-1,pos[0]-1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],0,-1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1],pos[0]-1,5)
                                elif ok!=turn: saveAvailable(pos[1],pos[0]-1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],1,-1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+1,pos[0]-1,5)
                                elif ok!=turn: saveAvailable(pos[1]+1,pos[0]-1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-1,0,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-1,pos[0],5)
                                elif ok!=turn: saveAvailable(pos[1]-1,pos[0],21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],1,0,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+1,pos[0],5)
                                elif ok!=turn: saveAvailable(pos[1]+1,pos[0],21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],-1,1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]-1,pos[0]+1,5)
                                elif ok!=turn: saveAvailable(pos[1]-1,pos[0]+1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],0,1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1],pos[0]+1,5)
                                elif ok!=turn: saveAvailable(pos[1],pos[0]+1,21)
                            ok=0
                            ok=horseTest(plat,pos[1],pos[0],1,1,turn)
                            if ok:
                                if ok==turn-1+(turn==1)*2: saveAvailable(pos[1]+1,pos[0]+1,5)
                                elif ok!=turn: saveAvailable(pos[1]+1,pos[0]+1,21)
                        
                        if choosen=="D"+str(turn):
                            done=0
                            for i in range(pos[1]+1,len(pospad[0])):
                                if done==0:
                                    if plat[pos[0]][i]!="  ":
                                        if plat[pos[0]][i][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[pos[0]][i],5])
                                            available.append(pospad[pos[0]][i])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[pos[0]][i],21])
                                        available.append(pospad[pos[0]][i])
                            done=0
                            for i in range(pos[0]+1,len(pospad)):
                                if done==0:
                                    if plat[i][pos[1]]!="  ":
                                        if plat[i][pos[1]][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[i][pos[1]],5])
                                            available.append(pospad[i][pos[1]])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[i][pos[1]],21])
                                        available.append(pospad[i][pos[1]])
                            done=0
                            for i in range(pos[1]-1,-1,-1):
                                if done==0:
                                    if plat[pos[0]][i]!="  ":
                                        if plat[pos[0]][i][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[pos[0]][i],5])
                                            available.append(pospad[pos[0]][i])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[pos[0]][i],21])
                                        available.append(pospad[pos[0]][i])
                            done=0
                            for i in range(pos[0]-1,-1,-1):
                                if done==0:
                                    if plat[i][pos[1]]!="  ":
                                        if plat[i][pos[1]][1]==str(turn-1+(turn==1)*2):
                                            midiout.send_message([0x90,pospad[i][pos[1]],5])
                                            available.append(pospad[i][pos[1]])
                                        done=1
                                    else:
                                        midiout.send_message([0x90,pospad[i][pos[1]],21])
                                        available.append(pospad[i][pos[1]])
                            diag=1
                            while pos[0]-diag>=0 and pos[1]+diag<=7:
                                if plat[pos[0]-diag][pos[1]+diag]!="  ":
                                    if plat[pos[0]-diag][pos[1]+diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]+diag],5])
                                        available.append(pospad[pos[0]-diag][pos[1]+diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]+diag],21])
                                    available.append(pospad[pos[0]-diag][pos[1]+diag])
                                    diag+=1
                            diag=1
                            while pos[0]+diag<=7 and pos[1]+diag<=7:
                                if plat[pos[0]+diag][pos[1]+diag]!="  ":
                                    if plat[pos[0]+diag][pos[1]+diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]+diag],5])
                                        available.append(pospad[pos[0]+diag][pos[1]+diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]+diag],21])
                                    available.append(pospad[pos[0]+diag][pos[1]+diag])
                                    diag+=1
                            diag=1
                            while pos[0]+diag<=7 and pos[1]-diag>=0:
                                if plat[pos[0]+diag][pos[1]-diag]!="  ":
                                    if plat[pos[0]+diag][pos[1]-diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]-diag],5])
                                        available.append(pospad[pos[0]+diag][pos[1]-diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]+diag][pos[1]-diag],21])
                                    available.append(pospad[pos[0]+diag][pos[1]-diag])
                                    diag+=1
                            diag=1
                            while pos[0]-diag>=0 and pos[1]-diag>=0:
                                if plat[pos[0]-diag][pos[1]-diag]!="  ":
                                    if plat[pos[0]-diag][pos[1]-diag][1]==str(turn-1+(turn==1)*2):
                                        midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]-diag],5])
                                        available.append(pospad[pos[0]-diag][pos[1]-diag])
                                    diag=9
                                else:
                                    midiout.send_message([0x90,pospad[pos[0]-diag][pos[1]-diag],21])
                                    available.append(pospad[pos[0]-diag][pos[1]-diag])
                                    diag+=1
                            
                    else:
                        move=[]
                        for i in range(len(pospad)):
                            for j in range(len(pospad[0])):
                                if pospad[i][j]==touch: move=[i,j]
                        if turn==1:
                            plat[move[0]][move[1]]=plat[pos[0]][pos[1]]
                            midiout.send_message([0x90,pospad[move[0]][move[1]],colorp1])
                        elif turn==2:
                            plat[move[0]][move[1]]=plat[pos[0]][pos[1]]
                            midiout.send_message([0x90,pospad[move[0]][move[1]],colorp2])
                        plat[pos[0]][pos[1]]="  "
                        midiout.send_message([0x90,pospad[pos[0]][pos[1]],0])
                        available=[]
                        printGame()
                        newpiece=9
                        while plat[0].count("P1"):
                            if newpiece==9:
                                print("P1 choose pawn's promotion...")
                                newpiece=plat[0].index("P1")
                                midiout.send_message([0x90,pospad[0][newpiece],21])
                                midiout.send_message([144,101,0])
                                midiout.send_message([144,102,21])
                                midiout.send_message([144,103,21])
                                midiout.send_message([144,104,21])
                                midiout.send_message([144,105,21])
                                midiout.send_message([144,106,0])
                            msg2=midiin.get_message()
                            if msg2:
                                msg2=msg2[0]
                                if msg2[2]!=0 and msg2[1]>99:
                                        touch2=msg2[1]-102
                                        if touch2>=0 and touch2<=3:
                                            plat[0][newpiece]=order[touch2+1]+"1"
                                            midiout.send_message([0x90,pospad[0][newpiece],colorp1])
                                            newpiece=9
                                            printGame()
                        newpiece=9
                        while plat[7].count("P2"):
                            if newpiece==9:
                                print("P2 choose pawn's promotion...")
                                newpiece=plat[7].index("P2")
                                midiout.send_message([0x90,pospad[7][newpiece],21])
                                midiout.send_message([144,101,0])
                                midiout.send_message([144,102,21])
                                midiout.send_message([144,103,21])
                                midiout.send_message([144,104,21])
                                midiout.send_message([144,105,21])
                                midiout.send_message([144,106,0])
                            msg2=midiin.get_message()
                            if msg2:
                                msg2=msg2[0]
                                if msg2[2]!=0 and msg2[1]>99:
                                        touch2=msg2[1]-102
                                        if touch2>=0 and touch2<=3:
                                            plat[7][newpiece]=order[-touch2-2]+"2"
                                            midiout.send_message([0x90,pospad[7][newpiece],colorp1])
                                            newpiece=9
                                            printGame()
                                
                        if not indexRequest("R1"): stop=1
                        elif not indexRequest("R2"): stop=1
                        else:
                            if turn==1: turn=2
                            elif turn==2: turn=1
                        selectLine(turn)
                        record.append([(pos[0],pos[1]),(move[0],move[1]),order.index(plat[move[0]][move[1]][0])])

    midiout.send_message([144,101,0])
    midiout.send_message([144,102,0])
    midiout.send_message([144,103,0])
    midiout.send_message([144,104,0])
    midiout.send_message([144,105,0])
    midiout.send_message([144,106,0])
    if turn==1: midiout.send_message([176,99,colorp1])
    if turn==2: midiout.send_message([176,99,colorp2])
    print("Player",turn,"win !")
    sleep(5)

echecs()

def replayChess():
    global midiin
    global midiout
    global record
    global colorp1
    global colorp2
    pospad=[[64,65,66,67,96,97,98,99],
            [60,61,62,63,92,93,94,95],
            [56,57,58,59,88,89,90,91],
            [52,53,54,55,84,85,86,87],
            [48,49,50,51,80,81,82,83],
            [44,45,46,47,76,77,78,79],
            [40,41,42,43,72,73,74,75],
            [36,37,38,39,68,69,70,71]]
    base=[["T2","C2","F2","D2","R2","F2","C2","T2"],
          ["P2","P2","P2","P2","P2","P2","P2","P2"],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["  ","  ","  ","  ","  ","  ","  ","  "],
          ["P1","P1","P1","P1","P1","P1","P1","P1"],
          ["T1","C1","F1","D1","R1","F1","C1","T1"]]
    order=["R","D","F","C","T","P"]
    plat=copy.deepcopy(base)
    def Players():
        for i in range(len(plat)):
            for j in range(len(plat[0])):
                if plat[i][j]!="  ":
                    if plat[i][j][1]=="1":
                        midiout.send_message([0x90,pospad[i][j],colorp1])
                    elif plat[i][j][1]=="2":
                        midiout.send_message([0x90,pospad[i][j],colorp2])
                else: midiout.send_message([0x90,pospad[i][j],0])
    def printGame():
        global order
        p1pieces=["♔","♕","♗","♘","♖","♙"]
        p2pieces=["♚","♛","♝","♞","♜","♟"]
        print("\n")
        print('----------------------')
        for i in range(len(plat)):
            for j in range(len(plat[0])):
                if plat[i][j]!="  ":
                    if plat[i][j][1]=="1":
                        print('|'+p1pieces[order.index(plat[i][j][0])],end='')
                    elif plat[i][j][1]=="2":
                        print('|'+p2pieces[order.index(plat[i][j][0])],end='')
                else:
                    if j&1==0: print('|     ',end='')
                    elif j&1==1: print('|    ',end='')
            print('|')
            print('----------------------')
    midiout.send_message([176, 91, 5])
    midiout.send_message([176, 93, 0])
    midiout.send_message([176, 94, 13])
    touch=0
    pos=-1
    turn=int(plat[record[0][0][0]][record[0][0][1]][1])
    Players()
    printGame()
    while not touch==1:
        msg=midiin.get_message()
        if msg:
            if msg[0][2]!=0 and msg[0][0]==176:
                touch=msg[0][1]-90
                if touch==3:
                    rew=copy.deepcopy(base)
                    for i in range(pos):
                        rew[record[i][1][0]][record[i][1][1]]=rew[record[i][0][0]][record[i][0][1]]
                        rew[record[i][0][0]][record[i][0][1]]="  "
                    plat=copy.deepcopy(rew)
                    pos-=1
                    if pos<-1:
                        pos=-1
                        midiout.send_message([176, 93, 0])
                    else: midiout.send_message([176, 93, 13])
                    if pos==-1: midiout.send_message([176, 93, 0])
                    midiout.send_message([176, 94, 13])
                    Players()
                    printGame()
                elif touch==4:
                    if pos!=len(record)-1:
                        pos+=1
                        if pos>len(record)-1: pos=len(record)-1
                        plat[record[pos][1][0]][record[pos][1][1]]=plat[record[pos][0][0]][record[pos][0][1]]
                        plat[record[pos][0][0]][record[pos][0][1]]="  "
                        if pos==len(record)-1: midiout.send_message([176, 94, 0])
                        else: midiout.send_message([176, 94, 13])
                    midiout.send_message([176, 93, 13])
                    Players()
                    printGame()
                    
    midiout.send_message([176, 91, 0])
    midiout.send_message([176, 93, 0])
    midiout.send_message([176, 94, 0])
