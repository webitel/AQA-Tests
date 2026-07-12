# Webitel API Tests

This project has been created for API tests


### Prerequisites

* Install Python 3.12.10

* Install pip3

* Install External libraries via requirements.txt

### Pycharm

* Install Pycharm
* Set Python Interpreter
* Set PyTest as default test runner

## Running the tests

* Via console command

```
Example:
Open the Project
- Run command in the terminal: pytest -v tests/test_your_test.py
```

* Additional commandline arguments

--env - selected server
```
--env=test - test server
--env=dev - development server
--env=prod - production server
```

--maxfail - stop tests after failure
```
--maxfail=1
```

-n; --numprocesses x - set amount of x threads
```
--numprocesses 2
```

--count - repeat a single test, or multiple tests, a specific number of times
```
--count=10 - 10 times
```

--alluredir - path to allure results
```
--alluredir=/path_to_dir_with_allure_reports/allure-results
```

-m markname - run marked tests
```
-m "smoke"
```

python -u -m "pytest" -v -m "${_marker}" --env="${_env}" tests/ -n 10 --alluredir=allure-results/ --junitxml=report.xml