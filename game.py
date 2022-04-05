
from audioop import minmax
from pickle import FALSE, TRUE
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import *
import asyncio
import nest_asyncio
import time
import datetime
from threading import Thread
nest_asyncio.apply()
totalScore = 0;
UI_names = ["mainmenu.ui","gamepage.ui"];
UI = [];

players = ["","BOT"];
allInts = [1,2,3];
maxScore = 21;

turn = 0;

def minimax(pos, total, maximizeMinimizePlayer):
    if(total>=21 and maximizeMinimizePlayer):
        return -1;
    elif(total>=21 and maximizeMinimizePlayer==False):
        return 1;
    if(maximizeMinimizePlayer):
        bestScore = -9999;
        for i in allInts:
            mx = minimax(i,total+i, False);
            if(bestScore<mx):
                bestScore = mx;
        return bestScore;
    else:
        bestScore = 9999;
        for i in allInts:
            mx = minimax(i,total+i, True);
            if(bestScore>mx):
                bestScore = mx;
        return bestScore;

def doMove():
    global turn;
    global totalScore;

    if(turn==0): 
        return;
    mxPoint = -99999;
    nextInt = 3;
    for i in allInts:
        mx = minimax(i, totalScore+i, False);
        if(mxPoint<mx):
            mxPoint = mx;
            nextInt = i;
    time.sleep(1);
    increseScore(nextInt);

def disableButtons(x):
    UI[1].button2.setEnabled(x)
    UI[1].button1.setEnabled(x)
    UI[1].button3.setEnabled(x)


def debugger(title, message):
    QMessageBox.information(None, title, message);

def startUI():
    for i in UI_names:
        UI_temp = uic.loadUi("screens/"+i);
        UI.append(UI_temp);

def switchUI(id):
    global players;

    players[0] = UI[0].NameText.text();
    for i in UI:
        i.hide();
    UI[id].show();
    UI[1].playername.setText(players[0]);

def increseScore(value):
    global totalScore;
    global players;
    global turn;
    totalScore+=value;
    UI[1].totalSum.setText(str(totalScore));
    if(totalScore>=21):
        switchUI(0);
        debugger("Game Over!", "WINNER IS "+players[turn]);
        resetTable();
    else:
        turn = (turn +1)%2;
        Thread(target=doMove).start()
        disableButtons(turn==0 and True or False)

def resetTable():
    global totalScore;
    global players;
    global turn;
    turn =0;
    totalScore = 0;
    UI[1].totalSum.setText(str(0));
    disableButtons(True);



app = QtWidgets.QApplication([]);

startUI();
UI[0].buttonOK.clicked.connect(lambda: switchUI(1));

UI[1].button2.clicked.connect(lambda: increseScore(2));
UI[1].button1.clicked.connect(lambda: increseScore(1));
UI[1].button3.clicked.connect(lambda: increseScore(3));
UI[1].totalSum.setText(str(totalScore));
switchUI(0);
app.exec();

