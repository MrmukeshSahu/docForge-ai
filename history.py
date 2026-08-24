import json
import os
import time
from typing import List, Dict, Any

class HistoryManager:
    def __init__(self, history_file: str = None):
        if history_file is None:
            history_file = os.path.join(os.path.dirname(__file__), "history_log.json")
        self.history_file = history_file

    def get_history(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def add_entry(self, input_file: str, output_file: str, elapsed_sec: float, elements_count: int, preset_used: str, status: str = "Success"):
        history = self.get_history()
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "input_file": input_file,
            "output_file": output_file,
            "elapsed_sec": round(elapsed_sec, 2),
            "elements_count": elements_count,
            "preset_used": preset_used,
            "status": status
        }
        history.insert(0, entry) # Most recent first
        # Keep top 100 entries
        history = history[:100]
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            print(f"[!] History log error: {e}")
