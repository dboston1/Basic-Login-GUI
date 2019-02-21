import tkinter as tk
from PIL import ImageTk, Image
import parseInput
import LoginData, Login
import Application
import parseInput
    

#suggest three alternatives if original username is not available
def suggestAlternateUsernames(app, valid_username):
    print("suggesting three alternative usernames")
    if hasattr(app, "notify"):
        if app.notify is not None:
            app.newUser_canvas.delete(app.notify)
    app.notify = app.newUser_canvas.create_rectangle(210, 300, 435, 380, fill="DarkOliveGreen4")
    newUser_canvasText2 = app.newUser_canvas.create_text(213, 303, anchor = "nw")
    app.newUser_canvas.itemconfig(newUser_canvasText2, text = "Username " + str(valid_username), font = ("courier", 12, "italic"), fill = "red4")
    newUser_canvasText3 = app.newUser_canvas.create_text(213, 318, anchor = "nw")
    app.newUser_canvas.itemconfig(newUser_canvasText3, text = "is not available. Alternatives:", font = ("courier", 12, "italic"), fill = "red4")
    options = app._loginData.suggestAlternativeUsernames(valid_username)
    
    ypos = 333
    idx = 0
    app.labels = []
    for username in options:
        app.labels.append( app.newUser_canvas.create_text(228, ypos, anchor = "nw"))
        app.newUser_canvas.itemconfig(app.labels[idx], text = str(username), font = ("courier", 12, "italic"), fill = "white")
        app.newUser_canvas.tag_bind(app.labels[idx], '<ButtonPress-1>', lambda event, arg = app, arg2 = username: createUsername(arg, arg2))  
        ypos += 15
        idx += 1
        
    
#check if new username is available   
def createUsername(app, username):
    if username != "":
        valid_username = parseInput.parseUsername(username)
        if username == valid_username:
            if not app._loginData.userExists(valid_username):
                #username is available
                app._login.setUsername(valid_username)
                app.unEntry = None
                app.notify = None
                app.labels = None
                createNewPassword(app)
            else:
                suggestAlternateUsernames(app, valid_username)
        else:
            if hasattr(app, "notify"):
                if app.notify is not None:
                    app.newUser_canvas.delete(app.notify)
                    if hasattr(app, "labels"):
                        if app.labels is not None:
                            for label in app.labels:
                                app.newUser_canvas.delete(label)
            app.notify = app.newUser_canvas.create_rectangle(210, 300, 430, 334, fill="DarkOliveGreen4")
            newUser_canvasText2 = app.newUser_canvas.create_text(213, 303, anchor = "nw")
            app.newUser_canvas.itemconfig(newUser_canvasText2, text = "Usernames must be alphanumeric", font = ("courier", 12, "italic"), fill = "red4")
            newUser_canvasText3 = app.newUser_canvas.create_text(223, 318, anchor = "nw")
            app.newUser_canvas.itemconfig(newUser_canvasText3, text = "and 12 characters or less.", font = ("courier", 12, "italic"), fill = "red4")
            app.unEntry.delete(0, "end")
            app.unEntry.focus()


#create a new username
def createNewUser(app):
    print("creating new user")
    #destroy current frames
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
        
    #display new background:
    app.newUser_canvas = tk.Canvas(app.window, width = 480, height = 480)
    app.newUser_canvas.pack()
    app.newUser_canvas.create_image(0, 0, image = app.newUser_image, anchor = "nw")
        
    newUser_canvasText2 = app.newUser_canvas.create_text(217, 190, anchor = "nw")
    app.newUser_canvas.itemconfig(newUser_canvasText2, text = "Pick A Username!", font = ("courier", 22), fill = "white")
        
    button1 = tk.Button(app.window, command = lambda: createUsername(app, app.unEntry.get()), anchor = "w", highlightbackground = "saddle brown", image = app.checkMark_image)
    button1.configure(borderwidth = 0)
    button1_window = app.newUser_canvas.create_window(375, 260, anchor="nw", window=button1)
    
    backLink = tk.Button(app.newUser_canvas, command = lambda: exitUsernameScreen(app), image = app.back_image, highlightbackground = "saddle brown")
    backLink.configure(borderwidth = 0)
    backLink.place(anchor = "center", x = 450, y = 25)
        
    app.unEntry = tk.Entry(app.window, width = 19)
    app.unEntry.insert(0, "username")
    app.unEntry['fg'] = "grey"
    app.unEntry['font'] = ("Calibri", 10, "italic")
    app.unEntry.bind("<FocusIn>", app.handleFocus)
    app.unEntry.bind("<Return>", lambda event, arg = app: createUsername(arg, app.unEntry.get()))        
    app.unEntry_window = app.newUser_canvas.create_window(240, 260, anchor="nw", window=app.unEntry)
    

