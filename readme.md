# Unit Tests
The unit tests were written with Python 3.10+ and are located in this [folder](/src/).
The test report is generated using pytest-html and can be found [here](https://htmlpreview.github.io/?https://github.com/KILLERWHOPPER/ECSE429_Project/blob/master/res/report.html).
Each failed test means that the API is not working as expected.

To test locally, run the following commands (powershell):
```powershell
# create virtual environment
python -m venv venv

# activate virtual environment
venv/Scripts/activate

# install dependencies
pip install -r requirements.txt

# run tests and generate report
pytest --html=res/report.html --self-contained-html 

# run tests only
pytest
```

<br/>

# Shell Scripts
Located in this [folder](/shell_scripts/), the shell scripts were ran and tested with WSL2 on Windows 10.