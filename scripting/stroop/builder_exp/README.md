# Creating a basic Stroop task experiment from scratch

## Using builder interface

### Step 1: Set Up the Experiment

- Open PsychoPy Builder:

  - Launch PsychoPy and select the Builder view.

- Create a New Experiment:
  - Go to File > New.
  - Save the experiment with the name `stroop.psyexp`
    ![Create new experiment](img/new_exp.png)

### Step 2: Define the Conditions

- Create a Conditions File:

  - Create an CSV file to define the conditions for your experiment.
    The file should have columns for the text stimuli and their corresponding colors. For example:

  | word | color |
  | ---- | ----- |
  | RED  | red   |
  | BLUE | blue  |
  | BLUE | red   |
  | BLUE | red   |
  | RED  | blue  |
  | BLUE | blue  |
  | RED  | red   |
  | RED  | blue  |
  | BLUE | red   |
  | RED  | blue  |

  - You can create the table quickly with python with the following code snippet

  ```
  import pandas as pd
  import random
  # create the lists
  words = ['BLUE']*5 + ['RED']*5
  colors = ['blue']*5 + ['red']*5
  # shuffle them and create the dataframe with using them
  random.shuffle(words)
  random.shuffle(colors)
  # create the dataframe with using dictionary declaration
  df_conditions = pd.DataFrame({'word':words, 'color':colors})
  # save the dataframe
  df_conditions.to_csv('conditions.csv')
  ```

### Step 3: Build the Routines

- How to add a Routine:

  - Click on the `Insert Routine` button on bottom left
  - Select `new` and name it `trial` or if you already have `trial` select it

    ![Create new routine](img/add_routine1.png)

  - Now on the `Flow` click on the arrow to place the `trial` routine

    ![Place the new routine](img/add_routine2.png)

  - You `Flow` should look like this:

    ![Flow looks like this](img/add_routine3.png)

- How to add a Text Component:

  - Add a Text component to the routine. Set its properties as follows:

    ![Add a text component](img/text0.png)

    - `Text`: `$word` (use the variable name from your conditions file)
    - `Color`: `$color` (use the variable name from your conditions file)
    - `Duration` (s): Leave it blank or set to a desired duration, e.g., 1.0
    - `Units`: Leave at default

#### `Welcome` Routine

- Click on the `Insert Routine` button on bottom left
- Select `new` and name it `welcome`
- Now let's add a `Text` component from the right hand side
- Name the component, `welcome_txt` might be an option
- To display the welcome screen for `3` seconds set the `Start` to 0 and `Stop` to 3 seconds
  - You can set it how long you want
- Type the welcome text to be shown in the `Text` field
- Click `OK`; now you should have your `welcome` routine
  ![Welcome routine](img/welcome0.png)

#### `Instructions` Routine

- Create the `Instructions` routine first
- One needs a `Text` and `Keyboard` component for the `Instructions` routine as the participants will be let to read the instructions with their own pace
- Add a `Text` component, you can name it `text`
- Do not type in any `Stop` time, this will be checked by the keyboard
- Type in the instructions in the `Text` field and click `OK`
  ![Instructions text field](img/inst_text0.png)

- Now add a `Keyboard` component, name it `key_resp` for keyboard responses
- Again do not type in any `Stop` time
- Set `Register keypress on...` field as `press`
- And allowed keys to `'return'` as we will use the `Enter` key for to move on to the next screen
- Click `OK`
  ![Instructions keyboard press](img/inst_key0.png)

#### `Fixation cross` Routine

- Create the `Fixation` routine first
- Now we need a Fixation cross
- As PsychoPy is able to display polygons via drawing the points specified, we will use the `Polygon` component
- PsychoPy already offers the following options natively, without thinking about the individual points:
  ![Polygon options](img/fix_cross0.png)

  So let's leverage that

- Select `Polygon` component from the menu
- Set the duration to 2 seconds
- Set the `Shape` option to cross
- Now switch to the `Layout` menu and set the size to `(0.1, 0.1)`. This means that we will create a shape with `(width, height)` pair of `10%` of the half of the screen
- In `Appereance` menu, set the `Fill color` and `Border color` to `Black`.
- Click `OK` and now you have the fixation cross!

##### `Stim` Routine

- Next up is displaying the stimuli!
- Create a routine with the name of `stim`
- We need two components for this routine, one `Text` and one `Keyboard`

##### `Checker` Routine

##### `Inter-stimulus Interval` Routine

#### Trial loop
