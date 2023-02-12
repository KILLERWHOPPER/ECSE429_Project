Test were written with Python 3.10+
The test report is generated using pytest-html and can be found [here](https://htmlpreview.github.io/?https://github.com/KILLERWHOPPER/ECSE429_Project/blob/master/res/report.html).

To run the tests locally, run the following commands (powershell):
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

# run tests with stdout
pytest -s
```

The failed tests are considered as unexpected results from the APIs tested.
