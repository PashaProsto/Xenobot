import json
import os
import time
import webbrowser
import subprocess
from vosk import Model, KaldiRecognizer
import pyaudio
import simpleaudio as sa
import random
from fuzzywuzzy import fuzz
import yaml
import openai
from openai import OpenAI
import datetime
from sound import Sound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fix_paths():
    """Автоматически находит правильные пути к файлам"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем существование папок
    if not os.path.exists("model_small"):
        # Пытаемся найти в разных местах
        possible_paths = [
            os.path.join(base_dir, "model_small"),
            os.path.join(os.getcwd(), "model_small"),
            "model_small"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                os.chdir(os.path.dirname(path))
                break
    
    print(f"Рабочая директория: {os.getcwd()}")

# Вызываем авто-исправление путей
fix_paths()

# Константы
ACTIVATION_WORDS = ['ксенобот', 'ксено', 'xeno', 'xenobot', 'шлюха', 'хороший мальчик', 'бот']
SOUNDS_DIR = "sounds"
VA_ALIAS = ('ксенобот',)
VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько', 'слушай')

# Загрузка команд из YAML файла
VA_CMD_LIST = yaml.safe_load(
    open('commands.yaml', 'rt', encoding='utf8'),
)

# Инициализация распознавания речи
model = Model("model_small")
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def filter_cmd(raw_voice: str):
    """Фильтрует команду от лишних слов"""
    cmd = raw_voice
    for x in VA_ALIAS:
        cmd = cmd.replace(x, "").strip()
    for x in VA_TBR:
        cmd = cmd.replace(x, "").strip()
    return cmd

def recognize_cmd(cmd: str):
    """Распознает команду используя расстояние Левенштейна"""
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc

def va_respond(voice: str):
    """Основная функция обработки голосовых команд"""
    print(f"Распознано: {voice}")

    # Фильтруем и распознаем команду
    filtered_cmd = filter_cmd(voice)
    cmd = recognize_cmd(filtered_cmd)

    print(f"Команда: {cmd}")

    if len(cmd['cmd'].strip()) <= 0:
        return False
        
    else:
        execute_command(cmd['cmd'])
        return True

def find_best_match(text, word_list, threshold=60):
    """Находит лучшее соответствие в списке слов используя расстояние Левенштейна"""
    best_match = None
    best_ratio = 0

    for word in word_list:
        ratio = fuzz.ratio(text.lower(), word.lower())
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = word

    if best_ratio >= threshold:
        return best_match, best_ratio
    return None, best_ratio

def play_sound(sound_type):
    """Воспроизведение звуков"""
    sounds = {
        'masya': ['masya.wav'],
        'ready': ['ready.wav'],
        'wait': ['wait1.wav', 'wait2.wav'],
        'success': ['success.WAV'],
        'error': ['error.wav'],
        'not_found': ['not_found.wav'],
        'lev0u': ['lev0u.wav'],
        'lev0u2': ['lev0u2.wav'],
        'stupid': ['stupid.wav'],
        'lockmean': ['lockmean.MP3'],
    }

    if sound_type in sounds:
        sound_file = random.choice(sounds[sound_type])
        sound_path = os.path.join(SOUNDS_DIR, sound_file)
        if os.path.exists(sound_path):
            wave_obj = sa.WaveObject.from_wave_file(sound_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()

def execute_command(cmd_name):
    """Выполняет команду на основе распознанного названия"""
    print(f"Выполняю команду: {cmd_name}")

    if cmd_name == 'open_browser':
        webbrowser.open('https://')
        masya_number = random.randint(1, 20)
        if masya_number == 1:
            play_sound('masya')
            print('мася привет')
        return "Открываю браузер"

    elif cmd_name == 'open_youtube':
        webbrowser.open('https://www.youtube.com')
        return "Открываю YouTube"

    elif cmd_name == 'open_vk':
        webbrowser.open('https://vk.com')
        return "Открываю ВКонтакте"

    elif cmd_name == 'shutdown':
        os.system("shutdown /s /t 5")
        return "Выключаю компьютер"

    elif cmd_name == 'open_explorer':
        subprocess.Popen('explorer')
        return "Открываю проводник"

    elif cmd_name == 'open_music':
        os.system("start spotify:")
        return "Включаю музыку"

    # elif cmd_name == 'lock_pc':
    #     os.system("rundll32.exe user32.dll,LockWorkStation")
    #     return "Блокирую компьютер"

    elif cmd_name == 'screenshot':
        subprocess.Popen(['snippingtool', '/clip'])
        return "Делаю скриншот"

    elif cmd_name == 'task_manager':
        os.system("taskmgr")
        return "Открываю диспетчер задач"

    elif cmd_name == 'open_github':
        webbrowser.open('https://github.com')
        return "Открываю GitHub"

    elif cmd_name == 'open_stackoverflow':
        webbrowser.open('https://stackoverflow.com')
        return "Открываю Stack Overflow"

    elif cmd_name == 'open_twitch':
        webbrowser.open('https://twitch.tv')
        return "Открываю Twitch"

    elif cmd_name == 'open_discord':
        os.system('start discord:')
        return "Открываю Discord"

    elif cmd_name == 'volume_up':
        Sound.volume_up() # увеличим громкость на 2 единицы
        return "Увеличиваю громкость"

    elif cmd_name == 'volume_down':
        Sound.volume_down() # уменьшим громкость на 2 единицы
        return "Уменьшаю громкость"

    elif cmd_name == 'volume_mute':
        Sound.mute() # убрали звук
        return "Выключаю звук"

    elif cmd_name == 'volume_unmute':
        Sound.volume_set(20) # установим пользовательскую громкость
        return "Включаю звук"


    return None

def listen_for_activation():
    """Слушает активационную фразу используя расстояние Левенштейна"""
    print("Ожидаю активационную фразу...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get('text', '').lower()
            print(f"Распознано: {text}")

            # Используем расстояние Левенштейна для активационных слов
            best_match, ratio = find_best_match(text, ACTIVATION_WORDS, threshold=60)

            if best_match:
                print(f"Активирован по слову: {best_match} (схожесть: {ratio}%)")
                play_sound('wait')

                # Функция от лёвы
                lev0u = random.randint(1, 100)
                if lev0u == 49:
                    play_sound('lev0u')
                    print("лёва привет")
                return True

def listen_for_command():
    """Слушает команду после активации"""
    print("Слушаю команду...")
    start_time = time.time()
    timeout = 5

    while time.time() - start_time < timeout:
        data = stream.read(4000, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command_text = result.get('text', '')

            if command_text:
                print(f"Команда: {command_text}")
                success = va_respond(command_text)

                if success:
                    play_sound('success')
                    return True
                else:
                    return False

    play_sound('error')
    print("Не дождался команды")
    return False

def main():
    print("Xenobot запущен и готов к работе!")
    play_sound('ready')

    try:
        while True:
            if listen_for_activation():
                listen_for_command()

    except KeyboardInterrupt:
        print("\nXenobot завершает работу...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()