import logging
from psychopy import visual, event, core, data, gui
import pandas as pd
import os  # Import os to create directories

# Collect participant info
exp_info = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Image Rating Task')
if not dlg.OK:
    core.quit()

# Set up data saving
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Set up logging
logging.basicConfig(filename='data/' + exp_info["participant"] + '_experiment.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

# Log the start of the experiment
logging.info('Experiment started')

# Load the image paths from the CSV file
try:
    image_data = pd.read_csv('images.csv')
    logging.info('Loaded images.csv successfully')
except Exception as e:
    logging.error(f'Error loading images.csv: {e}')
    core.quit()


logging.info(f'Participant ID: {exp_info["participant"]}')

# Create a window
win = visual.Window(size=[800, 600], color='gray', units='pix')

# Create an introduction screen
intro_text = visual.TextStim(win, text="Welcome to the experiment!\n\nYou will see a series of images.\nPlease rate each image after it is displayed.\nPress any key to start.", color='black', height=30)
intro_text.draw()
win.flip()

# Wait for a key press to start the experiment
event.waitKeys()
logging.info('Introduction screen completed')

# Create a rating scale prompt
rating_prompt = visual.TextStim(win, text="How realistic do you think this image is?", color='black', height=30, pos=(0, 200))

# Create a rating scale
ratingScale = visual.RatingScale(win, low=1, high=5, markerStart=3, size=1.5, pos=(0, -150), stretch=1, labels=['1', '2', '3', '4', '5'])

# Create a fixation cross
fixation = visual.TextStim(win, text="+", color='black', height=40)

data_filename = os.path.join(data_dir, '%s_ratings.csv' % exp_info['participant'])
try:
    data_file = open(data_filename, 'w')
    data_file.write('participant,image,rating,response_time\n')
    logging.info(f'Data file created: {data_filename}')
except Exception as e:
    logging.error(f'Error creating data file: {e}')
    core.quit()

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

# Close the data file
data_file.close()
logging.info('Data file closed')

# Create an end screen
end_text = visual.TextStim(win, text="Thank you for participating!\n\nPress any key to exit.", color='black', height=30)
end_text.draw()
win.flip()

# Wait for a key press to exit
event.waitKeys()
logging.info('End of experiment screen completed')

# Close the window
win.close()
core.quit()
logging.info('Experiment finished and window closed')
