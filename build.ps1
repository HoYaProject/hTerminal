.\.venv\Scripts\activate
pyinstaller --clean -w -F --specpath=spec -n="hTerminal_for_NXP_v1.0.0" --add-data="..\resource\favicon.ico;.\resource" -i="..\resource\logo.ico" src\main.py
deactivate