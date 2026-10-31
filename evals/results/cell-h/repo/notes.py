import json
from pathlib import Path
def load_notes(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
def save_notes(path, notes):
    Path(path).write_text(json.dumps(notes, ensure_ascii=False), encoding='utf-8')
