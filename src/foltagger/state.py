import json
from pathlib import Path

State = dict[str, list[str]]
statefile = Path("state.json")


def load_state() -> State:
    if not statefile.exists():
        return {}
    return json.loads(statefile.read_text())


GLOBAL_STATES = load_state()


def save_state(name: str, tags: list[str]):
    global GLOBAL_STATES
    GLOBAL_STATES[name] = tags
    statefile.write_text(json.dumps(GLOBAL_STATES))


def get_state_tags(name: str) -> list[str] | None:
    global GLOBAL_STATES
    return GLOBAL_STATES.get(name)
