import os

## Obviously this is not secure, as it relies on the file ".data", which is located on the host device. In a more realistic application, it should communicate with
# a server that is inaccessible to the user (so it cannot be inappropriately modified). Of course, if we go down this rabbit-hole, python is easy to 'decompile' from an executable, 
# where it could be modified to forgo password checks completely. So, take the "security" of this program with a (rather large) grain of salt. 

class LoginData():
    
    def __init__(self):
        self._filename = ".data"
        self._loginInfo = {}
        
        self.checkFileExists()
        self.readFromFile()
        
    
    #ensure .data file exists, create it if not:
    def checkFileExists(self):
        if not os.path.exists(self._filename):
            with open(self._filename, "w") as f:
                pass
     
    #initialize loginInfo from .data file 
    def readFromFile(self):
        with open(self._filename, "r") as f:
            line = f.readline()
            while line is not "":
                try:
                    un, pw, email = line.split("\t")
                    self._loginInfo[un] = [pw, email]
                except ValueError:
                    print(".data file corrupted")
                    pass
                line = f.readline()
    
    #check if a username exists
    def userExists(self, valid_username):
        if valid_username in self._loginInfo:
            return True
        return False
    
    
    #add a username / password 
    def createUser(self, valid_username, hash_password, valid_email = "NA"):
        if self.userExists(valid_username):
            print("user \'" + str(valid_username) + "\' already exists")
            return False
        self._loginInfo[valid_username] = [hash_password, valid_email]
        with open(self._filename, "a") as f:
            f.write(str(valid_username) + "\t" + str(hash_password) + "\t" + str(valid_email) + "\n")
        return True
    
    
    #called by create new username; if username not available, suggest three alternatives
    #check for length of original username (can't exceed 12)
    def suggestAlternativeUsernames(self, valid_username):
        return ["option1", "option2", "option3"]
    

#for testing        
if __name__ == '__main__':
    login = LoginData()
    login.createUser("admin", "password")
    login.createUser("bob", "bananas")
    
        
