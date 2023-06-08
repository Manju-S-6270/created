chcp 65001
echo off
cls

openfiles>nul 2>&1 || (
    powershell -c start "%~f0" -verb runas
    exit /b
)



echo.
echo PCスキャン スタート
echo.
echo.
echo スキャンメニュー
echo ***********************
echo 1. sfc
echo 2. dism
echo 3. All(sfc,dism)
echo ***********************
echo.
set /p Scan="数字で選択してください(1-3): "

if %Scan%==1 (
  sfc /scannow
  echo 正常に終了しました。
) else if %Scan%==2 (
  Dism.exe /Online /Cleanup-Image /Restorehealth
  echo 正常に終了しました。
) else if %Scan%==3 (
  sfc /scannow
  Dism.exe /Online /Cleanup-Image /Restorehealth
) else if (
  echo 1-3以外が入力されました。
  echo やり直してください
  timeout 10
  exit
) timeout 20
cls
echo.
echo PCスキャン スキャン終了
echo.
echo.
echo Windowsシステムのスキャンを終了しました。ログファイルを自動で起動します。
echo.
echo 保存場所:　%~dp0log¥%date:~0,4%-%date:~5,2%-%date:~8,2%.log
echo.
echo.
if %Scan%==1 (
  echo 注意: ログファイルが文字化けしている可能性があります
) else if %Scan%==3 (
  echo 注意: ログファイルが文字化けしている可能性があります
)
echo. 
echo.
timeout 10
"%~dp0/log/%date:~0,4%-%date:~5,2%-%date:~8,2%.log"
exit
