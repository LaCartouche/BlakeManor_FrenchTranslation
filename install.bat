@echo off
rem Blake Manor FR - Windows installer. Double-click, or: install.bat -Uninstall
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
echo.
pause
