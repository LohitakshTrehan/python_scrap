have following instaled:
- `python3 --version`
- `pip3 --version`

Be sure you have python virtual env:
- `pip3 install virtualenv`

How to create a new virtual env (It creates a folder):
- `python3 -m venv basic`

Note: check how to initiate a venv in already existing folder, as you can see that `basic` folder exists in this directory already.

to install beautiful soup library:
- `pip3 install beautifulsoup`

to install requests:
- `pip3 install requests`

to activate a venv:
- go to the venv folder by using `cd` in terminal
- `source bin/activate`
- The above command will activate the venv

Just type `deactivate` to deactivate the venv

Why virtual env?
Ans: Helps you to not pollute global environment otherwise packages will be installed in all python in your computer globally

post this, just run python scripts like `python3 <scriptname>.py`