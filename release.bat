REM @echo off

SET cur_dir=%~dp0

DEL %cur_dir%version.py

wscript.exe %cur_dir%versionfile-gen.vbs %cur_dir%version.py %1
