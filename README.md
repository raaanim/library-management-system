````markdown
# Library Management System – Istruzioni di installazione

Tutti i comandi devono essere eseguiti **all'interno dell'ambiente virtuale**. Se questo passaggio viene saltato, i pacchetti verranno installati a livello di sistema.

1. Creare un ambiente virtuale

```bash
python3 -m venv .venv
````

Attivare l'ambiente virtuale:

Linux / macOS

```bash
source .venv/bin/activate
```

Windows (PowerShell)

```powershell
.venv\Scripts\activate
```

Per uscire dall'ambiente virtuale(uguale per tutti i sistemi operativi):

```bash
deactivate
```

2. Aggiornare pip

```bash
pip install --upgrade pip
```

3. Installare le dipendenze di produzione

```bash
pip install -r requirements.txt
```

4. Installare le dipendenze di sviluppo

```bash
pip install -r requirements_dev.txt
```

5. Verificare l'installazione

```bash
pip list
```

Dopo il comando, il terminale non mostrerà più `(.venv)` all'inizio della riga, indicando che si è tornati all'ambiente Python di sistema.

Estensioni consigliate per l'IDE (Visual Studio Code):

* Python
* Pylance
* Python debugger
* Python Environments
* SQLite viewer

```
```
