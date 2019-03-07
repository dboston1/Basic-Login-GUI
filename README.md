This is a basic username / password login program, mostly used to experiment with Python's Tkinter GUI tools.

As this is my first project attempting a GUI, I expect it is not very well done - if you notice any blatant mistakes or ways I could have simplified things, feel free to let me know! :)

To run the code from a terminal, use: 

python3 Application.py 

Otherwise, run Application.py from any python 3 IDE.

It is also a work in progress, so it currently displays only a white screen after a successful login. I have ideas of implementing a basic Snake game or something similar, but I'll figure it out after I get some free time. Also, the "Forgot Username / Password" functionality is not currently implemented. Other than that, it is fully functional! You will need to create a user in order to successfully login for the first time.

**PLEASE NOTE** - this is in no way meant to be a secure program. While it does store passwords encrypted with MD5 (debatable, I know), it saves them in an easily accessible .data file located in the same directory you run the program from, as I didn't plan to utilize a server. 

If accessed, it would be relatively straightforward to run a dictionary attack on this file (which doesn't use salt, either as that was not the point of this project) and all data would be compromised. So, don't use real data. You've been warned :)
