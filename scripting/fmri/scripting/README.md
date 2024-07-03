
# Image Rating Task with PsychoPy

This repository contains a PsychoPy script for running an image rating task. Participants view a series of images and rate each one on a scale based on its realism. The experiment can be conducted in both test mode and fMRI mode.

## Table of Contents
- [Setup](#setup)
- [MR_Settings Initialization](#mr_settings-initialization)
- [Collect Participant Info and fMRI Check](#collect-participant-info-and-fmri-check)
- [Screen and Monitor Setup](#screen-and-monitor-setup)
- [Loading Image Paths](#loading-image-paths)
- [Introduction Screen](#introduction-screen)
- [Experiment Loop](#experiment-loop)
- [Ending the Experiment](#ending-the-experiment)
- [Data Saving](#data-saving)

## Setup

Ensure you have the required packages installed. This experiment relies on PsychoPy and additional packages listed below:

```python
from psychopy import visual, core, data, event, logging, gui, monitors
import os, locale, platform
from pathlib import Path
import pandas as pd
from psychopy.hardware.emulator import launchScan
from screeninfo import get_monitors
```

## MR_Settings Initialization

The `MR_settings` dictionary initializes parameters for the MRI scanner:

```python
MR_settings = {
    'TR': 2,  # duration (sec) per whole-brain volume
    'volumes': 33,  # number of whole-brain 3D volumes per scanning run
    'sync': 't',  # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0,  # number of volumes lacking a sync pulse at start of scan
    'sound': False  # in test mode: play a tone as a reminder of scanner noise
}
```

## Collect Participant Info and fMRI Check

A dialog box collects participant information and checks if fMRI mode is selected:

```python
exp_info = {'participant': '', 'fMRI': False}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Image Rating Task')
if not dlg.OK:
    core.quit()
fmri = exp_info['fMRI']
```

## Screen and Monitor Setup

The script detects available monitors and allows the user to select one:

```python
monitors_list = get_monitors()
monitor_names = [f"{monitor.name} ({monitor.x},{monitor.y}) - {monitor.width}x{monitor.height}" for monitor in monitors_list]

scr_dlg = gui.Dlg(title="Select screen")
scr_dlg.addField('Monitor:', choices=monitor_names)
scr_dlg.show()

if dlg.OK:
    selected_index = monitor_names.index(scr_dlg.data['Monitor:'])
    selected_monitor = monitors_list[selected_index]
    win_res = [selected_monitor.width, selected_monitor.height]
else:
    core.quit()
```

## Loading Image Paths

The script loads image paths from a CSV file:

```python
try:
    image_data = pd.read_csv('images.csv')
    logging.info('Loaded images.csv successfully')
except Exception as e:
    logging.error(f'Error loading images.csv: {e}')
    core.quit()
```

## Introduction Screen

An introductory screen is displayed before the experiment starts:

```python
intro_text = visual.TextStim(win, 
                             text="Welcome to the experiment!\n\nYou will see a series of images.\nPlease rate each image after it is displayed.\nPress any key to start.", 
                             color=textCol, height=fontH, wrapWidth=wrapW)
intro_text.draw()
win.flip()
event.waitKeys()
```

## Experiment Loop

The main loop displays each image and records ratings:

```python
for idx, row in image_data.iterrows():
    image_path = row['image']
    logging.info(f'Displaying image: {image_path}')

    fix.draw()
    win.flip()
    core.wait(1)

    image.setImage(image_path)
    trials.addData('imgName', image_path)

    image.draw()
    trials.addData('imgBeginTime', globalClock.getTime())
    win.flip()
    core.wait(5)
    trials.addData('imgEndTime', globalClock.getTime())

    questionScale.reset()
    trials.addData('scaleBeginTime', globalClock.getTime())
    while questionScale.noResponse:
        questionScale.draw()
        win.flip()
    trials.addData('scaleEndTime', globalClock.getTime())

    ratingTime = questionScale.getRT()
    trials.addData('ratingTime', ratingTime)
    rating = questionScale.getRating()
    trials.addData('rating', rating)
    thisExp.nextEntry()
```

## Ending the Experiment

An end screen is displayed when the experiment concludes:

```python
end_text = visual.TextStim(win, text="Thank you for participating!\n\nPress any key to exit.", color='black', height=fontH)
end_text.draw()
win.flip()
event.waitKeys()
logging.info('End of experiment screen completed')
```

## Data Saving

Data is saved in both CSV and Pickle formats to ensure robustness:

```python
thisExp.saveAsWideText(filename+'.csv', fileCollisionMethod='rename')
thisExp.saveAsPickle(filename, fileCollisionMethod='rename')
logging.flush()
thisExp.abort()
win.close()
core.quit()
```

Ensure all dependencies are installed and paths are correctly set before running the script. Modify parameters as needed for specific experimental requirements.
