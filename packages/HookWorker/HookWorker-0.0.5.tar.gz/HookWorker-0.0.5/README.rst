.. image:: https://readthedocs.org/projects/hook-worker/badge/?version=latest
    :target: http://hook-worker.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
    
.. image:: https://badge.fury.io/py/HookWorker.svg
    :target: https://badge.fury.io/py/HookWorker
    :alt: Latest version

Lightweight API to deploy on the machine distributing the test on a
redis connection

Commands
========

``hookworker-api [-h] [-p PORT] [-d DOMAIN] [-g DEBUG] [-s SECRET] [-n] [-o PATH] [-e LEVEL] [-r REDIS] [-w]``

+-----------------------+-------------------------------------------------------+------------+
| Parameter / Syntax    | Description                                           | Concerns   |
+=======================+=======================================================+============+
| -p PORT, --port       | PORT Port to use to run the API                       | Redis      |
+-----------------------+-------------------------------------------------------+------------+
| -g DEBUG, --debug     | DEBUG Debug mode for the API                          | API        |
+-----------------------+-------------------------------------------------------+------------+
| -s SECRET, --secret   | SECRET Secret used to secure data exchanges in Hook   | API        |
+-----------------------+-------------------------------------------------------+------------+
| -o PATH, --path       | PATH Path to use for storing logs                     | API        |
+-----------------------+-------------------------------------------------------+------------+
| -e LEVEL, --level     | LEVEL Level of logging                                | API        |
+-----------------------+-------------------------------------------------------+------------+
| -r REDIS, --redis     | REDIS Redis address                                   | Redis      |
+-----------------------+-------------------------------------------------------+------------+
| -w WORKER, --workers  | Number of workers to use for HookTest                 | API        |
+-----------------------+-------------------------------------------------------+------------+
| -g GIT, --git         | Path where you would like to do the cloning           | API        |
+-----------------------+-------------------------------------------------------+------------+
| -h, --help            | show this help message and exit                       |            |
+-----------------------+-------------------------------------------------------+------------+
| -q, --rq              | Run the worker                                        | Redis      |
+-----------------------+-------------------------------------------------------+------------+
| -a, --api             | Run the api                                           | API        |
+-----------------------+-------------------------------------------------------+------------+

