rem %1 is the folder of the pyinstaller
%1/pyinstaller micro_player.py --exclude-module pkg_resources --onefile --noconsole
:
copy dist\micro_player.exe c:\bin\micro_player.exe
:
rem select.exe might be re-introduced in future
rem %1/pyinstaller select.py --onefile --noconsole
rem copy dist\select.exe c:\bin\select.exe
