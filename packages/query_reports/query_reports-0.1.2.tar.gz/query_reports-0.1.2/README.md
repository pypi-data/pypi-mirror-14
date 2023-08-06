Query Reports
========================

Query Reports creates reports based on the django queryset object.


## Using the pretty bootstrap template

If you want to use a pretty bootstrap template instead of the normal site `base.html`
you can override `query_reports/base.html` and just put this in the file

    {% extends "query_reports/bootstrap_base.html" %}


## Running the Tests

You can run the tests with via

    python setup.py test

or

    python run_tests.py
