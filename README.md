# **Poetry issues data analytics**

This is a software to analyze insightful trends from the open source project: [poetry](https://github.com/python-poetry/poetry/issues)

## **Setup**

Clone this repository either from [ENPM611-project-team3](https://github.com/joyson13/ENPM611-project-team3.git) or using the git command line interface

## **Prerequisites**

1. Python v3.10 or above (latest version recommended)
2. pip v23 or above
3. poetry_issues.json file (JSON array of all the issues of the target repository) in data folder

## **Install dependencies**

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

## **Run an analysis**

The file to execute is `run.py`
Command syntax

```
python run.py -f | --feature FEATURE [-u | --user USER] [-l | --label LABEL]
```

## **Analysis features**
### **1. Bug Pattern analysis**
  **Description:** Analyze frequency distribution of types of bug (optionally for a specific user) \
  **Options accepted:** `-u | --user USER` (Analyzes for all users if not provided)\
  **Command Syntax:** 
  ```
  python run.py -f | --feature 1 [-u | --user USER]
  ```
  Replace `USER` with the GitHub username you wish to analyze

  **Example:** 
  ```
  python run.py --feature 1
  ```
  **Example with user option:** 
  ```
  python run.py --feature 1 --user ghost
  ```

### 2. Contributor and Assignee analysis
  **Description:** Fetch the most engaged contributors and assignees (optionally for a specific issue label)\
  **Options accepted:** `-l | --label LABEL` (Analyzes for all labels if not provided)\
  **Command Syntax:** 
  ```
  python run.py -f | --feature 2 [-l | --label LABEL]
  ```
  Replace `LABEL` with the issue label you wish to analyze

  **Example:** 
  ```
  python run.py --feature 2
  ```
  **Example with label option:** 
  ```
  python run.py --feature 2 --label kind/bug
  ```

### 3. Severity and Impact analysis
  **Description:** Identify trends in severity patterns and the impact generated by issues\
  **Command Syntax:** 
  ```
  python run.py -f | --feature 3
  ```
  **Example:** 
  ```
  python run.py --feature 3
  ```

## Description of Options
`-f | --feature FEATURE`: provide the corresponding feature number (from above) to run analysis\
`-u | --user USER`: provide a valid username\
`-l | --label LABEL`: provide a valid label

## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.