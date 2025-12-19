python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=00000000-0000-0000-0000-000000000000"

python app.py
http://localhost:8000