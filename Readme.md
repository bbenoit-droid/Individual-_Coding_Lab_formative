# Grade Evaluator Submission

This repository contains:

1. `grade-evaluator.py` - Python script for reading and evaluating student grades from a CSV file.
2. `organizer.sh` - Bash script for archiving a CSV file and creating a fresh `grades.csv`.
3. `Readme.md` - Usage instructions for both scripts.

## Requirements

- Python 3
- Bash shell

## CSV Format

The grade CSV file should use this header:

```csv
assignment,group,score,weight
```

Example:

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

## Running the Python Script

Run the evaluator with:

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV file name, for example:

```text
grades.csv
```

The script will:

- Read the CSV file
- Validate scores and weights
- Enforce the `60/40` Formative/Summative split
- Calculate the final grade, letter grade, and GPA
- Determine pass or fail status
- Show resubmission options for failed formative assignments

## Running the Bash Script

Make the script executable if needed:

```bash
chmod +x organizer.sh
```

Run it with the default working file:

```bash
./organizer.sh
```

Or run it with a specific CSV file path:

```bash
./organizer.sh /path/to/grades.csv
```

The script will:

- Create the `archive/` folder if it does not exist
- Move and rename the source CSV with a timestamp
- Create a fresh `grades.csv` with the correct header
- Append an entry to `organizer.log`

## Output Files

- Archived CSV files are stored in `archive/`
- Archive history is recorded in `organizer.log`
- A new working file is recreated as `grades.csv`
