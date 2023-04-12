Project for the Master's Thesis in the University Master's Degree in Logic, Computing and Artificial Intelligence at
the University of Seville.

[![codecov](https://codecov.io/gh/frapercan/experience-recorder/branch/main/graph/badge.svg?token=hIyfvLsU2D)](https://codecov.io/gh/frapercan/experience-recorder)
[![PyPI version](https://badge.fury.io/py/experience_recorder.svg)](https://badge.fury.io/py/experience_recorder)



# Experience Recorder
Utility that supports the task of recording Human Computer Interactions. 
It has been tried to be modeled following human notions but concepts useds are still adopting new forms.
This module basically includes python programs based on a global configuration that generates specific tasks configuration:
* keyboard and mouse listeners
* Senses abstraction such as sight or ear for computer ports extraction/injection.
* Skills abstraction such as read or watch for postprocesses of senses.
* Configuration handling
* Docs (Sphinx)
* Tests (Pytest)
* CI/CD with poetry using GitHub Actions

This project is designed to support the creation of agents using reinforcement learning through an environment based
exclusively on the interface between ourselves and our computer.

# Software Prerequisites

| Component                | Description                                  |
|--------------------------|----------------------------------------------|
| Linux based distribution | Ubuntu 22.04 recommended                     |
| python3                  | Version 3.10                                 |
| Poetry                   | Python dependency management and packaging   |
| PaddlePaddle             | Optical Character Recognition external package |
| xdotool                  | simulate keyboard input and mouse activity   |


# Global Configuration
High level parameters related to system and model configuration. 
```
    datasets_dir: ./datasets
    buffer_dir: ./__buffer__/
    tasks_configuration_dir: ./conf/tasks
    task: 2048                              # Task identifier
    language: en                            # OCR language selection
```

# Task configuration
Specific task configuration with senses and skills. 
This can be automatically generated using Configuration Module.
```
    keyboard: true
    mouse: true
    senses:
      board:
        kind: see
        location:
          height: 490
          left: 712
          top: 348
          width: 494
        skill: watch
      score:
        kind: see
        location:
          height: 28
          left: 944
          top: 178
          width: 133
        skill: read
    task: '2048'
```
This is the configuration for playing [2048](https://play2048.co/). It looks for watching the board
and reading the score using OCR. 

# Human Computer Interfaces
* Monitor (Xlib)
* Mouse 
* Keyboard
* Audio channel (Not implemented)
* Clock (Timeseries indexing burly implemented)

# Senses
* **Sight** tracks monitor specific zones.
* **Ear** tracks audio channel (Not implemented)

# Skills
* **Watch** stores the latest monitor state 
* **Read** stores the text contained in latest monitor state using *Optical Characters Recognition*
* **Detect**  (Not implemented)
* **Listen** (Not implemented)

# Intendeds behaviour
Givens a configuration, generate a buffer tracking interfaces that allows pairing states to the user actions.
The given example is a configuration for playing 2048 task. 
It maps board and score state to the given action. Action can be virtual or a real experience from an agent. 
