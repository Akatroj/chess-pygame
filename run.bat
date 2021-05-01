@ECHO OFF
pip3 install -r requirements.txt || pip install -r requirements.txt
python3 src/main.py || python src/main.py || py src/main.py
