from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

ARQUIVO = "editor.py"
ARQUIVO = "main.py"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(ARQUIVO):
            os.system("cls" if os.name == "nt" else "clear")
            print("Recarregando...")
            subprocess.Popen(["python", ARQUIVO])

# Inicia o observador
observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, ".", recursive=False)
observer.start()

print("Observando alterações em tempo real...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
