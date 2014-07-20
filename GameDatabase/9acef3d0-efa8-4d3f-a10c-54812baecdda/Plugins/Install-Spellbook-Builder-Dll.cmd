@echo off
rem v1.8.0.0
cd /d %~dp0

@echo Installing the Spellbook Builder DLL for the Mage Wars on OCTGN module!
@echo.
@echo Making sure that file is unblocked 
@echo.
powershell -command unblock-file .\Octgn.MagewarsPlugin\Octgn.Magewars.dll && @echo  - It is not Blocked.....

@echo.
@echo Making sure that the folder where we want to install the plugin exists and if it doesn't we will create it...
@echo.
if exist ..\..\..\Plugins\MWPlugIn (@echo   - Folder already exists!) else (mkdir ..\..\..\Plugins\MWPlugIn & @echo   - Target folder was created!) 
@echo.

@echo Copy DLL to target folder, replacing the existing DLL if needed
@echo.
copy .\Octgn.MagewarsPlugin\Octgn.Magewars.dll ..\..\..\Plugins\MWPlugIn /y >nul && @echo   - DLL file copied to folder successfully

@echo.
if exist ..\..\..\Plugins\MWPlugIn\Octgn.Magewars.dll (@echo Done updating the Spellbookbuilder DLL for the Mage Wars on OCTGN module!) else (@echo Something bad happened!)
@echo.

pause
