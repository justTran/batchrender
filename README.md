# BatchRenderer

## Renders multiple projects for Sony Vegas Pro 14

**Current Version:** 0.1

**Last updated:** December 25th 2019

### Important Notice

I have only tested this for Vegas Pro 14. This script is intended for someone to be _away_ from their computer and have the script render videos for them.

### Features:

- Windows only
- Visual queue _(listbox)_
- Easily remove items from queue
- Renders in order of queue

:warning: This version is tailored for a 2560 x 1440 screen. May need to modify for a 1920 x 1080 screen. Also manipulates cursor placement, so **do not move the cursor.**

### Required Modules and Versions:

- Python 3.8+
- psutil
- pyautogui

* There is also a special Vegas Script to auto-render a video. You can find that file [**here.**](https://github.com/WhatIfWeDigDeeper/SonyVegasProScripting) _Credits to @WhatIfWeDigDeeper_
* He provides a great guide to use the script and create a button in the toolbar to run the script, which is what I used for the cursor events.

### Usage:

Run the main.py file with the required modules installed.

## Enqueue / Add to Queue

Click the **Enqueue** button to browse for a Vegas project _(.veg file)_.
Click **open** to add the project to the queue.

## Dequeue / Remove from Queue

Select the projects you want to dequeue from the **listbox** in the tkinter window.
Click **Dequeue** to remove the projects from the queue and listbox.

## Render

Click the **Render** button.
Do not touch anything. The script will render the projects in the queue and turn off your computer.

### Future Improvements:

- Multithreading
- Error Handling
- Secure Coding
