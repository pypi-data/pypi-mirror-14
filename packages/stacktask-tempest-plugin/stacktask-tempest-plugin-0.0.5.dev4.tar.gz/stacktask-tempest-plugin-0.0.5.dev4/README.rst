Stacktask Tempest Plugin
=====================
Tempest plugin that runs a Stacktask test case.

============
Installation
============
You can install the plugin using pip, directly into the python environment tempest uses (either global or a virtualenv):

.. code-block:: bash

    $ cd tempest
    $ source .venv/bin/activate
    $ pip install stacktask-tempest-plugin

    # Or, for the development testpypi version:
    $ pip install -i https://testpypi.python.org/pypi --upgrade stacktask-tempest-plugin

============
Running tests
============
1. Install either the development or pypi versions using pip.

2. To validate that Tempest discovered the tests in the plugin, you can run:

   .. code-block:: bash

    $ testr list-tests | grep stacktask_tempest_plugin

   This command will show your complete list of test cases inside the plugin.


2. Run the test cases by name, or include in your tempest test lists.

   .. code-block:: bash

    $ testr run stacktask_tempest_plugin.tests.api.test_users.StacktaskProjectAdminTestUsers.test_get_users


============
Development Installation
============
When Tempest runs, it will automatically discover the installed plugins. So we just need to install the Python packages that contains the plugin.

Clone the repository in your machine and install the package from the src tree:

.. code-block:: bash

    $ cd stacktask-tempest-plugin
    $ sudo pip install -e .

============
Pypi package creation
============

There are better guides for pypi, but the basic commands may be useful.
These steps require a pypi account, configured in ~/.pypirc

Register the project with pypi:

.. code-block:: bash

    $ python setup.py register -r pypitest


Upload a new version:

.. code-block:: bash

    $ python setup.py sdist upload -r pypitest

Increment the version number in setup.cfg for any new versions that need to be uploaded.
Remove the '-r pypitest' for offical deploys.
