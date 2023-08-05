Behave Web Api
==============

Provides testing for JSON APIs with Behave

Installation
------------

::

    pip install behave-web-api

Import steps in your features/steps/\ **init**.py

.. code:: python

    from behave_web_api.steps import *

So you can use the steps in your feature files

.. code:: gherkin

    Feature: Doing http requests

      Scenario: Send text body and headers
        Given I set header "X-My-Header" with value "Something"
        When I send a POST request to "/requests/echo" with body:
        """
        Something
        """
        Then the response code should be 200
        And the response should contain json:
        """
            {
                "headers": {
                    "X-My-Header": "Something"
                },
                "body": "%[A-Za-z]+%"
            }
        """

      Scenario: Send file using variables and environment variables
        Given I set the variable "DATA_DIR" with "$PWD/features/data" 
        And I attach the file "$DATA_DIR/favicon.ico" as "upload"
        When I send a POST request to "/requests/echo"
        Then the response code should be 200
        And print response


And run using BASE_URL environment variable:

::

    BASE_URL=localhost:5000 behave features/requests.feature


Available Steps
---------------

-  I set variable "{}" with value "{}"
-  I set header "{}" with value "{}"
-  I attach the file "{}" as "{}"
-  I send a {} request to "{}" with body
-  I send a {} request to "{}" with values
-  I send a {} request to "{}"
-  the response code should be {}
-  the response should contain json
-  the response should contain text
-  print response


Acknowledgments
---------------

The REST steps are based on Behat WebApiExtension [1]_

.. [1] https://github.com/Behat/WebApiExtension
