try:
    import sys
    import time
    import os
    import json
    from threading import Thread
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import urllib.parse
    import threading
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
        self.Thread_Kunderuftan = threading.Timer(1, self.Kunde_ruft_an)
        self.thread_webserver = Starface_Modul.WebServerThread()
        self.thread_webserver.daemon = False
        self.thread_webserver.start()

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
                    with open("Zahl.txt", "r") as Zahl_Stand_gel:
                        Zahl_Stand = Zahl_Stand_gel.read()
                        print(f"Zahl_Stand liegt vor der erhöhung bei: {Zahl_Stand}.")
                        Zahl_Stand = int(Zahl_Stand) + 1
                        print(f"Zahl_Stand liegt nach der erhöhung bei: {Zahl_Stand}.")
                    with open("Zahl.txt", "w+") as z_schreiben:
                        z_schreiben(Zahl_Stand)
                        print(f"Zahl_Stand wurde auf {Zahl_Stand} aktualisiert.")

                except Exception:
                    pass
                time.sleep(1)
            print("Thread beendet: Kunde_ruft_an (def")

instance = Starface_Modul("Master")