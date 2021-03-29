rm -rf venv
python -m venv venv
venv/scripts/python.exe -m pip install --upgrade pip
venv/scripts/python.exe -m pip install -r requirements.txt -r requirements-dev.txt
venv/scripts/python.exe -m pip install -e .