@echo off
chcp 65001
echo.
pushd %~dp0

:loopstart

::Attempts to start py launcher without relying on PATH
%SYSTEMROOT%\py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO attempt
%SYSTEMROOT%\py.exe -3.5 "C:\Users\victo\Documents\Game Programming\WorldSim\worldsim.py"

pause
goto loopstart

:end