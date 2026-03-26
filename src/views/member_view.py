"""
Questo file `member_view.py` conterrà le rotte dedicate all'autenticazione e gestione dell'identità dell'utente.

Scopo:
- Gestire la registrazione di nuovi utenti (rotta di GET per il form HTML e rotta POST per il salvataggio sul db).
- Gestire il Login, verificando le credenziali e impostando la sessione Flask (session["member_id"]).
- Gestire il Logout pulendo i dati di sessione.

In queste rotte i costrutti usati saranno essenzialmente `MemberModel` per controllare o salvare i dati sul database locale e `werkzeug.security` per la gestione sicura delle password.
"""
