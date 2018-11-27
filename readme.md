virtualenv venv -p python3

source venv/bin/activate

pip install --upgrade pip

pip install --upgrade setuptools urllib3[secure]

pip install git+https://github.com/mlockett42/py-eos-api@46c25eae0ecce048cd85b97d06534c8bbd390a35

pip install pytest


Instructions (Notes)

git clone project

use readme to do important things

refer to binary crate readme

1. venv
2. unit tests
3. test runner


Set-up
--> Install pytest:
    - In your command line:
        >> pip install -U pytest
        >> pytest --version
    - Your should have pytest version 3.x.y
--> Install future (for testing):
    - In your command line:
        >> pip install future
    - This will be used for testing where:
        from __future__ import absolute_import
