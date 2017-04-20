@ECHO OFF

SET inpath=..
for /f "tokens=4" %%A in ('mode^|findstr "COM[0-9]"') do set port=%%A
SET port=%port:~0,4%
SET ampy=scripts\utils\ampy