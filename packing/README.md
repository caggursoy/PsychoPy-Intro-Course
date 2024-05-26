# Part 4: Packing up your Experiment

## Topics:

- PyInstaller
  - Auto-py-to-exe
- Conda

---

## Tutorial: Packing Up Your Experiment as an Executable with PyInstaller

### Step 1: Install PyInstaller

First, you need to install PyInstaller. Open your terminal or command prompt and run:

```bash
pip install pyinstaller
```

### Step 2: Prepare Your Python Script

Ensure your Python script (let's call it `experiment.py`) is working correctly. This is the script you want to convert into an executable.

### Step 3: Create a Spec File (Optional)

A spec file allows you to customize how PyInstaller packages your application. This step is optional but useful for advanced configurations. You can create a spec file using:

```bash
pyi-makespec experiment.py
```

This will generate a file named `experiment.spec`. You can edit this file to change various settings, such as adding data files or setting the entry point.

### Step 4: Package Your Script

To package your script without a spec file, simply run:

```bash
pyinstaller --onefile experiment.py
```

This command will generate a single executable file in the `dist` directory. The `--onefile` option ensures that all dependencies are bundled into one executable.

If you're using a spec file, run:

```bash
pyinstaller experiment.spec
```

### Step 5: Handle Additional Files (Optional)

If your script relies on additional files (like data files, configuration files, etc.), you need to include them in the package. You can do this by editing the spec file.

Open `experiment.spec` and locate the `datas` variable. Add your additional files as tuples of the source path and destination path:

```python
datas=[('path/to/your/datafile', 'datafile')]
```

Then, re-run:

```bash
pyinstaller experiment.spec
```

### Step 6: Test Your Executable

After packaging, navigate to the `dist` directory and find your executable (`experiment.exe` on Windows or `experiment` on Mac/Linux). Run it to ensure it works correctly.

### Additional Tips

- **Hidden Imports**: If you encounter missing module errors, you might need to specify hidden imports using the `--hidden-import` option:

  ```bash
  pyinstaller --onefile --hidden-import=module_name experiment.py
  ```

- **Icon File**: You can specify an icon for your executable using the `--icon` option:

  ```bash
  pyinstaller --onefile --icon=path/to/icon.ico experiment.py
  ```

- **UPX Compression**: If you want to reduce the size of your executable, you can use UPX (Ultimate Packer for eXecutables). Install UPX and add the `--upx-dir` option:

  ```bash
  pyinstaller --onefile --upx-dir=/path/to/upx experiment.py
  ```

### Common Issues and Troubleshooting

- **Missing Modules**: Use the `--hidden-import` option to specify any missing modules.
- **Large Executable Size**: Consider using UPX for compression or review dependencies to remove unnecessary ones.
- **Runtime Errors**: Ensure all necessary files are included and paths are correctly set.

### Future documentation

For more detailed documentation, refer to the [PyInstaller official documentation](https://pyinstaller.readthedocs.io/en/stable/).

## OR you can use the package auto-py-to-exe

Which is a GUI written on top of PyInstaller!

![Auto-py-to-exe image](https://pypi-camo.freetls.fastly.net/eb29c9774b11dab42fbee0e2c5e9cf2af72895fc/68747470733a2f2f6e6974726174696e652e6e65742f706f7374732f6175746f2d70792d746f2d6578652f666561747572652e706e67)

## Guide: Using `auto-py-to-exe` to Convert Python Scripts to Executables

### Step 1: Install `auto-py-to-exe`

First, you need to install `auto-py-to-exe`. You can do this using `pip`. Open your terminal or command prompt and run:

```bash
pip install auto-py-to-exe
```

### Step 2: Launch `auto-py-to-exe`

Once installed, you can launch the graphical interface of `auto-py-to-exe` by running:

```bash
auto-py-to-exe
```

This command will open up the `auto-py-to-exe` graphical user interface (GUI).

### Step 3: Select Your Script

In the GUI, you'll see a field labeled "Script Location." Click "Browse" and navigate to the Python script you want to convert into an executable. Select your script (e.g., `your_script.py`).

### Step 4: Configure the Settings

#### Onefile vs. Directory

- **Onefile**: Select this option to bundle everything into a single executable file.
- **Directory**: Select this option to create a directory with the executable and all its dependencies.

#### Console Window

- **Console Based**: Select this option if your script runs in a console window (i.e., command line).
- **Window Based**: Select this option if your script has a graphical user interface (GUI) and you do not want a console window to appear.

#### Icon

If you want your executable to have a custom icon, click "Browse" under the "Icon" section and select an `.ico` file.

#### Additional Files

If your script relies on additional files (e.g., data files, configuration files), you can add them in the "Additional Files" section by clicking "Add Files" or "Add Folder."

### Step 5: Advanced Options

If you need to specify additional options like hidden imports or run-time hooks, you can do so in the "Advanced" section. This is useful if your script imports modules dynamically or has special requirements.

### Step 6: Convert the Script

Once you've configured all the necessary options, click the "Convert .py to .exe" button at the bottom. `auto-py-to-exe` will start the conversion process. You can see the progress and any messages in the output panel.

### Step 7: Locate the Executable

After the process completes, the output directory will contain your executable. If you selected "Onefile," you will see a single executable file. If you selected "Directory," you will find a folder containing your executable and its dependencies.

### Troubleshooting Common Issues

- **Missing Modules**: If you encounter missing module errors, ensure all necessary modules are installed in your environment. You can add hidden imports in the "Advanced" section.
- **Large Executable Size**: To reduce the size, consider using UPX (Ultimate Packer for eXecutables) for compression. You can install UPX and then select the "UPX" option in the settings.
- **Runtime Errors**: Make sure all additional files and dependencies are included correctly. Check the paths and configurations.

### Example Configuration

Here’s an example of what the configuration might look like for a simple script:

- **Script Location**: `your_script.py`
- **Onefile**: Selected
- **Window Based**: Selected (if using a GUI)
- **Icon**: Path to your custom `.ico` file (optional)
- **Additional Files**: Added necessary data files

### Conclusion

`auto-py-to-exe` provides a straightforward and user-friendly way to convert your Python scripts into standalone executables. By following the steps above, you can easily package your script and share it with others, ensuring it runs on their systems without requiring a Python installation.

For more detailed information, you can visit the [official documentation of auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/).

Feel free to ask if you have any specific questions or need further assistance!

---

## Step-by-Step Guide to Creating a Reproducible `environment.yml`

### Step 1: Create a New Conda Environment

Start by creating a new Conda environment. Open your terminal or Anaconda prompt and run:

```bash
conda create --name myenv python=3.9
```

Replace `myenv` with the name you want for your environment and `3.9` with the desired Python version.

### Step 2: Activate the Environment

Activate the newly created environment:

```bash
conda activate myenv
```

### Step 3: Install Required Packages

Install the necessary packages for your project. For example:

```bash
conda install numpy pandas scipy matplotlib
pip install some-external-package
```

### Step 4: Export the Environment

Once all required packages are installed, export the environment to a `yml` file:

```bash
conda env export --no-builds > environment.yml
```

The `--no-builds` flag ensures the environment is more reproducible by excluding specific build versions of packages, making it more likely to work across different systems.

### Step 5: Edit the `environment.yml` (Optional)

Open the `environment.yml` file and review its contents. It should look something like this:

```yaml
name: myenv
channels:
  - defaults
dependencies:
  - python=3.9
  - numpy=1.21.2
  - pandas=1.3.3
  - scipy=1.7.1
  - matplotlib=3.4.3
  - pip:
      - some-external-package==0.1.2
```

You can add any additional details or dependencies here. Ensure external packages installed via `pip` are listed under the `pip` section.

### Step 6: Share and Recreate the Environment

Share the `environment.yml` file with your collaborators. They can recreate the same environment using:

```bash
conda env create -f environment.yml
```

To update an existing environment with changes from the `environment.yml`, use:

```bash
conda env update --file environment.yml
```

### Additional Tips

- **Locking Dependencies**: For stricter reproducibility, you might consider using a tool like `conda-lock`, which generates lock files similar to `pip freeze`.

  ```bash
  pip install conda-lock
  conda-lock -f environment.yml
  ```

  This generates a `conda-lock.yml` file that can be used to recreate the environment with exact versions.

- **Environment Management**: List all environments with `conda env list` and remove an environment with `conda env remove --name myenv`.

### Example `environment.yml`

Here’s a complete example of what an `environment.yml` might look like:

```yaml
name: myenv
channels:
  - defaults
dependencies:
  - python=3.9
  - numpy=1.21.2
  - pandas=1.3.3
  - scipy=1.7.1
  - matplotlib=3.4.3
  - pip:
      - some-external-package==0.1.2
```
