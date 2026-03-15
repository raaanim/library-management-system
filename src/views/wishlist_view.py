"""
Questo file `wishlist_view.py` conterrà le rotte per la gestione dei carrelli/desideri (Area Privata).

Scopo:
- Mostrare la lista dei libri desiderati dall'utente loggato.
- Gestire l'aggiunta di un libro desiderato (rotta POST): si affiderà al CatalogueService per salvare il libro nel DB (se non c'è già) e aggiungerà la relazione alla `wishlist` dell'utente.
- Gestire la rimozione (rotta POST): per togliere la relazione tra il libro e la wishlist dell'utente.

Tutte queste rotte saranno protette dal decoratore `@login_required`.
"""
