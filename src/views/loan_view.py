"""
Questo file `loan_view.py` conterrà le rotte per la gestione dei prestiti (Area Privata).

Scopo:
- Mostrare la lista dei prestiti (attivi e passati) dell'utente loggato.
- Gestire l'azione di "Prendi in prestito" (rotta POST): verificherà tramite CatalogueService se il libro va salvato in locale, istanzierà la classe pura `Member` per controllare `can_borrow()` e creerà il Loan associato.
- Gestire l'azione di "Restituzione" (rotta POST): inietterà la logica della classe pura `Loan` per calcolare eventuali multe (`calculate_fine()`) e chiudere il prestito nel db.

Tutte queste rotte saranno protette dal decoratore `@login_required`.
"""
