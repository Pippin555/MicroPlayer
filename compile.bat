pyinstaller micro_player.py --onefile --noconsole
:
pyinstaller select.py --onefile --noconsole
:
copy dist\micro_player.exe c:\bin\micro_player.exe
copy dist\select.exe c:\bin\select.exe
