@echo off
echo Установка Xenobot...
echo.

:: Копируем файлы в удобное место
if not exist "C:\Xenobot" mkdir "C:\Xenobot"
xcopy /Y /E . "C:\Xenobot\"

:: Создаем ярлык в автозагрузке
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\start.bat.lnk'); $Shortcut.TargetPath = 'C:\Xenobot\start.bat'; $Shortcut.WorkingDirectory = 'C:\Xenobot\'; $Shortcut.Save()"

echo Xenobot установлен и будет запускаться автоматически!
echo.
echo Папка с Xenobot: C:\Xenobot
echo Чтобы удалить: удали папку C:\Xenobot и ярлык из автозагрузки
pause