import tkinter as tk
import parseInput
import LoginData
import NewUser
import hashlib
import Application
import Forgot

#TODO: possibly limit login attempts over so much time? i.e. 3 login attempts per minute?

#stores current username and hashed password
class Login():
    
    def __init__(self):
        self._USERNAME = ""
        self._PASSWORD = ""  
        self._EMAIL = ""
    
    def setUsername(self, username):
        self._USERNAME = username
    
    def getUsername(self):
        return self._USERNAME
    
    def setPassword(self, password):
        h = hashlib.md5()
        h.update(password.encode("utf-8"))
        hash_password = h.hexdigest()
        self._PASSWORD = hash_password
        
    def getPassword(self):
        return self._PASSWORD
    
    def clear(self):
        self._USERNAME = ""
        self._PASSWORD = ""
        self._EMAIL = ""
        
        
#entry method to display login screen - contains links to create new user and forgot username as well
def requestUsername(app):
    app.displayCoverImage()
    app.bottom_frame = tk.Frame(app.window, width = 480, bg = "DarkOliveGreen4", height = 240)
    app.bottom_frame.pack(fill = "both", expand = True)
        
    #formatting / entry etc
    app.greet = tk.Label(app.bottom_frame, text = "\nHello!\n", font = ("times new roman", 30, "bold"), fg = "black", bg = "DarkOliveGreen4")
    app.greet.pack(anchor = "n", fill = "both")
    prompt = tk.Label(app.bottom_frame, text = "Please Enter Your Username", font = ("calibri", 15), bg = "dark khaki", fg = "white")
    prompt.pack(anchor = "n", fill = "both")
    unEntry = tk.Entry(app.bottom_frame, width=19)
    unEntry.pack()
    unEntry.insert(0, "username")
    unEntry['fg'] = "grey"
    unEntry['font'] = ("Calibri", 10, "italic")
    unEntry.bind("<FocusIn>", app.handleFocus)
    unEntry.bind("<Return>", lambda event, arg = app: onEnterUsername(arg, unEntry.get()))
        
    newUserLink = tk.Label(app.bottom_frame, text = "Create New User", bg = "DarkOliveGreen4", fg = "gray20", borderwidth = 2, relief = "groove", font = ("times new roman", 12), highlightcolor = "black")
    newUserLink.configure(width = 16)
    newUserLink.pack(anchor = "n", pady = 28)
    newUserLink.bind("<Button-1>", lambda event, arg = app: NewUser.createNewUser(arg))
        
    newUserLink2 = tk.Label(app.bottom_frame, text = "Forgot Username?", bg = "DarkOliveGreen4", fg = "navy", font = ("times new roman", 12, "italic"))
    newUserLink2.configure(width = 16)
    newUserLink2.place(anchor = "se", x = 430, y = 157)
    newUserLink2.bind("<Button-1>", lambda event, arg = app: app._forgot.forgotUsername(arg, "dz.1767@gmail.com"))
    

#if username doesn't exist in app._loginData:
#note; all labels / canvases are destroyed prior to this method (guaranteed)
def usernameNotFound(app, username):
    requestUsername(app)
    #now override "Hello" label with custom message
    app.greet["text"] = "\nUsername " + str(username) + " Not Found\n"
    app.greet["font"] = ("times new roman", 30, "bold")


#check if entered username is valid and exists in _loginData
def onEnterUsername(app, username):
    if username != "":
        valid_username = parseInput.parseUsername(username)
        if username == valid_username:
            if valid_username in app._loginData._loginInfo:
                print("valid, existing username: " + valid_username)
                app._login.setUsername(valid_username)
                app.greet = None
                if hasattr(app, "cover_label"):
                    if app.cover_label is not None:
                        app.cover_label.destroy()
                        app.coverlabel = None
                if hasattr(app, "bottom_frame"):
                    if app.bottom_frame is not None:
                        app.bottom_frame.destroy()
                        app.bottom_frame = None
                requestPassword(app, valid_username)
                
                
            else:
                print("username not on file")
                #destroy current labels if they exist
                if hasattr(app, "cover_label"):
                    if app.cover_label is not None:
                        app.cover_label.destroy()
                        app.coverlabel = None
                if hasattr(app, "bottom_frame"):
                    if app.bottom_frame is not None:
                        app.bottom_frame.destroy()
                        app.bottom_frame = None
                usernameNotFound(app, valid_username)
                
        else:
            didYouMean(app, valid_username)
            print("invalid username: " + str(username))
    

