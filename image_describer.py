from __future__ import annotations

import base64
import io
import os
import sys
from pathlib import Path

from openai import OpenAI
from PIL import Image, UnidentifiedImageError

MAX_BYTES = 20 * 1024 * 1024


def to_png_data_url(path: str | os.PathLike[str]) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

    try:
        with Image.open(file_path) as img:
            img = img.convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            data = buffer.getvalue()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError(f"Bild konnte nicht gelesen werden: {file_path}") from exc

    if len(data) > MAX_BYTES:
        raise ValueError("Bild ist zu groß. Maximal 20 MB erlaubt.")

    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def describe_image(path: str | os.PathLike[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY ist nicht gesetzt.\n"
            "Bitte vorher ausführen: export OPENAI_API_KEY='dein_api_key'"
        )

    client = OpenAI(api_key=api_key)
    image_url = to_png_data_url(path)

    prompt = """
    Du bist ein sehr genauer Bildanalysator auf Deutsch.

    Beschreibe das Bild extrem detailliert, präzise und verständlich.

    Achte auf:
    1. Hauptmotiv und zentrale Elemente
    2. Personen, Tiere, Objekte und ihre Positionen
    3. Farben, Licht, Schatten, Kontrast, Sättigung
    4. Perspektive, Komposition, räumliche Anordnung, Bildaufbau
    5. Stimmung, Atmosphäre, Emotionen, mögliche Symbolik
    6. Kontext und mögliche Interpretation
    7. Text im Bild, falls vorhanden, möglichst genau wiedergeben
    8. Bildqualität, Schärfe, Farbwirkung, Stimmung und visuellen Stil

    Bitte formatiere die Antwort in klaren Abschnitten:
    - Kurzbeschreibung
    - Hauptmotiv und Details
    - Farben und Licht
    - Komposition und Perspektive
    - Stimmung und Interpretation
    - Zusammenfassung

    Antworte auf Deutsch, ausführlich, aber klar strukturiert und nicht übermäßig verwirrend.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Verwendung: python image_describer.py bild.jpg")
        sys.exit(1)

    try:
        print(describe_image(sys.argv[1]))
    except Exception as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        sys.exit(1)
