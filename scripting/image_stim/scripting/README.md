# Step-by-Step Guide for Creating an Image Rating Task Experiment Using PsychoPy

This guide will help you create an image rating task experiment using PsychoPy scripting mode. Follow these steps to set up and run your experiment.

## Step 0: Set Up the Environment

- Ensure you have PsychoPy installed. You can download it from the [PsychoPy website](https://www.psychopy.org/download.html).
- Open your preferred code editor or the PsychoPy Coder view.

## Step 1: Import Libraries

```python
import logging
from psychopy import visual, event, core, data, gui
import pandas as pd
import os  # Import os to create directories
```

- This block imports necessary libraries for the experiment.

## Step 2: Collect Participant Information

```python
# Collect participant info
exp_info = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Image Rating Task')
if not dlg.OK:
    core.quit()
```

- This block creates a dialog box to collect participant information. If the dialog is canceled, the experiment exits.

## Step 3: Set Up Data Saving and Logging

```python
# Set up data saving
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    logging.info(f'Created directory: {data_dir}')

# Set up logging
logging.basicConfig(filename='data/' + exp_info["participant"] + '_experiment.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')

# Log the start of the experiment
logging.info('Experiment started')
```

- This block sets up the directory for saving data and configures logging to record the experiment's progress.

## Step 4: Load Image Paths

```python
# Load the image paths from the CSV file
try:
    image_data = pd.read_csv('images.csv')
    logging.info('Loaded images.csv successfully')
except Exception as e:
    logging.error(f'Error loading images.csv: {e}')
    core.quit()
```

- This block loads image paths from a CSV file and logs the success or failure of this operation.

## Step 5: Log Participant ID

```python
logging.info(f'Participant ID: {exp_info["participant"]}')
```

- Logs the participant's ID.

## Step 6: Create the Experiment Window

```python
# Create a window
win = visual.Window(size=[800, 600], color='gray', units='pix')
```

- Creates a window with a gray background where the experiment will be displayed.

## Step 7: Display Introduction Screen

```python
# Create an introduction screen
intro_text = visual.TextStim(win, text="Welcome to the experiment!\n\nYou will see a series of images.\nPlease rate each image after it is displayed.\nPress any key to start.", color='black', height=30)
intro_text.draw()
win.flip()

# Wait for a key press to start the experiment
event.waitKeys()
logging.info('Introduction screen completed')
```

- Displays a welcome message and waits for the participant to press any key to continue.

## Step 8: Set Up Rating Scale and Fixation Cross

```python
# Create a rating scale prompt
rating_prompt = visual.TextStim(win, text="How realistic do you think this image is?", color='black', height=30, pos=(0, 200))

# Create a rating scale
ratingScale = visual.RatingScale(win, low=1, high=5, markerStart=3, size=1.5, pos=(0, -150), stretch=1, labels=['1', '2', '3', '4', '5'])

# Create a fixation cross
fixation = visual.TextStim(win, text="+", color='black', height=40)
```

- Creates a prompt for the rating scale, the rating scale itself, and a fixation cross to center the participant's attention.

## Step 9: Open Data File

```python
data_filename = os.path.join(data_dir, '%s_ratings.csv' % exp_info['participant'])
try:
    data_file = open(data_filename, 'w')
    data_file.write('participant,image,rating,response_time\n')
    logging.info(f'Data file created: {data_filename}')
except Exception as e:
    logging.error(f'Error creating data file: {e}')
    core.quit()
```

- Opens the data file for writing and logs the success or failure of this operation.

## Step 10: Main Experiment Loop

```python
# Loop through each image in the CSV file
for idx, row in image_data.iterrows():
    image_path = row['image']
    logging.info(f'Displaying image: {image_path}')

    # Display the fixation cross for 1 second
    fixation.draw()
    win.flip()
    core.wait(1)

    # Create an image stimulus
    image = visual.ImageStim(win, image=image_path, size=(400, 400))

    # Display the image for 5 seconds
    image.draw()
    win.flip()
    core.wait(5)

    # Display the rating scale prompt
    ratingScale.reset()
    while ratingScale.noResponse:
        rating_prompt.draw()
        ratingScale.draw()
        win.flip()

    # Save the rating
    rating = ratingScale.getRating()
    ratingTime = ratingScale.getRT()
    data_file.write(f'{exp_info["participant"]},{image_path},{rating},{ratingTime}\n')


    logging.info(f'Rating recorded: image={image_path}, rating={rating}, response_time={ratingTime}')
```

- This block runs the main experiment loop:
  - Displays the fixation cross for 1 second.
  - Shows each image for 5 seconds.
  - Displays the rating scale prompt and waits for a response.
  - Saves the participant's rating and response time.

## Step 11: Close Data File

```python
# Close the data file
data_file.close()
logging.info('Data file closed')
```

- Closes the data file and logs this action.

## Step 12: End Screen

```python
# Create an end screen
end_text = visual.TextStim(win, text="Thank you for participating!\n\nPress any key to exit.", color='black', height=30)
end_text.draw()
win.flip()

# Wait for a key press to exit
event.waitKeys()
logging.info('End of experiment screen completed')
```

- Displays a thank-you message and waits for the participant to press any key to exit.

## Step 13: Close the Window

```python
# Close the window
win.close()
core.quit()
logging.info('Experiment finished and window closed')
```

- Closes the experiment window and quits PsychoPy, logging the completion of the experiment.

## Step 14: Run the Experiment

- Save the script as `image_rating_task.py`
- Ensure the `images.csv` file is in the same directory as your script.
- Open a terminal or command prompt and navigate to the directory containing your script.
- Run the script using the following command:

```sh
python image_rating_task.py
```

- Follow the instructions displayed on the screen to complete the experiment.

## Summary

You have now created and run an image rating task experiment using the scripting mode of PsychoPy. The script includes all necessary components and saves the participant responses and logs to a CSV file and a log file, respectively.
