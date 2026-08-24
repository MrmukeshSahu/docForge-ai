import os
import time
import threading
from typing import Callable

class FolderWatcher:
    def __init__(self, watch_dir: str, output_dir: str, process_callback: Callable[[str, str], None], interval_sec: float = 3.0):
        self.watch_dir = watch_dir
        self.output_dir = output_dir
        self.process_callback = process_callback
        self.interval_sec = interval_sec
        self.is_running = False
        self.processed_files = set()
        self._thread = None

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        os.makedirs(self.watch_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False

    def _watch_loop(self):
        print(f"[*] Hot-Folder Watcher active on: '{self.watch_dir}'")
        while self.is_running:
            try:
                if os.path.exists(self.watch_dir):
                    files = [f for f in os.listdir(self.watch_dir) if f.lower().endswith('.docx') and not f.startswith('~$')]
                    for fname in files:
                        full_path = os.path.join(self.watch_dir, fname)
                        if full_path not in self.processed_files:
                            self.processed_files.add(full_path)
                            out_path = os.path.join(self.output_dir, f"formatted_{fname}")
                            print(f"[*] Watcher detected new file: '{fname}'. Processing...")
                            try:
                                self.process_callback(full_path, out_path)
                            except Exception as e:
                                print(f"[!] Watcher error processing {fname}: {e}")
            except Exception as e:
                print(f"[!] Watcher loop error: {e}")

            time.sleep(self.interval_sec)
