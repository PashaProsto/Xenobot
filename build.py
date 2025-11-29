import os
import subprocess
import sys

def build_exe():
    print("Собираю Xenobot в exe...")
    
    # Устанавливаем PyInstaller если нет
    try:
        import PyInstaller
    except:
        print("Устанавливаю PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Команда сборки
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name=Xenobot',
        '--add-data=model_small;model_small',
        '--add-data=sounds;sounds',
        '--add-data=commands.yaml;.',
        'main.py'
    ]
    
    subprocess.call(cmd)
    print("Сборка завершена! EXE файл в папке dist/")

if __name__ == "__main__":
    build_exe()