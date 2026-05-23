#!/usr/bin/env python3
"""
Añade un episodio al feed RSS del podcast Daily Digest.
Uso: python add_episode.py <ruta_mp3> <titulo> <descripcion>

Ejemplo:
  python add_episode.py digest-2026-05-23.mp3 "Digest del 23 de mayo" "5 newsletters curadas"
"""
import sys
import os
import re
from datetime import datetime
from email.utils import formatdate
import xml.etree.ElementTree as ET

FEED_FILE = os.path.join(os.path.dirname(__file__), "feed.xml")
BASE_URL = "https://mariagps.github.io/daily-digest-podcast"

def get_file_size(path):
    return os.path.getsize(path)

def add_episode(mp3_path, title, description):
    mp3_name = os.path.basename(mp3_path)
    mp3_url = f"{BASE_URL}/{mp3_name}"
    mp3_size = get_file_size(mp3_path)
    pub_date = formatdate(localtime=True)

    with open(FEED_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    item = f"""
    <item>
      <title>{title}</title>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{mp3_url}" length="{mp3_size}" type="audio/mpeg"/>
      <guid>{mp3_url}</guid>
    </item>"""

    # Insertar antes del cierre de </channel>
    content = content.replace("    <!-- Los episodios se insertan aquí automáticamente -->",
                               item + "\n\n    <!-- Los episodios se insertan aquí automáticamente -->")

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Episodio añadido: {title}")
    print(f"URL: {mp3_url}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python add_episode.py <ruta_mp3> <titulo> <descripcion>")
        sys.exit(1)
    add_episode(sys.argv[1], sys.argv[2], sys.argv[3])
