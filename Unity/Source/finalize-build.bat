@ECHO OFF


robocopy "%CD%/transcend-broker" "%CD%/../Build/transcend_demo_Data/transcend-broker" /S /XD "__pycache__" /NJH /NJS /NDL
robocopy "%CD%/UX-scripts/" "%CD%/../Build/" /NJH /NJS /NDL