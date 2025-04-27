#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from snake_game import *
from tic_tac_toe import *

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # typing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
  
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False) # to make it resizable
        self.Window.configure(width = 470, # change the chat window size
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the typing box
        # into the gui window
        self.entryMsg.place(relwidth = 0.6,
                            relheight = 0.03,
                            rely = 0.008,
                            relx = 0.15)
          
        self.entryMsg.focus()

        # create a tic tac toe button
        self.tic_tac_toe = Button(self.labelBottom,
                                text = "Tic",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.ticButton())
        
        # place the tic tac toe button
        self.tic_tac_toe.place(relx = 0.01,
                                rely = 0.008,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        # place the Send button
        self.buttonMsg.place(relx = 0.71,
                             rely = 0.008,
                             relheight = 0.03, 
                             relwidth = 0.11)
          
        self.textCons.config(cursor = "arrow")

        # create a scores button
        self.scores = Button(self.labelBottom,
                                text = "Scores",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("scores"))
        
        # place the scores button
        self.scores.place(relx = 0.85,
                                rely = 0.008,
                                relheight = 0.03, 
                                relwidth = 0.11)
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)

        # create a button for time
        self.time = Button(self.labelBottom,
                                text = "Time",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("time"))
        
        # place time button
        self.time.place(relx = 0.01,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
        # create a button for who
        self.who = Button(self.labelBottom,
                                text = "Who",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("who"))
        
        # place the Who button
        self.who.place(relx = 0.15,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)

        # create a button for quit
        self.quit = Button(self.labelBottom,
                                text = "Quit",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("q"))
        
        # place the quit button
        self.quit.place(relx = 0.29,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
        # create a button for search
        self.search = Button(self.labelBottom,
                                text = "Search",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("? " + self.entryMsg.get()))
        
        # place the search button
        self.search.place(relx = 0.43,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
        # create a button for sonnet
        self.sonnet = Button(self.labelBottom,
                                text = "Sonnet",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("p" + self.entryMsg.get()))
        
        # place the sonnet button
        self.sonnet.place(relx = 0.57,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
        # create a button for connect
        self.connect = Button(self.labelBottom,
                                text = "Connect",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton("c " + self.entryMsg.get()))
        
        # place the connect button
        self.connect.place(relx = 0.71,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)
        
        # create a button for snake game
        self.snake = Button(self.labelBottom,
                                text = "Snake",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.gameButton())
        
        # place the snake button
        self.snake.place(relx = 0.85,
                                rely = 0.042,
                                relheight = 0.03, 
                                relwidth = 0.11)

    # create a new window for snake game
    def gameButton(self):
        self.game_window = Toplevel()
        self.game_window.title("Snake Game")
        self.game_window.resizable(width = False, 
                             height = False)
        self.game_window.configure(width = 500,
                             height = 500)
        # create a canvas for the snake game
        self.canvas = Canvas(self.game_window, bg = "black", height = 500, width = 500)
        self.canvas.pack()
        # start the snake game
        SnakeGame(self.game_window, self.canvas)


    # start tic tac toe game
    def ticButton(self):
        tic_play()

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)


    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                self.system_msg = ""

    def searchButton(self):
        self.textCons.config(state = DISABLED)
        self.my_msg = "? " + self.entryMsg.get()
        self.entryMsg.delete(0, END)

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__": 
    # g = GUI()
    pass