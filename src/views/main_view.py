"""
Questo file `main_view.py` conterrà le rotte pubbliche principali dell'applicazione.

Scopo:
- Gestire la Homepage (rotta `/`), caricando libri casuali dal DB locale tramite CatalogueService.
- Gestire la pagina di Ricerca e i suoi risultati interrogando OpenLibrary tramite Reader.
- Gestire la visualizzazione dei dettagli di un singolo libro o edizione (pescando i dati online tramite Reader).

Non conterrà logica di business pura, ma si occuperà solo di orchestrare le chiamate ai servizi e renderizzare i template HTML pubblici.
"""
