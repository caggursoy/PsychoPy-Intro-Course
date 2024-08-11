# Image Rating Task with PsychoPy

This PsychoPy experiment displays images to participants and collects their ratings on the realism of each image. The experiment is compatible with both fMRI environments and standard behavioral setups, with customizable settings for each context.

## Link to script

The full script to the task is in this [link](https://github.com/caggursoy/PsychoPy-Intro-Course/blob/main/scripting/fmri/scripting/image_fmri.py).

## Table of Contents

- [Dependencies](#dependencies)
- [Setup](#setup)
- [MR_Settings Initialization](#mr_settings-initialization)
- [Collect Participant Info and fMRI Check](#collect-participant-info-and-fmri-check)
- [Create the Filename and Log File](#create-the-filename-and-log-file)
- [Initialize the Experiment Handler](#initialize-the-experiment-handler)
- [Screen and Monitor Setup](#screen-and-monitor-setup)
- [Loading Image Paths](#loading-image-paths)
- [Initialize Visual Components](#initialize-visual-components)
- [Introduction Screen](#introduction-screen)
- [Experiment Loop](#experiment-loop)
- [Ending the Experiment](#ending-the-experiment)
- [Data Saving](#data-saving)

## Dependencies

This experiment requires the following Python packages:

- `psychopy`
- `pandas`
- `screeninfo`

If the packages are not installed, to install these packages, run the following command in your conda psychopy environment in your terminal/anaconda prompt:

```bash
pip install pandas screeninfo
```

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
# set the fmri variable
fmri = exp_info['fMRI']
```

## Create the Filename and Log File

A filename is created for storing data, and a log file is set up to record the experiment’s events:

```python
os.makedirs(str(Path.cwd()/'data'), exist_ok=True)
filename = str(Path('data') / exp_info['participant']) + '_experiment'
logFile = logging.LogFile(str(filename)+'.log', level=logging.EXP, filemode='w')
logging.console.setLevel(logging.WARNING)
logging.info(f'Participant ID: {exp_info["participant"]}')
```

## Initialize the Experiment Handler

An `ExperimentHandler` is created to manage and save experiment data:

```python
thisExp = data.ExperimentHandler(name='image_fmri', version='v01', extraInfo=None, runtimeInfo=None,
                                 originPath=None, savePickle=True, saveWideText=True, dataFileName=filename)

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

## Initialize Visual Components

Several visual stimuli are initialized, including the rating scale, fixation cross, and an image stimulus:

```python
questionScale = visual.RatingScale(win=win, name='questionScale', scale='How realistic do you think this image is?\n\n\n',
                                   showAccept=False, noMouse=True, low=1, high=5, textSize=1.25, stretch=1.5,
                                   markerStart=3, leftKeys='g', rightKeys='b', acceptKeys='r', labels=['1', '5'],
                                   maxTime=10)
fix = visual.TextStim(win, text='+', height=fontH*2, color=textCol)
image = visual.ImageStim(win, size=(.5625, .5625))
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
