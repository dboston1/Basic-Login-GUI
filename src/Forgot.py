
import smtplib, ssl

class Forgot:

    def __init__(self):
        #TODO: fill with garbage values
        self.password = "pinkpoodle"
        self.email = "test.app10097@gmail.com"
    
        with smtplib.SMTP("smtp.gmail.com") as self.server:
            self.server.starttls()
            self.server.login(self.email, self.password)
            

    
    def genUserMessage(self, app, email):
        username = ""
        for l in app._loginData._loginInfo.values():
            print(str(l))
            temp_email = l[1]   #l has format [password, email]
            if temp_email == email:
                username = l[0]
                break
        if username is not "":
            message = "\nSubject: Forgotten Username\n\nHello,\nYour username is: " + str(username) + "\n\nThank you!\n  -DB"
            return message
        else:
            print("error")
            #TODO: no account associated with this email address
            pass 
            
            
        #send email with username 
    def forgotUsername(self, app, email):
        message = str(self.genUserMessage(app, email))
        print("message: " + str(message))
        self.server.sendmail(self.email, email, message)
        #TODO: display message notifying email has been sent
        
        
        #send email with temporary password (reset to some random value)
    def forgotPassword(self, app, username):
        pass


#when user has forgotten their username, confirm email address, then send email
#def forgotUsername(app):
#    print("forgot username")
#    pass

#confirm email address, then send email
#def forgotPassword(app, username):
#    print("user: \'" + str(username) + "\' forgot password")
#    pass

