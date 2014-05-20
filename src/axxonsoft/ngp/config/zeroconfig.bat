@echo off

set PATH=%PATH%;%WINDIR%\SYSTEM32

taskkill /f /t /fi "services eq ngp*"
taskkill /F /T /IM AppHost.exe
taskkill /F /T /IM NetHost.exe

rem Detect architecture
set REG_PATH="HKLM\SOFTWARE\Wow6432Node\AxxonSoft\AxxonSmart\InstallPropertyInfo"
if %PROCESSOR_ARCHITECTURE% == x86 set REG_PATH="HKLM\SOFTWARE\AxxonSoft\AxxonSmart\InstallPropertyInfo"

rem Get AxxonSmart install path and parse it to drive and path
for /f "tokens=2*" %%i in ('reg query %REG_PATH% /v InstallDir ^| find "InstallDir"') do (
	set SMARTDRIVE=%%~dj
	set SMARTPATH=%%~pj
)
set HG="%SMARTPATH%\bin\hg.exe"
rem Change current directory to SmartIP location
%SMARTDRIVE%
cd %SMARTPATH%
rem remove SharedDatabase
for /d %%p in (SharedDatabase\base.*) do rd /s /q "%%p"
for /d %%p in ( SharedDatabase\repository_clone.*) do rd /s /q "%%p"
rem remove current configuration
rd /q /s Config\config_repo
for /d %%p in (Config\repository_clone.*) do rd /s /q "%%p"
rem create empty folder
md Config\config_repo

rem extract initial configuration
%HG% clone Config\zeroconf.hg Config\config_repo
if errorlevel 1 (
  goto clean_fail
)
cd Config\config_repo
%HG% update tip
if errorlevel  1 (
  goto clean_fail
)

net start ngp_host_service
if errorlevel 1 (
REM uncomment it
REM  goto clean_fail
)

echo CLEAN OK
exit /b 0

:clean_fail
echo ********** CLEAN FAILURE **********
exit /b %errorlevel%
