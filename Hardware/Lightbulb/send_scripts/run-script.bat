@ECHO off

ECHO.
ECHO See /scripts for available scripts

SET /P SCRIPT="Script to run (lowercase): "

ECHO.
ECHO Getting port and setting path...
CALL scripts/set_path.bat

ECHO.
ECHO Removing main.py from microcontroller...
CALL scripts/remove_main.bat

ECHO.
ECHO Running job...
CALL scripts/%SCRIPT%.bat

ECHO.
ECHO Done.