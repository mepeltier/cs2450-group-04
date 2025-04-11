# CS 2450 Group 04 — UVSim

This is currently a Proof of Concept UVSim parser for the BasicML language. It currently has support for the following commands:

**I/O operation:**
- `READ = 10` Read a word from the keyboard into a specific location in memory.
- `WRITE = 11` Write a word from a specific location in memory to screen.

**Load/store operations:**
- `LOAD = 20` Load a word from a specific location in memory into the accumulator.
- `STORE = 21` Store a word from the accumulator into a specific location in memory.

**Arithmetic operation:**
- `ADD = 30` Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
- `SUBTRACT = 31` Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
- `DIVIDE = 32` Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
- `MULTIPLY = 33` multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

**Control operation:**
- `BRANCH = 40` Branch to a specific location in memory
- `BRANCHNEG = 41` Branch to a specific location in memory if the accumulator is negative.
- `BRANCHZERO = 42` Branch to a specific location in memory if the accumulator is zero.
- `HALT = 43` Pause the program

## Poetry
This project is managed with [Poetry](https://python-poetry.org/). In order to run this project, first install Poetry, through one of the recommended methods described by its documentation. Once Poetry is installed, see the following commands:

`$ poetry lock` -- This step shouldn't be necessary, but it will make sure that the lockfile is up to date with the latest versions.

`$ poetry install --all-extras` -- This creates a `.venv/` folder, in which poetry installs all the necessary libraries to run this project.

Once that is completed, run the program with `$ poetry run python -m src.main`

And run tests with `$ poetry run pytest tests/`

> Note: Some installations of Python don't ship with `tkinter` by default. You need to make sure your Python 3.12 version is setup to use `tkinter` before creating the virtual environment with Poetry. 
> If you're on MacOS, using Pyenv to manage your Python versions: 
> 1. Run `$ brew install tcl-tk`
> 2. Add `tcl-tk` to PATH (something like this: `$ echo 'export PATH="/opt/homebrew/Cellar/tcl-tk/9.0.1/bin:$PATH"' >> ~/.zshrc`) 
> 3. Run `$ pyenv install 3.12.9`
> 4. Modify Pyenv's version file (whose location can be found by running `$ pyenv version-file`) to read `3.12.9`
>
> Then proceed with the Poetry instructions as listed above. If you already have Python 3.12.9 installed via Pyenv, you may need to uninstall it before these steps
>
> If these steps fail, you can always attempt to run the program without Poetry. You'll need to install the dependencies manually (`$ pip install <pkg>`) for `termcolor`, and `pytest`, if you want to run the test scripts. Then you can run `$ python -m src.main` without Poetry involved.