lambda-controller
===============

Command line utility for AWS Lambda.

Installation
~~~~~~~~~~~~

The latest release of lambda-controller can be installed via pip:

::

    pip install lambda-controller

An alternative install method would be manually installing it leveraging
``setup.py``:

::

    git clone https://github.com/cloudfish7/lambda-controller
    cd lambda-controller
    python setup.py install


Command Line Usage
~~~~~~~~~~~~~~~~~~

See the Lambda Function List

.. code:: shell

    lambda-controller --list

See the Lambda Function Info

.. code:: shell

    lambda-controller --detail

To invoke Lambda Function

.. code:: shell

    lambda-controller --invoke FunctionName


