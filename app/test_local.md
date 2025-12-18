python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=e826256d-d6a1-40c4-a22c-370bb3f797bc"

python app.py
http://localhost:8000