#if back button or error creating user from username screen
def exitUsernameScreen(app):
    app.newUser_canvas.destroy()
    app.unEntry = None
    app.notify = None
    app.labels = None
    app._login.clear()
    Login.requestUsername(app)


#if back button or error creating user from password screen
def exitPasswordScreen(app):
    app.newPass_canvas.destroy()
    app.unEntry = None
    app.unEntry2 = None
    app._login.clear()
    Login.requestUsername(app)
 

#handle case passwords don't match
def passwordsDidntMatch(app):
    print("passwords didn't match")
    #insert notification window, then recall createNewPassword(app):
    
    if hasattr(app, "notify"):
        if app.notify is not None:
            app.newPass_canvas.delete(app.notify)
            app.newPass_canvas.delete(app.newPass_notifyText1)
            app.newPass_canvas.delete(app.newPass_notifyText2)
        
    
    app.notify = app.newPass_canvas.create_rectangle(240, 340, 398, 360, fill="DarkOliveGreen4")
    
    newPass_canvasText2 = app.newPass_canvas.create_text(250, 343, anchor = "nw")
    app.newPass_canvas.itemconfig(newPass_canvasText2, text = "Passwords must match", font = ("courier", 12, "italic"), fill = "red4")
    
    #clear currently entered passwords
    app.unEntry2.delete(0, "end")
    app.unEntry.delete(0, "end")
    app.unEntry.focus()


#password must be between five and twelve characters
def invalidPassword(app):
    print("invalid password")
    #insert notification window, then recall createNewPassword(app):
    
    if hasattr(app, "notify"):
        if app.notify is not None:
            app.newPass_canvas.delete(app.notify)
    
    
    app.notify = app.newPass_canvas.create_rectangle(227, 340, 410, 373, fill="DarkOliveGreen4")
    
    app.newPass_notifyText1 = app.newPass_canvas.create_text(230, 343, anchor = "nw")
    app.newPass_canvas.itemconfig(app.newPass_notifyText1, text = "Passwords must be between", font = ("courier", 12, "italic"), fill = "red4")
    
    app.newPass_notifyText2 = app.newPass_canvas.create_text(230, 358, anchor = "nw")
    app.newPass_canvas.itemconfig(app.newPass_notifyText2, text = "5 and 12 characters long", font = ("courier", 12, "italic"), fill = "red4")
    
    #clear currently entered passwords
    app.unEntry2.delete(0, "end")
    app.unEntry.delete(0, "end")
    app.unEntry.focus()
    
    
#handle password entry (move to next step or handle mismatch)    
def createPassword(app, password1, password2):
    print("checking passwords match")
    if parseInput.isValidPw(password1) and parseInput.isValidPw(password2):
        if password1 == password2:
            app._login.setPassword(password1)
            app.unEntry = None
            app.unEntry2 = None
            app.notify = None
            app.newPass_notifyText1 = None
            app.newPass_notifyText2 = None
            createNewEmail_step1(app)
        else:
            passwordsDidntMatch(app)
    else:
        invalidPassword(app)
 
 
