@ECHO off

SET inpath=D:\Google Drive\Classes\Senior Project\Workspace\Transcend\Hardware\Lightbulb
for /f "tokens=4" %%A in ('mode^|findstr "COM[0-9]"') do set port=%%A
SET port=%port:~0,4%