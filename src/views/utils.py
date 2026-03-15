"""
Questo file `utils.py` conterrà funzioni di utilità condivise tra le diverse Viste.

Scopo principale attuale:
- Definire il decoratore `@login_required` che le views private (loan_view, wishlist_view) potranno importare.
Questo decoratore controllerà se esiste una sessione attiva ("member_id" in session) e, in caso contrario, reindirizzerà l'utente alla pagina di login.
"""
