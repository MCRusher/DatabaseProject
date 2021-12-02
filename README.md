# DatabaseProject
Group project for UAkron DatabaseManagement

# Dependencies

Python Dependencies:
- requests
- selenium
- kaggle
- pandas
- sqlite3 (comes with python)

Other Dependencies:
- A 'kaggle.json' API key inside a '.kaggle' directory located in the project directory
- firefox
- geckodriver in the project directory (or possibly in the path)

# Setup

1. Clone or save as zip
2. install python dependencies
3. Create .kaggle directory
4. Create a free kaggle account and generate an API Key in account settings
5. Save the api key file 'kaggle.json' in the '.kaggle' directory
6. download geckodriver from https://github.com/mozilla/geckodriver/releases
7. unzip and place executable in the project directory
8. open commandline in project directory
9. run ```python download_data.py``` to collect datasheets necessary to populate database
10. run ```python setup_data.py``` to populate the database with the datasheets

# Usage

1. Peform setup steps
2. run ```flask run``` to start the server application
