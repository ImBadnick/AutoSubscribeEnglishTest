# AutoSubscribeEnglishTest

Script used to autosubscribe to the english test of CLI using Universitary credentials to login in the CLI's eLearning.

## Description
It logs in the CLI's eLearning using the Universitary credentials. Then it clicks on the first link to subscribe. Then it repeats:
1) Check if the button used to subscribe to the exam is avaiable;
   - IF YES: SUBSCRIBE!
   - IF NOT: Go to the next subscribe page (clicking the right button in the bottom dx page)
2) do the (1) while the script is not at the last subscribe page. 
3) Wait 60s 
4) Do the same thing in (1) but going back (clicking the left button in the left sx page)


## HOW TO USE

### USE A VIRTUALENV

HOW TO INSTALL
1) Go to the program directory
2) Install:
    - Install a virtualenv: virtualenv "nome"
    - Activate a virtualenv: source bin/activate
    - Install Dependencies: pip install -r requirements.txt  

HOW TO USE (if virtualenv is not already activated):  source bin/activate

### USE THE SCRIPT

BEFORE USE THE SCRIPT **YOU MUST** CHANGE IN THE **bot.py** FILE THE 2 VARIABLES **self.username** and **self.password** with your **UNIVERSITARY** username and password.

AFTER THAT IT SHOULD WORK!


