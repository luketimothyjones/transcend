@echo off

CALL set_path
echo Starting job...

echo.
CALL esptool -p %port% erase_flash

echo.
CALL esptool -p %port% write_flash 0x0 "D:\Google Drive\Classes\Senior Project\Workspace\ESP8266 Resources\Firmware\MicroPython\micropython-v1.8.7.bin"

echo.
CALL ampy -p %port% reset

echo.

@echo on
CALL all

echo.
echo Done