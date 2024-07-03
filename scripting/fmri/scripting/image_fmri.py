### Import packages ###
from psychopy import visual, core, data, event, logging, gui, monitors
import os, locale, platform
from pathlib import Path
import pandas as pd
from psychopy.hardware.emulator import launchScan
from screeninfo import get_monitors

# MR_Settings initialization
MR_settings = {
    'TR': 2,     # duration (sec) per whole-brain volume
    'volumes': 33,    # number of whole-brain 3D volumes per scanning run
    'sync': 't',  # character to use as the sync timing event; assumed to come at start of a volume
    # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'skip': 0,
    'sound': False    # in test mode: play a tone as a reminder of scanner noise
}

# Collect participant info and fMRI check
exp_info = {'participant': '', 'fMRI': False}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Image Rating Task')
if not dlg.OK:
    core.quit()
# set the fmri variable
fmri = exp_info['fMRI']

# create the filename
os.makedirs(str(Path.cwd()/'data'), exist_ok=True)
filename = str(Path('data') / exp_info['participant']) + '_experiment'

# logfile overwrites when overwrite is selected. If not, as the filename changes it won't be overwritten
logFile = logging.LogFile(str(filename)+'.log',
                          level=logging.EXP, filemode='w')
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

# log the participant number
logging.info(f'Participant ID: {exp_info["participant"]}')

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='image_fmri', version='v01', extraInfo=None, runtimeInfo=None,
                                 originPath=None, savePickle=True, saveWideText=True, dataFileName=filename)

# now generate the screen
monitors_list = get_monitors()
monitor_names = [f"{monitor.name} ({monitor.x},{monitor.y}) - {monitor.width}x{monitor.height}" for monitor in monitors_list]
# 
scr_dlg = gui.Dlg(title="Select screen")
scr_dlg.addField('Monitor:', choices=monitor_names)
scr_dlg.show()

if dlg.OK:
    selected_index = monitor_names.index(scr_dlg.data['Monitor:'])
    selected_monitor = monitors_list[selected_index]
    win_res = [selected_monitor.width, selected_monitor.height]
else:
    core.quit()  # user pressed cancel
exp_mon = monitors.Monitor('exp_mon')  # create a "monitor"
exp_mon.setSizePix(win_res)  # and set the size of the screen
# now create a psychopy window
if fmri:  # if fmri, fullscreen
    win = visual.Window(size=win_res, screen=selected_index, allowGUI=True,
                        fullscr=True, monitor=exp_mon, units='height',
                        color=(0.2, 0.2, 0.2))
else:  # if test, only 800x600
    win = visual.Window(size=[800, 600], screen=selected_index, allowGUI=True,
                        fullscr=False, monitor=exp_mon, units='height',
                        color=(0.2, 0.2, 0.2))
# Setup the window and presentation constants
yScr = 1.
xScr = float(win_res[0])/win_res[1]
fontH = yScr/25
wrapW = xScr/1.5
textCol = 'black'

# Load the image paths from the CSV file
try:
    image_data = pd.read_csv('images.csv')
    logging.info('Loaded images.csv successfully')
except Exception as e:
    logging.error(f'Error loading images.csv: {e}')
    core.quit()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
# logClock = core.Clock()
logging.setDefaultClock(globalClock) # set a default clock for logging, so combined task will run smoothly

# Create TrialHandlers to save data
trials = data.TrialHandler([], nReps=len(image_data))

# Initialize components for wanting scales # left='g'reen, right='b'lue, confirm='r'ed
questionScale = visual.RatingScale(win=win, name='questionScale', scale='How realistic do you think this image is?\n\n\n',
                               showAccept=False, noMouse=True, low=1, high=5, textSize=1.25, stretch=1.5,
                               markerStart=3, leftKeys='g', rightKeys='b',acceptKeys='r', labels=['1', '5'], 
                               maxTime=10)
# #create fixation stimulus
fix = visual.TextStim(win, text='+', height=fontH*2, color=textCol)

# Create an image stimulus
image = visual.ImageStim(win, size=(.5625, .5625)) # size is relative

# clear all the keyboard presses and hide the mouse cursor
event.clearEvents(eventType='keyboard')
event.Mouse(visible=False)  # hide mouse cursor

# Create an introduction screen
intro_text = visual.TextStim(win, 
                             text="Welcome to the experiment!\n\nYou will see a series of images.\nPlease rate each image after it is displayed.\nPress any key to start.", 
                             color=textCol, height=fontH, wrapWidth=wrapW)
intro_text.draw()
win.flip()

# Wait for a key press to start the experiment
event.waitKeys()

# add loops to the experiment
thisExp.addLoop(trials)

# now handle the launchScan / important for trigger capturing
launchScan(win=win, settings=MR_settings, 
           globalClock=globalClock, mode='Scan' if fmri else 'Test', 
           wait_msg='Waiting for the trigger')

# Loop through each image in the CSV file
for idx, row in image_data.iterrows():
    image_path = row['image']
    logging.info(f'Displaying image: {image_path}')

    # Display the fixation cross for 1 second
    fix.draw()
    win.flip()
    core.wait(1)

    # set the image on the screen
    image.setImage(image_path)
    trials.addData('imgName', image_path) # get image name and add to table

    # Display the image for 5 seconds
    image.draw()
    trials.addData('imgBeginTime', globalClock.getTime()) # get image drawing begin time and add to table
    win.flip()
    core.wait(5)
    trials.addData('imgEndTime', globalClock.getTime()) # get image drawing end time and add to table

    # Display the rating scale prompt
    questionScale.reset()
    trials.addData('scaleBeginTime', globalClock.getTime()) # get scale drawing begin time and add to table
    while questionScale.noResponse:
        questionScale.draw()
        win.flip()
    trials.addData('scaleEndTime', globalClock.getTime()) # get scale drawing begin time and add to table

    # Save the rating and RT
    ratingTime = questionScale.getRT()
    trials.addData('ratingTime', ratingTime) # get response time and add to table
    rating = questionScale.getRating()
    trials.addData('rating', rating) # get rating and add to data table
    # 
    thisExp.nextEntry()

# Create an end screen
end_text = visual.TextStim(win, text="Thank you for participating!\n\nPress any key to exit.", color='black', height=fontH)
end_text.draw()
win.flip()

# Wait for a key press to exit
event.waitKeys()
logging.info('End of experiment screen completed')

# save log files as csv and pickle as backup
thisExp.saveAsWideText(filename+'.csv',fileCollisionMethod = 'rename')
thisExp.saveAsPickle(filename, fileCollisionMethod = 'rename')
logging.flush()

# make sure everything is shut down
thisExp.abort()  # or data files will save again on exit

# Close the window
win.close()
core.quit()
