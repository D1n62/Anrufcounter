try:
    import sys
    import time
    import os
    import json
    from threading import Thread
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import urllib.parse
    import threading
    from datetime import datetime
    import csv
except Exception as E:
    print(f"(FATAL) Fehler beim laden der Bibliotheken, Fehlermeldung: {E}")
    time.sleep(1)
    sys.exit()



class Starface_Modul:
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            parsed_path = urllib.parse.urlparse(self.path)
            print("[- Starface-Modul - HTTP - INFO -] Angeforderter Pfad:", parsed_path.path)
            besserer_pfad = parsed_path.path.replace("/", "")
            print("[- Starface-Modul - HTTP - INFO -] Nummer die angerufen hat/wurde: ", besserer_pfad)
            try:
                with open("tmp.txt", "w+") as tmp:
                    tmp.write(besserer_pfad)
            except Exception as e:
                print(f"Fehler beim Schreiben in tmp.txt: {e}")
            self.wfile.write(b"<html><head><title>Starface Modul Anrufzaehler</title></head>")
            self.wfile.write(b"<meta name='viewport' content='width=device-width, initial-scale=1.0'><style>body {margin: 0;padding: 0;background-color: #293136;}.content {padding: 20px;color: white;font-family: Arial, sans-serif;}</style></head><body><div class='content'></div></body></html>")
            
    class WebServerThread(threading.Thread):
        def run(self):
            port = 24757
            server_address = ('', port)
            Starface_Modul.Programm_läuft = True
            try:
                httpd = HTTPServer(server_address, Starface_Modul.RequestHandler)
            except Exception as exhttp:
                print(f"[- Starface-Modul - HTTP - ERR -] {exhttp}")
                return
            try:
                while Starface_Modul.Programm_läuft == True:
                    print(f'[- Starface-Modul - HTTP - INFO -] Ich horche mal auf Port {port}...') 
                    httpd.handle_request()
                    if Starface_Modul.Programm_läuft == False: # wenn diese funktion hier jemals funktionieren würde, könnten hier auch Fehler erscheinen.
                        httpd.shutdown()
                        httpd.server_close()
                        print(f'[- Starface-Modul - HTTP - INFO -] Server auf Port {port} gestoppt.')
                        sys.exit()
            except KeyboardInterrupt:
                httpd.server_close()
                httpd.shutdown()
                print(f'[- Starface-Modul - HTTP - INFO -] Server auf Port {port} gestoppt.')

##### INIT START
    def __init__(self, master):
        self.master = master
        self.Programm_läuft = True
        self.Programm_Name = "Starface Modul"
        self.Version = 0
        Dings = r"""
#            _ .-') _             .-') _                   
#           ( (  OO) )           ( OO ) )                  
#           \     .'_  .---.,--./ ,--,'   ,--.   .-----.  
#           ,`'--..._)/_   ||   \ |  |\  /  .'  / ,-.   \ 
#           |  |  \  ' |   ||    \|  | ).  / -. '-'  |  | 
#           |  |   ' | |   ||  .     |/ | .-.  '   .'  /  
#           |  |   / : |   ||  |\    |  ' \  |  |.'  /__  
#           |  '--'  / |   ||  | \   |  \  `'  /|       | 
#           `-------'  `---'`--'  `--'   `----' `-------'  <-2024->
"""
        print(Dings)
        self.Benutzerordner = os.path.expanduser('~')
    ## Die Threads einstellen
        self.thread_webserver = Starface_Modul.WebServerThread()
        self.thread_webserver.daemon = False
        self.Db_Ordner_pfad = os.path.join(self.Benutzerordner, 'Starface Moul', 'Db')
        self.Json_pfad = os.path.join(self.Db_Ordner_pfad, 'Db.json')


        self.thread_webserver.start()
        self.Kunde_ruft_an()


