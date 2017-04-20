@echo off

%ampy% -p %port% run "scripts\utils\fix_filesystem.py"
echo Successfully cleaned filesystem