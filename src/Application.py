import tkinter as tk
from PIL import ImageTk, Image
import parseInput
import LoginData
import NewUser
import hashlib
import Login
import Forgot

## TODO: 

    # finish "forgot username / password" screenss
    # create email options (send username / password to email on file if not NA)
    #check all files for todo flags


class Application:
    
    def __init__(self):
        #setup window basics
        self.window = tk.Tk()
        self.window.minsize(480,480)
        self.window.maxsize(480,480)
        self.window.resizable(width = False, height = False)
        
        self._login = Login.Login()
        self._loginData = LoginData.LoginData()
        self._forgot = Forgot.Forgot()
        
        #load image files
        self.getImages()
        
        
    #load / process all images at start (consistent reference to prevent premature gc)
    def getImages(self):
        #first image is "header" image for login pages:
        img_temp = Image.open("background_top.jpg")
        img_temp = img_temp.resize((480, 240), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img_temp)
        
        #second image is the opening gif (played at startup):
        gif = Image.open("greeting.gif")
        self.gif_frames = []
        try:    
            while True:
                gif_temp = gif.copy().resize((480, 480), Image.ANTIALIAS)
                gif_ph = ImageTk.PhotoImage(gif_temp)
                self.gif_frames.append(gif_ph)
                gif.seek(len(self.gif_frames)) #get next frame
        except EOFError:
            pass    #no more frames in gif 
        
        #third image is when an invalid username is entered (one containing characters not allowed)
        img_temp = Image.open("didYouMean.jpg")
        img_temp = img_temp.resize((480, 480), Image.ANTIALIAS)
        self.didYouMean_image = ImageTk.PhotoImage(img_temp)
        
        #fourth image is used when a new user is created
        img_temp = Image.open("newUser.jpg")
        img_temp = img_temp.resize((480, 480), Image.ANTIALIAS)
        self.newUser_image = ImageTk.PhotoImage(img_temp)
        
        #fifth image is also used when a new user is created (check mark)
        img_temp = Image.open("checkMark.jpg")
        img_temp = img_temp.resize((15, 16), Image.ANTIALIAS)
        self.checkMark_image = ImageTk.PhotoImage(img_temp)
        
        #sixth image is a 'back' image (go to previous screen)
        img_temp = Image.open("back.jpg")
        img_temp = img_temp.resize((15, 16), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(img_temp)
    
    
    #update method to display gif
    def playGif(self, idx):
        try:
            nextFrame = self.gif_frames[idx]
            idx += 1
            self.gif_label.configure(image = nextFrame)
            self.window.after(60, self.playGif, idx)
        except IndexError:
            self.gif_label.destroy()    #no more frames in gif 
        
        
    #initialize startup gif:
    def startupGif(self):
        self.gif_label = tk.Label(self.window)
        self.gif_label.pack()
        self.window.after(0, self.playGif, 0)
    
    
    def displayCoverImage(self):
        self.cover_label = tk.Label(self.window, image = self.background_image)
        self.cover_label.pack()
     
    
    #used by entry boxes for username / email, removes placeholder text and allows regular user input (visible input)
    def handleFocus(self, event):
        event.widget.delete(0, 'end')
        event.widget['fg'] = "black"
        event.widget['font'] = ("Calibri", 10) 
    
    
    #used by entry boxes for password, removes placeholder text and allows hidden user input ('*')
    def handlePassFocus(self, event):
        event.widget.delete(0, 'end')
        event.widget['fg'] = "black"
        event.widget['font'] = ("Calibri", 10) 
        event.widget.configure(show = "*")
    

#entry function
def main():
    app = Application()
    #display startup gif
    app.startupGif()
    #entry points to program; cover image (top frame) and request username
    Login.requestUsername(app)
    tk.mainloop()


#call main (starting / entry) function   
if __name__ == '__main__':
    main()
