;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------

; The name of the installer
  Name "Mage Wars for OCTGN DeckBuilder Plugin Install v1.9.0.0"

; The file to write
  OutFile "OCTGN-SBB-for-MageWars.exe"

; Request application privileges for Windows Vista/7/8
  RequestExecutionLevel user

  !define MUI_ICON "Deck.ico"

;--------------------------------
;Interface Settings

;--------------------------------
;Pages

  !define MUI_TEXT_WELCOME_INFO_TEXT "This wizard will install the Mage Wars for OCTGN DeckBuilder Plugin.$\n$\nClick the Install button to start the installation."
  !define MUI_PAGE_CUSTOMFUNCTION_SHOW WelcomeShowCallback
  
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------


Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  ; This is the install location for the dll 
  SetOutPath $DOCUMENTS\Octgn\Plugins\MWPlugIn
  
  ; Put file there
  ; Where do I find the source dll to compile into the EXE
  File ..\..\GameDatabase\9acef3d0-efa8-4d3f-a10c-54812baecdda\Plugins\Octgn.MagewarsPlugin\Octgn.Magewars.dll
  File ..\..\GameDatabase\9acef3d0-efa8-4d3f-a10c-54812baecdda\Plugins\Octgn.MagewarsPlugin\OCTGNDeckConverter.dll
  
SectionEnd ; end the section


Function WelcomeShowCallback
  SendMessage $mui.WelcomePage.Text ${WM_SETTEXT} 0 "STR:$(MUI_TEXT_WELCOME_INFO_TEXT)"
FunctionEnd
