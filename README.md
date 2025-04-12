# PyOrganizer

**PyOrganizer** is a command-line utility for organizing files in a directory based on custom rules such as file type or modification date.

## Features

- Organize files by extension or modification date
- Simple, modular codebase using object-oriented design
- Easy to extend with future rules
- CLI interface using `argparse`
- Uses only the Python Standard Library

## Getting Started

### Requirements

- Python 3.8+
- No external libraries (standard library only)

### Setup

### Clone the repository

`git clone https://github.com/ssk367/pyorganizer.git
cd pyorganizer`

Create and activate virtual environment (Windows PowerShell)

`python -m venv venv `

`.\venv\Scripts\Activate`

### Run script → python pyorganizer.py

`pyorganizer/
│
├── organizer/           # Core modules
│   ├── scanner.py       # FileScanner class
│   ├── sorter.py        # FileCategorizer class (coming soon)
│   ├── mover.py         # FileMover class (coming soon)
│   └── logger.py        # Logger config (planned)
│
├── sample_files/        # Test folder with random files
├── pyorganizer.py       # CLI entry point
├── requirements.txt     # Dependency list
├── .gitignore
└── README.md`
