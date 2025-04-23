# foltagger
## Install

First you need to run https://github.com/danbooru/autotagger

### With UV
`uv sync`
### With PIP
1. Create virtual env: `python -m venv .venv
2. Activate venv with `source .venv/bin/activate` on linux or `.venv/Scripts/activate` on Windows
3. Run `pip install aiohttp`
## Usage
### With UV
`uv run main.py [folder]`
### With PIP
`python main.py [folder]`

### Configuration
Set `AUTOTAGGER_URL` to use a different autotagger url.
