@echo off
cd /d %~dp0

:menu
cls
echo ==============================
echo        PY BOT LAUNCHER
echo ==============================
echo.
echo  run     - clone + build + start
echo  build   - install deps + preflight
echo  deploy  - start bot only
echo  env     - load env
echo  exit
echo.

set /p cmd=Command: 

if /i "%cmd%"=="run" goto run
if /i "%cmd%"=="build" goto build
if /i "%cmd%"=="deploy" goto deploy
if /i "%cmd%"=="env" goto env
if /i "%cmd%"=="exit" exit

echo Unknown command
pause
goto menu

:run
powershell -ExecutionPolicy Bypass -File ".\scripts\start.ps1"
pause
goto menu

:build
powershell -ExecutionPolicy Bypass -File ".\scripts\build.ps1"
pause
goto menu

:deploy
powershell -ExecutionPolicy Bypass -File ".\scripts\deploy.ps1"
pause
goto menu

:env
powershell -ExecutionPolicy Bypass -File ".\scripts\env.ps1"
pause
goto menu