#ask for password
def createNewPassword(app):
    print("ask for new password")
    #destroy current frames
    app.newUser_canvas.destroy()
        
    #display new background:
    app.newPass_canvas = tk.Canvas(app.window, width = 480, height = 480)
    app.newPass_canvas.pack()
    app.newPass_canvas.create_image(0, 0, image = app.newUser_image, anchor = "nw")
        
    newPass_canvasText2 = app.newPass_canvas.create_text(227, 170, anchor = "nw")
    app.newPass_canvas.itemconfig(newPass_canvasText2, text = "Hi " + str(app._login.getUsername()) + ",", font = ("courier", 26), fill = "white")
    
    newPass_canvasText3 = app.newPass_canvas.create_text(205, 210, anchor = "nw")
    app.newPass_canvas.itemconfig(newPass_canvasText3, text = "Please Pick A Password!", font = ("courier", 18), fill = "white")
        
    button1 = tk.Button(app.window, command = lambda: createPassword(app, app.unEntry.get(), app.unEntry2.get()), anchor = "w", highlightbackground = "saddle brown", image = app.checkMark_image)
    button1.configure(borderwidth = 0)
    button1_window = app.newPass_canvas.create_window(375, 300, anchor="nw", window=button1)
    
    backLink = tk.Button(app.newPass_canvas, command = lambda: exitPasswordScreen(app), image = app.back_image, highlightbackground = "saddle brown")
    backLink.configure(borderwidth = 0)
    backLink.place(anchor = "center", x = 450, y = 25)
        
    app.unEntry2 = tk.Entry(app.window, width = 19)
    app.unEntry = tk.Entry(app.window, width = 19)
    
    app.unEntry.insert(0, "password")
    app.unEntry['fg'] = "grey"
    app.unEntry['font'] = ("Calibri", 10, "italic")
    app.unEntry.bind("<FocusIn>", app.handlePassFocus)
    app.unEntry.bind("<Return>", lambda c: app.unEntry2.focus())
    app.unEntry_window = app.newPass_canvas.create_window(240, 260, anchor="nw", window=app.unEntry)
    
    app.unEntry2.insert(0, "confirm password")
    app.unEntry2['fg'] = "grey"
    app.unEntry2['font'] = ("Calibri", 10, "italic")
    app.unEntry2.bind("<FocusIn>", app.handlePassFocus)
    app.unEntry2.bind("<Return>", lambda event, arg = app: createPassword(arg, app.unEntry.get(), app.unEntry2.get()))
    app.unEntry_window2 = app.newPass_canvas.create_window(240, 300, anchor="nw", window=app.unEntry2)


#ask if user would like to set a recovery email address
def createNewEmail_step1(app):
    #destroy current frames
    app.newPass_canvas.destroy()
        
    #display new background:
    app.newEmail_canvas1 = tk.Canvas(app.window, width = 480, height = 480)
    app.newEmail_canvas1.pack()
    app.newEmail_canvas1.create_image(0, 0, image = app.didYouMean_image, anchor = "nw")
        
    #overlay text:
    newEmail_canvas1Text2 = app.newEmail_canvas1.create_text(25, 180, anchor = "nw")
    app.newEmail_canvas1.itemconfig(newEmail_canvas1Text2, text = "Would you like to set a username and", font = ("courier", 20), fill = "white")
        
    newEmail_canvas1Text2_b = app.newEmail_canvas1.create_text(50, 210, anchor = "nw")
    app.newEmail_canvas1.itemconfig(newEmail_canvas1Text2_b, text = "password recovery email address?", font = ("courier", 20), fill = "white")
        
    button1 = tk.Button(app.window, text = "Yes", command = lambda: createNewEmail_step2(app), anchor = "w", highlightbackground = "saddle brown")
    button1.configure(width = 8)
    button1_window = app.newEmail_canvas1.create_window(120, 340, anchor="nw", window=button1)

    button2 = tk.Button(app.window, text = "No", command = lambda: finalizeWithoutEmail(app), anchor = "e", highlightbackground = "saddle brown")
    button2.configure(width = 8)
    button2_window = app.newEmail_canvas1.create_window(360, 340, anchor="ne", window=button2)
    
    newEmail_canvas1Text3_b = app.newEmail_canvas1.create_text(80, 400, anchor = "nw")
    app.newEmail_canvas1.itemconfig(newEmail_canvas1Text3_b, text = "Usernames and Passwords are unrecoverable", font = ("courier", 13, "italic"), fill = "white")
    
    newEmail_canvas1Text3_b = app.newEmail_canvas1.create_text(140, 420, anchor = "nw")
    app.newEmail_canvas1.itemconfig(newEmail_canvas1Text3_b, text = "without an email address.", font = ("courier", 13, "italic"), fill = "white")
        

#exit to main screen if back button or error
def exitEmailScreen(app):
    app.newEmail_canvas.destroy()
    app.unEntry = None
    app.unEntry2 = None
    app._login.clear()
    Login.requestUsername(app)


