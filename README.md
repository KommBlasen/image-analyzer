# Image Analyzer

Ein kleines Python-Programm, das ein Bild mit OpenAI Vision analysiert und eine ausführliche deutsche Beschreibung liefert.

## Voraussetzungen

- Python 3.10+
- OpenAI API-Key

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API-Key setzen

```bash
export OPENAI_API_KEY="dein_api_key"
```

## Benutzung

```bash
python image_describer.py /pfad/zum/bild.jpg
```

## Beispiel

```bash
python image_describer.py example.jpg
```

## Hinweis

Das Programm akzeptiert derzeit JPG, JPEG, PNG und WEBP und beschränkt Bilder auf 20 MB.

