# Anrufcounter
 Zählt die Anrufe, die von einer Starface TK-Anlage empfangen werden
 - Kompatibel mit jedem Starface UCC Client der Browser URIs unterstützt.
 - Kompatibel mit Windows und MacOS

## Installation
- Das Paket urllib3 von Pypi installieren (pip install urllib3)
- Im Starface UCC Client: Unter Einstellungen -> Browser / Aktion URLs: Aktion URL: http://localhost:24757/$(callerId) und als Standard URL http://localhost:24757/
- Das Python script starten, fertsch

## Vorraussetzungen
- Python 3.12.
- Pip
- Unter Windows Adminrechte / Python benötigt Zugriff auf Webseiten hosting unter Localhost