#handle case emails don't match
def emailsDidntMatch(app):
    print("emails didn't match")
    #insert notification window, then recall createNewPassword(app):
    notify = app.newEmail_canvas.create_rectangle(240, 340, 433, 360, fill="DarkOliveGreen4")
    
    newEmail_canvasText2 = app.newEmail_canvas.create_text(250, 343, anchor = "nw")
    app.newEmail_canvas.itemconfig(newEmail_canvasText2, text = "Emails must match", font = ("courier", 12, "italic"), fill = "red4")
    
    #clear currently entered passwords
    app.unEntry2.delete(0, "end")
    app.unEntry.delete(0, "end")
    app.unEntry.focus()


#handle email input (create new user or handle mismatch)
def createEmail(app, email1, email2):
    print("checking emails match")
    if email1 != "" or email2 != "":
        if email1 == email2:
            app.unEntry = None
            app.unEntry2 = None
            finalizeWithEmail(app, email1)
        else:
            emailsDidntMatch(app)
        

#setup email address    
def createNewEmail_step2(app):
    #destroy current frames
    app.newEmail_canvas1.destroy()
        
    #display new background:
    app.newEmail_canvas = tk.Canvas(app.window, width = 480, height = 480)
    app.newEmail_canvas.pack()
    app.newEmail_canvas.create_image(0, 0, image = app.newUser_image, anchor = "nw")
        
    newEmail_canvas1Text2_b = app.newEmail_canvas.create_text(240, 180, anchor = "nw")
    app.newEmail_canvas.itemconfig(newEmail_canvas1Text2_b, text = "Please enter an", font = ("courier", 20), fill = "white")
    newEmail_canvas1Text2_b = app.newEmail_canvas.create_text(260, 210, anchor = "nw")
    app.newEmail_canvas.itemconfig(newEmail_canvas1Text2_b, text = "email address", font = ("courier", 20), fill = "white")
    
    button1 = tk.Button(app.window, command = lambda: createEmail(app, app.unEntry.get(), app.unEntry2.get()), anchor = "w", highlightbackground = "saddle brown", image = app.checkMark_image)
    button1.configure(borderwidth = 0)
    button1_window = app.newEmail_canvas.create_window(440, 300, anchor="nw", window=button1)
    
    backLink = tk.Button(app.newEmail_canvas, command = lambda: exitEmailScreen(app), image = app.back_image, highlightbackground = "saddle brown")
    backLink.configure(borderwidth = 0)
    backLink.place(anchor = "center", x = 450, y = 25)
    
    app.unEntry2 = tk.Entry(app.window, width = 30)
    app.unEntry = tk.Entry(app.window, width = 30)
    
    app.unEntry.insert(0, "email address")
    app.unEntry['fg'] = "grey"
    app.unEntry['font'] = ("Calibri", 10, "italic")
    app.unEntry.bind("<FocusIn>", app.handleFocus)
    app.unEntry.bind("<Return>", lambda c: app.unEntry2.focus())
    app.unEntry_window = app.newEmail_canvas.create_window(240, 260, anchor="nw", window=app.unEntry)
    
    app.unEntry2.insert(0, "confirm email address")
    app.unEntry2['fg'] = "grey"
    app.unEntry2['font'] = ("Calibri", 10, "italic")
    app.unEntry2.bind("<FocusIn>", app.handleFocus)
    app.unEntry2.bind("<Return>", lambda event, arg = app: createEmail(arg, app.unEntry.get(), app.unEntry2.get()))
    app.unEntry_window2 = app.newEmail_canvas.create_window(240, 300, anchor="nw", window=app.unEntry2)
 

#TODO: determine successive state (what comes next?)
#if successful, move to logged in screen
def exitSuccess(app):
    pass
   

#finish everything up (without email)
def finalizeWithoutEmail(app):
   #destroy current canvas
   app.newEmail_canvas1.destroy()
   
   #create new email with default email = "NA":
   app._loginData.createUser(app._login.getUsername(), app._login.getPassword())
   exitSuccess(app)
   
 
#finish everything up (with email)
def finalizeWithEmail(app, email):
    #destroy current canvas
    app.newEmail_canvas.destroy()
    
    #create new user with email address:
    app._loginData.createUser(app._login.getUsername(), app._login.getPassword(), email)
    exitSuccess(app)
    
