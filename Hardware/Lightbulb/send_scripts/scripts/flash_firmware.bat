@echo off

echo Starting job...

echo.
CALL esptool -p %port% erase_flash

echo.
CALL esptool -p %port% write_flash 0x0 "scripts\utils\micropython-v1.8.7.bin"

echo.
echo Done. Please reset the module.