#TODO: implement forgotUsername feature   
def forgotUsername(app):
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
    app.unEntry = None
    app.prompt = None
    #TODO: ask for email, check if its valid
    
    app._forgot.forgotUsername(app, email)


#TODO: implement forgotPassword feature
def forgotPassword(app, username):
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
    app.unEntry = None
    app.prompt = None
    app._forgot.forgotPassword(app, username)
    
    
#removes non-alphanumeric characters from inputted username and asks if that is what the user meant to enter
def didYouMean(app, valid_username):
    #destroy current labels
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
    
    #display new background:
    app.DYM_canvas = tk.Canvas(app.window, width = 480, height = 480)
    app.DYM_canvas.pack()
    app.DYM_canvas.create_image(0, 0, image = app.didYouMean_image, anchor = "nw")
        
    #overlay text:
    DYM_canvasText1 = app.DYM_canvas.create_text(60, 85, anchor = "nw")
    app.DYM_canvas.itemconfig(DYM_canvasText1, text = "Oops!", font = ("courier", 55, "italic"), fill = "white")
        
    DYM_canvasText2 = app.DYM_canvas.create_text(60, 180, anchor = "nw")
    app.DYM_canvas.itemconfig(DYM_canvasText2, text = "Usernames must be alphanumeric and", font = ("courier", 14), fill = "white")
        
    DYM_canvasText2_b = app.DYM_canvas.create_text(80, 200, anchor = "nw")
    app.DYM_canvas.itemconfig(DYM_canvasText2_b, text = "twelve characters or less.", font = ("courier", 14), fill = "white")
        
    DYM_canvasText3 = app.DYM_canvas.create_text(50, 260, anchor = "nw")
    app.DYM_canvas.itemconfig(DYM_canvasText3, text = "Did You Mean", font = ("courier", 25), fill = "white")
        
    DYM_canvasText4 = app.DYM_canvas.create_text(240, 260, anchor = "nw")
    app.DYM_canvas.itemconfig(DYM_canvasText4, text = valid_username + " ?", font = ("courier", 25), fill = "deep sky blue")
        
    button1 = tk.Button(app.window, text = "Yes", command = lambda arg1 = app, arg2 = valid_username: DYM_Yes(arg1, arg2), anchor = "w", highlightbackground = "saddle brown")
    button1.configure(width = 8)
    button1_window = app.DYM_canvas.create_window(120, 340, anchor="nw", window=button1)

    button2 = tk.Button(app.window, text = "No", command = lambda arg = app: DYM_No(arg), anchor = "e", highlightbackground = "saddle brown")
    button2.configure(width = 8)
    button2_window = app.DYM_canvas.create_window(360, 340, anchor="ne", window=button2)    
    

#update method for "did you mean" upon clicking no
def DYM_No(app):
    print("DYM_NO")
    #destroy current labels
    app.DYM_canvas.destroy()
    app.DYM_canvas = None
    requestUsername(app)
    
    
#update method for "did you mean" upon clicking yes
def DYM_Yes(app, username):
    print("DYM_YES")
    #destroy current labels
    app.DYM_canvas.destroy()
    app.DYM_canvas = None
    onEnterUsername(app, username)