##### INIT ENDE
    def Kunde_ruft_an(self):
        print("Thread gestartet: Kunde_ruft_an (def)")
        while self.Programm_läuft == True:
            try:
                with open("tmp.txt", "r") as tmp_ld:
                    gel_tmp = tmp_ld.read()
                    self.Anruf_Telefonnummer = gel_tmp
                    print1 = "-abgefangene Telefonummer: " + self.Anruf_Telefonnummer + "-"
                    print(print1)
                    tmp_ld.close()
                    os.remove("tmp.txt")
                '''self.Gesperrte_Nummer = False
                try:
                    print("else f")
                    with open(self.Json_pfad, 'r', encoding='utf-8') as datei:
                        daten = json.load(datei)
                    try:
                        print("lade die Blacklist...")
                        with open(self.Blacklist_pfad, "r", encoding='utf-8') as b_datei:
                            daten_blacklist = json.load(b_datei)
                    except Exception as E:
                        self.Ereignislog_insert(nachricht_f_e="-Konnte die Blacklist nicht laden-")
                        daten_blacklist = ""
                    for Gesperrte_kontakt in daten_blacklist.get("Kontakte", []):
                        print(f"ich durchsuche die Blacklist... mit {Gesperrte_kontakt.get("Telefonnummer_jsn_gesperrt")}")
                        if str(Gesperrte_kontakt.get("Telefonnummer_jsn_gesperrt")) == str(self.Anruf_Telefonnummer):
                            print("if f")
                            self.Anruf_Telefonnummer = None
                            self.Gesperrte_Nummer = True
                        else:
                            print(f"offensichtlicher weise war {str(Gesperrte_kontakt.get("Telefonnummer_jsn_gesperrt"))} nicht das selbe wie {str(self.Anruf_Telefonnummer)}... oder so ähnlich.")
                        #else:
                    if self.Gesperrte_Nummer == False:
                        print("else f 1")
                        for kontakt in daten.get("Kontakte", []):
                            if kontakt.get("Telefonnummer_jsn") == self.Anruf_Telefonnummer: # WENN ES IN DER KTK GEFUNDEN WURDE
                                print("if f 1")
                                self.Name_gel_für_e = kontakt.get("Name")
                                self.Anruf_Telefonnummer = None
                                # hier kommen jetzt die Ausnahmen für spezielle Kontakte hin. !!WENN SIE GEFUNDEN WUDEN!!
                                    
                                    # hier enden die speziellen Ausnahmen für spezielle Kontakte.
                except Exception as ExcK1:
                        print(f"Fehler beim Durchsuchen der JSON DB nach dem Kontakt. Fehlercode: {ExcK1}")'''

                with open("Zahl.txt", "r") as Zahl_Stand_gel:
                    Zahl_Stand = int(Zahl_Stand_gel.read())
                    print(f"Zahl_Stand liegt vor der erhöhung bei: {Zahl_Stand}.")
                    Zahl_Stand = Zahl_Stand + 1
                    print(f"Zahl_Stand liegt nach der erhöhung bei: {Zahl_Stand}.")
                with open("Zahl.txt", "w") as z_schreiben:
                    z_schreiben.write(str(Zahl_Stand))
                    print(f"Zahl_Stand wurde auf {Zahl_Stand} aktualisiert.")

                def update_csv(date, Tel_Nummer):
                    file_exists = None
                    # Dateinamen auf Basis des aktuellen Monats und Jahres
                    file_name = f"{datetime.now().strftime('%Y_%m')}_Anruf_Statistik.csv"

                    # Prüfen, ob die Datei existiert
                    file_exists = os.path.isfile(file_name)

                    if file_exists:
                        # Datei existiert, Daten laden und aktualisieren
                        with open(file_name, 'r', newline='') as csvfile:
                            reader = csv.reader(csvfile)
                            data = list(reader)
                    else:
                        # Datei existiert nicht, neue Datenstruktur anlegen
                        data = [["Datum", "Telefonnummer", "Anzahl"]]

                    # Prüfen, ob die Telefonnummer bereits in der Datei ist
                    found = False
                    for row in data:
                        if row[1] == Tel_Nummer:
                            row[2] = str(int(row[2]) + 1)
                            found = True
                            break

                    # Wenn die Telefonnummer nicht gefunden wurde, neue Zeile hinzufügen
                    if not found:
                        data.append([date, Tel_Nummer, "1"])

                    # Daten zurück in die CSV-Datei schreiben
                    with open(file_name, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(data)
                        
                    print(f"Updated {file_name} with {Tel_Nummer} for date {date}")

                    # Beispiel für die Nutzung
                date = datetime.now().strftime("%Y-%m-%d")
                Tel_Nummer = self.Anruf_Telefonnummer
                update_csv(date, Tel_Nummer)

            except Exception as s:
                print(s)
            time.sleep(1)
        print("Thread beendet: Kunde_ruft_an (def")
        

instance = Starface_Modul("Master")