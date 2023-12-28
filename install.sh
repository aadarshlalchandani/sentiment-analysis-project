python -m venv env
. env/bin/activate
libs="pip wheel setuptools"
python -m pip install -U $libs
pip install -r requirements.txt