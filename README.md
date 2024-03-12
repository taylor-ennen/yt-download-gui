# To Run:
Clone the repo to a folder where you want to store your songs. Videos are downloaded into this repo directly, but can be changed using the gui.
```
git clone https://www.github.com/taylor-ennen/yt-download-gui && cd yt-download-gui
```
Your terminal should be pointing in the cloned repo folder using the last command. Next verify the installation by running:
```
python3 main.py -h
```
# Using the CLI: 
This should show you the CLI arguments. You can run the program in CLI or GUI mode. The CLI workflow looks like this:
```
cli broken, use gui for now. need to fix list interpretation through the arguments correctly still
```
# Using the GUI 
```
python3 main.py
```
# Useful tips:
UX Tip: 
 - If you have the url on your clipboard and run the main.py file, the url will auto populate to the url field, follow this up my hitting enter/return after the window to start your download


# Caution
Make sure to exit the program from the gui using the x on the window 
failure to do so may mean you have to kill the process thread itself to clear the gui window from your desktop if you exit the program via terminal (ctrl z/c)
