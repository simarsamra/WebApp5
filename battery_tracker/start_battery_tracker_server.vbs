Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c venv\Scripts\activate && python setup_and_run.py", 0, False