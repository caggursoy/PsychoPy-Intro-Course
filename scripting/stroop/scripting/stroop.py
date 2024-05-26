# Import necessary libraries
from psychopy import visual, core, data, event, gui
import random  # Import random for generating random ISI

# Define a function to create the conditions CSV file
def create_conditions_file():
    import pandas as pd

    # create the lists
    words = ['BLUE']*5 + ['RED']*5
    colors = ['blue']*5 + ['red']*5

    # shuffle them and create the dataframe using them
    random.shuffle(words)
    random.shuffle(colors)

    # create the dataframe with using dictionary declaration
    df_conditions = pd.DataFrame({'word': words, 'color': colors})

    # save the dataframe
    df_conditions.to_csv('conditions.csv', index=False)

# Create the conditions file
create_conditions_file()

# Create a dictionary for storing the experiment info
exp_info = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Stroop Task')
if not dlg.OK:
    core.quit()

# Create a window with gray background
win = visual.Window([800, 600], color='gray', units='height')

# Define routines and components

# Welcome routine
welcome_text = visual.TextStim(win=win, text='Welcome to the Stroop task experiment!\n\nPress any key to begin.', color='black', height=0.05)
welcome_text.draw()
win.flip()
event.waitKeys()

# Instructions routine
instructions_text = visual.TextStim(win=win, text='You will see words displayed in different colors.\n\nPress the LEFT arrow key if the color is RED.\nPress the RIGHT arrow key if the color is BLUE.\n\nPress Enter to start.', color='black', height=0.05)
instructions_text.draw()
win.flip()
event.waitKeys(keyList=['return'])

# Create a fixation cross
fixation = visual.ShapeStim(win=win, vertices='cross', size=(0.05, 0.05), fillColor='black', lineColor='black')

# Define the trial routine
trial_text = visual.TextStim(win=win, text='', color='', height=0.1)
key_resp = event.BuilderKeyResponse()

# Create a data handler for the trials
trials = data.TrialHandler(nReps=1, method='random', trialList=data.importConditions('conditions.csv'))
this_exp = data.ExperimentHandler(dataFileName='data/%s_%s' % (exp_info['participant'], 'stroop'), extraInfo=exp_info)

# Add the data handler to the experiment
this_exp.addLoop(trials)

# Run the trial loop
for trial in trials:
    # Fixation cross
    fixation.draw()
    win.flip()
    core.wait(2.0)

    # Display the word with the color
    trial_text.setText(trial['word'])
    trial_text.setColor(trial['color'])
    trial_text.draw()
    win.flip()

    # Collect response
    key_resp.keys = []
    key_resp.rt = []
    event.clearEvents(eventType='keyboard')
    resp_clock = core.Clock()
    while len(key_resp.keys) == 0:
        theseKeys = event.getKeys(keyList=['left', 'right'])
        if len(theseKeys) > 0:
            key_resp.keys = theseKeys[0]
            key_resp.rt = resp_clock.getTime()
            if key_resp.keys == 'left' and trial['color'] == 'red':
                feedback = 'correct'
            elif key_resp.keys == 'right' and trial['color'] == 'blue':
                feedback = 'correct'
            else:
                feedback = 'wrong'
            trials.addData('response', key_resp.keys)
            trials.addData('feedback', feedback)
            trials.addData('rt', key_resp.rt)
            this_exp.nextEntry()
            break

    # Display feedback
    feedback_text = visual.TextStim(win=win, text=feedback, color='black', height=0.05)
    feedback_text.draw()
    win.flip()
    core.wait(1.0)

    # Inter-stimulus interval (ISI)
    t_isi = random.uniform(0, 1)
    fixation.draw()
    win.flip()
    core.wait(t_isi)

# Save the data to a CSV file
this_exp.saveAsWideText('data/%s_stroop_task.csv' % exp_info['participant'], delim=',')
this_exp.saveAsPickle('data/%s_stroop_task' % exp_info['participant'])

# End of experiment
end_text = visual.TextStim(win=win, text='Thank you for participating!\n\nPress any key to exit.', color='black', height=0.05)
end_text.draw()
win.flip()
event.waitKeys()

# Close the window and quit
win.close()
core.quit()
