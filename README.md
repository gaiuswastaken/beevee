# Beevee
A task organiser for the busy people

## Who is this for?
Mainly A Level Students doing 3-4 A Levels

## What does this do?
- Uses AI to generate a database of your specification for each A Level
- Generates tasks that reward you money for completing them
- Lets you buy eggs to hatch cute bees
- Tracks how many bees you have discovered!

# Prerequisites
- The attention span to read the instructions (failure to read them leads to issues that can be avoided otherwise)
- A Google Gemini API Key (if you do not know how to get it or what it is, learn more about it [here](GEMINI_KEY.md)
- Internet links for your specifications (must start with https:// and be a PDF!)

# How to download it

## Windows: Method 1 (my favourite way as updates are a dream here)
1. Download Git [here](https://git-scm.com/)
2. Install Git
3. Run Git Bash
4. Now type `git clone https://github.com/gaiuswastaken/beevee`
5. Now type `explorer .`
6. Find the folder 'beevee'
7. Move the folder 'beevee' to a convenient location. This could be your Desktop, Downloads or a folder specifically created for it 

### Updating
1. Copy the path your beevee directory is in (at the top of the ribbon)
2. Open Git Bash 
3. Run `cd "{your directory}"`
4. Then type `git pull`

## Windows: Method 2 (requires redownloading in case it needs updates)
1. Click on the green button that says 'Code'
2. Then click on 'Download ZIP'
3. Download the ZIP
4. Extract the ZIP
5. Move the folder to your preferred location

## macOS/Linux
To be frank, setting up Beevee on macOS and Linux is more complicated on Windows (because they are fundamentally different)

However, I have tried to simplify it as much as possible despite the limitations I have (this is the simplest, least error-prone way)

1. (macOS) Open the 'Terminal' app (sounds scary but is not)
2. (macOS) Type the command `git version` 
    - If Git is already installed, you should see the Git version
    - If Git is not installed, you will instead see a prompt asking you whether you want to install "xcode-select". Press Install
3. (macOS) If you have just installed it, check it again with `git version` and you should now see the Git Version
4. Now type `git clone https://github.com/gaiuswastaken/beevee`
5. Now type `open .` (macOS) or `xdg-open .` (Linux). This should make it so that it opens the current directory in your file manager
6. Move the folder 'beevee' to a convenient location. This could be your Desktop, Downloads or a folder specifically created for it 

### Updating
1. Copy the path your beevee directory is in (at the top of the ribbon)
2. Open Git Bash 
3. Run `cd "{your directory}"`
4. Then type `git pull`

# Setting up Python with the necessary libraries
Downloading Python is necessary otherwise it will simply not run

## Python
1. Go to the Python website [here](https://www.python.org/)
2. Then click on 'Downloads'
3. Then scroll to 'Looking for a specific release?'
4. Scroll on the table to find 'Python 3.12.10' (recommended) but you are free to use the latest Python 3.12 (do not go beyond that though)
5. Download the version that is suitable for you (Windows: Get the Windows Installer, Mac: Get the macOS version, Linux: Do not download from here, use your package manager)
6. Make sure to enable the PATH checkbox before installing
7. Install Python (duh)

## Libraries

### Windows
To downoad the libraries, double click on 'install_dependencies.py' to run it (it should install the necessary libraries)

### macOS/Linux
To downoad the libraries, double click on 'install_dependencies_macos.command' to run it (it should install the necessary libraries)

This is why the downloading was initially more complicated (if you followed the same way as Windows, guess what; more Terminal!)

# How to use it
1. Go to the location where you placed Beevee (e.g. Desktop, Downloads, etc.)

## Windows
2. To run it, double click on 'main_program.py' (may have to run it twice)

## macOS/Linux
2. To run it, double click on 'main_program_macos.command' (may have to run it twice)

# Extra information
- On the onboarding screen, when it asks for your 4th subject, if you don't do a 4th subject, input `none` in the subject name field and type some gibberish in the specification URL



- When you finish the setup, go to the editor (indicated by the pen and paper) and then select your subject and add your confidence ratings (the task recommendation algorithm will not work without it)
- Close the editor
- Repeat for every subject you are doing
- Then close the main app and reopen it

