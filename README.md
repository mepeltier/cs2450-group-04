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


Once those setup steps are completed, you can use `$ poetry run pytest tests/` to run the tests or `$ poetry run python src/main.py <file path>` to run the main program with a BasicML file. `Test1.txt` and `Test2.txt` are included here for convenience

#TODO: Actually make sure that we can read in a file name ^^