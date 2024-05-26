# Creating a basic Stroop task experiment from scratch using PsychoPy scripting

## Step 1: Set Up the Environment

- Ensure you have PsychoPy installed. You can download it from the [PsychoPy website](https://www.psychopy.org/download.html).
- Open your preferred code editor or the PsychoPy Coder view.

## Step 2: Create the Conditions File

- Use the following Python code to generate the conditions file:

```python
import pandas as pd
import random

# Create the lists
words = ['BLUE']*5 + ['RED']*5
colors = ['blue']*5 + ['red']*5

# Shuffle them and create the dataframe using them
random.shuffle(words)
random.shuffle(colors)

# Create the dataframe with using dictionary declaration
df_conditions = pd.DataFrame({'word': words, 'color': colors})

# Save the dataframe
df_conditions.to_csv('conditions.csv', index=False)
```

Explanation:

- This code imports the necessary libraries (`pandas` and `random`).
- It creates lists of words and corresponding colors.
- It shuffles these lists to randomize the order.
- It creates a DataFrame from the lists and saves it as `conditions.csv`.

- Save this script as `create_conditions.py` and run it to generate `conditions.csv`.

## Step 3: Write the Stroop Task Script

- Create a new Python script file (e.g., `stroop_task.py`) and use the following code:

### Import Libraries

```python
from psychopy import visual, core, data, event, gui
import random  # Import random for generating random ISI
```

Explanation:

- This block imports necessary libraries from PsychoPy for creating visual stimuli, handling time, managing data, capturing events, and displaying graphical user interfaces.
- The `random` library is imported to generate random inter-stimulus intervals (ISI).

### Define a Function to Create the Conditions CSV File

```python
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
```

Explanation:

- This function creates the `conditions.csv` file used in the experiment.
- It generates lists of words and colors, shuffles them, and saves them as a CSV file.

### Set Up Experiment Information

```python
# Create a dictionary for storing the experiment info
exp_info = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Stroop Task')
if not dlg.OK:
    core.quit()
```

Explanation:

- This block creates a dialog box to collect participant information.
- If the user cancels the dialog, the experiment exits.

### Create a Window

```python
# Create a window with gray background
win = visual.Window([800, 600], color='gray', units='height')
```

Explanation:

- This line creates a window with a gray background where the experiment will be displayed.
- The window size is set to 800x600 pixels, and the units are set to `height` for scaling.

### Welcome Routine

```python
# Welcome routine
welcome_text = visual.TextStim(win=win, text='Welcome to the Stroop task experiment!\n\nPress any key to begin.', color='black', height=0.05)
welcome_text.draw()
win.flip()
event.waitKeys()
```

Explanation:

- This block displays a welcome message to the participant.
- The `TextStim` object creates text stimuli, and `win.flip()` updates the window to show the text.
- `event.waitKeys()` waits for the participant to press any key to continue.

### Instructions Routine

```python
# Instructions routine
instructions_text = visual.TextStim(win=win, text='You will see words displayed in different colors.\n\nPress the LEFT arrow key if the color is RED.\nPress the RIGHT arrow key if the color is BLUE.\n\nPress Enter to start.', color='black', height=0.05)
instructions_text.draw()
win.flip()
event.waitKeys(keyList=['return'])
```

Explanation:

- This block displays instructions to the participant.
- It waits for the participant to press the `Enter` key to start the experiment.

### Fixation Cross Routine

```python
# Create a fixation cross
fixation = visual.ShapeStim(win=win, vertices='cross', size=(0.05, 0.05), fillColor='black', lineColor='black')
```

Explanation:

- This block creates a fixation cross to center the participant's attention before each trial.
- The `ShapeStim` object is used to create the cross.

### Define the Trial Routine

```python
# Define the trial routine
trial_text = visual.TextStim(win=win, text='', color='', height=0.1)
key_resp = event.BuilderKeyResponse()
```

Explanation:

- This block defines the components of a trial.
- `trial_text` will display the word stimuli, and `key_resp` will handle the participant's key responses.

### Set Up Data Handler

```python
# Create a data handler for the trials
trials = data.TrialHandler(nReps=1, method='random', trialList=data.importConditions('conditions.csv'))
this_exp = data.ExperimentHandler(dataFileName='data/%s_%s' % (exp_info['participant'], 'stroop'), extraInfo=exp_info)

# Add the data handler to the experiment
this_exp.addLoop(trials)
```

Explanation:

- This block creates a `TrialHandler` to manage trial conditions and randomize their order.
- `ExperimentHandler` is used to handle saving data, and `addLoop(trials)` adds the trial loop to the experiment.

### Run the Trial Loop

```python
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
```

Explanation:

- This block runs the main trial loop:
  - Displays the fixation cross for 2 seconds.
  - Displays the word stimulus in the specified color.
  - Collects the participant's response and records the reaction time.
  - Provides feedback based on the correctness of the response.
  - Displays a random inter-stimulus interval (ISI).

### Save the Data

```python
# Save the data to a CSV file
this_exp.saveAsWideText('data/%s_stroop_task.csv' % exp_info['participant'], delim=',')
this_exp.saveAsPickle('data/%s_stroop_task' % exp_info['participant'])
```

Explanation:

- This block saves the collected data in both CSV and pickle formats.

### End of Experiment

```python
# End of experiment
end_text = visual.TextStim(win=win, text='Thank you for participating!\n\nPress any key to exit.', color='black', height=0.05)
end_text.draw()
win.flip()
event.waitKeys()

# Close the window and quit
win.close()
core.quit()
```

Explanation:

- This block displays a thank-you message and waits for the participant to press any key to exit.
- It then closes the window and quits the experiment.

## Step 4: Run the Experiment

- Ensure the `conditions.csv` file is in the same directory as your script.
- Open a terminal or command prompt and navigate to the directory containing your script.
- Run the script using the following command:

```sh
python stroop_task.py
```

- Follow the instructions displayed on the screen to complete the experiment.

## Summary

You have now created and run a basic Stroop task experiment using the scripting mode of PsychoPy. The script includes all necessary components and saves the participant responses to a CSV file.
