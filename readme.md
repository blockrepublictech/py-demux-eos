virtualenv venv -p python3

source venv/bin/activate

pip install --upgrade pip

pip install --upgrade setuptools urllib3[secure]

pip install git+https://github.com/mlockett42/py-eos-api@46c25eae0ecce048cd85b97d06534c8bbd390a35
