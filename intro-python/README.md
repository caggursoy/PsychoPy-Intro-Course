# Part 1: Introduction to Python (in an hour or so)

## Fundamental Concepts in Python

### Basic Data Types

- **Strings**: Immutable sequences of characters. Useful for text manipulation.

  - Creation: `s = "Hello, world!"`
  - Basic operations: concatenation (`+`), repetition (`*`), slicing (`s[1:5]`).

- **Integers and Floats**: Basic numeric types for mathematical operations.

  - Operations: addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), floor division (`//`), modulus (`%`), power (`**`).

- **Conversions**: Converting between `int`, `float`, and `str`.
  - `int("10")`, `float(5)`, `str(20.5)`

### Collections: Lists and Dictionaries

- **Lists**: Ordered collections of items.

  - Creating lists: `numbers = [1, 2, 3, 4]`
  - Accessing elements, slicing, appending, removing.
  - List comprehensions for efficient data processing.

- **Dictionaries**: Key-value pairs for storing linked data.
  - Creation: `person = {"name": "John", "age": 30}`
  - Accessing and setting values, keys, values, and items methods.

### Loops

- **For loops**: Iterating over a range or collection.

  - `for i in range(5): print(i)`
  - Looping through lists, dictionaries.

- **While loops**: Running a block of code until a condition changes.
  - `while x < 5: x += 1`

### Numpy, Pandas, and Matplotlib (Seaborn)

- **NumPy**: Basics of array creation and operations.

  - Creating arrays, basic array operations.

- **Pandas**: Introduction to `DataFrame`s and basic manipulations.
  - Reading data, selecting data, summary statistics.
- **Matplotlib**: Basic plotting functions.
  - Line plot, histogram, scatter plot.

### Functions

- Defining functions, return values, parameters.
  - Example: `def add(x, y): return x + y`

### Debugging

- Common types of errors: syntax, runtime, and logic errors.
- Using print statements or using IDEs/debuggers to trace and fix errors.

## Optional: Data Analysis

### 1. Introduction to Data Analysis with Python

- Overview of Python’s ecosystem for data analysis (Pandas, NumPy, SciPy, Matplotlib).

### 2. Data Visualization Using Matplotlib

- Basic chart types and when to use them.
- Customizing plots (titles, labels, legends).

### 3. Basic Statistical Analysis with Pandas

- Calculating mean, median, mode.
- Simple correlations, handling missing values.

## Virtual Environments in Python

### 1. Conda

- Benefits of using Conda environments for Python projects.
- Basic commands:
  - creating an environment
    - `conda create -n yourenvname python=x.x`
  - activating an environment
    - `conda activate yourenvname`
  - installing packages
    - `conda install numpy`
