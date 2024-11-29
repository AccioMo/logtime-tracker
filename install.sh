python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
echo 'do shell script "$VIRTUAL_ENV/bin/python3 $VIRTUAL_ENV/src/logtime.py"' > logtime.applescript
osacompile -o logtime.app logtime.applescript
osascript -e 'tell application "System Events" to make login item at end with properties {path:"$PWD/logtime.app", hidden:false}'
