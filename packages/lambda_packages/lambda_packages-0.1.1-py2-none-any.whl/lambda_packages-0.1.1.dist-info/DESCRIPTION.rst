lambda-packages |Build Status| |Slack|
======================================

Various popular libraries, pre-compiled to be compatible with AWS
Lambda.

Installation
------------

::

    pip install lambda-packages

Usage
-----

**lambda-packages** also includes a manifest with information about the
included packages and the paths to their binaries.

.. code:: python

    from lambda_packages import lambda_packages

    print lambda_packages['psycopg2']['version'] 
    # 2.6.1
    print lambda_packages['psycopg2']['path'] 
    # /home/YourUsername/.venvs/lambda_packages/psycopg2/psycopg2-2.6.1.tar.gz

.. |Build Status| image:: https://travis-ci.org/Miserlou/lambda-packages.svg
   :target: https://travis-ci.org/Miserlou/lambda-packages
.. |Slack| image:: https://img.shields.io/badge/chat-slack-ff69b4.svg
   :target: https://slackautoinviter.herokuapp.com/


