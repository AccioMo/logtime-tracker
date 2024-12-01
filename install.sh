python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
echo 'do shell script "'$VIRTUAL_ENV'/bin/python3 '$PWD'/logtime_tracker.py > /dev/null 2>&1 &"' > logtime_tracker.applescript
osacompile -o logtime_tracker.app logtime_tracker.applescript
STARTUP_SCRIPT='tell application "System Events" to make login item at end with properties {path:"'$PWD'/logtime_tracker.app", hidden:true}'
echo $STARTUP_SCRIPT
osascript -e "$STARTUP_SCRIPT"
open -g logtime_tracker.app
echo "alias logtime='$VIRTUAL_ENV/bin/python3 $PWD/get_logtime.py'" >> ~/.bash_profile
echo "alias logtime='$VIRTUAL_ENV/bin/python3 $PWD/get_logtime.py'" >> ~/.zshrc
echo 'Installation complete. '