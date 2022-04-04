# MaveCore
Shared MaveDB and MaveTools functionality

## Contributing

To contribute to MaveCore development, please install the additional requirements:
```
pip install -r requirements-dev.txt
```

To run the tests and generate an HTML coverage report use:
```
coverage run -m unittest && coverage html
```

By default, the coverage report will be located at `htmlcov/index.html`.
Open this file in your browser to identify lines that have not been adequately covered by the test suite.