#check if correct password was entered
def onEnterPassword(app, username, password):
    if password != "":
        if parseInput.isValidPw(password):
            h = hashlib.md5()
            h.update(password.encode("utf-8"))
            hash_password = h.hexdigest()
            
            if app._loginData._loginInfo[username][0] == hash_password:
                print("correct password - logging in")
                #destroy current frames
                if hasattr(app, "cover_label"):
                    if app.cover_label is not None:
                        app.cover_label.destroy()
                        app.coverlabel = None
                if hasattr(app, "bottom_frame"):
                    if app.bottom_frame is not None:
                        app.bottom_frame.destroy()
                        app.bottom_frame = None
                app.unEntry = None
                app.prompt = None
                #TODO: move to successive state (logged in)
            else:
                print("incorrect password")
                app.prompt["text"] = "Incorrect Password; Try Again"
                app.prompt["fg"] = "red4"
                
                app.unEntry.delete(0, "end")
                app.unEntry.focus()
        else:
            print("invalid password")
            app.prompt["text"] = "Passwords must be 5-12 Characters Long"
            app.prompt["fg"] = "red4"
                
            app.unEntry.delete(0, "end")
            app.unEntry.focus()


def exitPasswordScreen(app):
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
    app.prompt = None
    app.unEntry = None
    requestUsername(app)


#ask user for password - contains links to create new user and forgot password as well
def requestPassword(app, username):
    #destroy current frames
    if hasattr(app, "cover_label"):
        if app.cover_label is not None:
            app.cover_label.destroy()
            app.cover_label = None
    if hasattr(app, "bottom_frame"):
        if app.bottom_frame is not None:
            app.bottom_frame.destroy()
            app.bottom_frame = None
    
    app.displayCoverImage()
    app.bottom_frame = tk.Frame(app.window, width = 480, bg = "DarkOliveGreen4", height = 240)
    app.bottom_frame.pack(fill = "both", expand = True)
        
    #formatting / entry etc
    greet = tk.Label(app.bottom_frame, text = "\nHello " + str(username) + "!\n", font = ("times new roman", 30, "bold"), fg = "black", bg = "DarkOliveGreen4")
    greet.pack(anchor = "n", fill = "both")
    app.prompt = tk.Label(app.bottom_frame, text = "Please Enter Your Password", font = ("calibri", 15), bg = "dark khaki", fg = "white")
    app.prompt.pack(anchor = "n", fill = "both")
    app.unEntry = tk.Entry(app.bottom_frame, width=19)
    app.unEntry.pack()
    app.unEntry.insert(0, "password")
    app.unEntry['fg'] = "grey"
    app.unEntry['font'] = ("Calibri", 10, "italic")
    app.unEntry.bind("<FocusIn>", app.handlePassFocus)
    app.unEntry.bind("<Return>", lambda event, arg1 = app, arg2 = username: onEnterPassword(arg1, arg2, app.unEntry.get()))
    
    backLink = tk.Button(app.bottom_frame, command = lambda: exitPasswordScreen(app), image = app.back_image, highlightbackground = "saddle brown")
    backLink.configure(borderwidth = 0)
    backLink.place(anchor = "center", x = 450, y = 25)
    
    newUserLink = tk.Label(app.bottom_frame, text = "Create New User", bg = "DarkOliveGreen4", fg = "gray20", borderwidth = 2, relief = "groove", font = ("times new roman", 12), highlightcolor = "black")
    newUserLink.configure(width = 16)
    newUserLink.pack(anchor = "n", pady = 28)
    newUserLink.bind("<Button-1>", lambda event, arg = app: NewUser.createNewUser(arg))
        
    newUserLink2 = tk.Label(app.bottom_frame, text = "Forgot Password?", bg = "DarkOliveGreen4", fg = "navy", font = ("times new roman", 12, "italic"))
    newUserLink2.configure(width = 16)
    newUserLink2.place(anchor = "se", x = 430, y = 157)
    newUserLink2.bind("<Button-1>", lambda event, arg1 = app, arg2 = username: forgotPassword(arg1, arg2))
    
    
    
