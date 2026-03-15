from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.loan.loan import Loan


@dataclass
class MemberData:
    id: int
    username: str
    email: str
    password: str
    address: str = ""


class Member:
    MAX_ACTIVE_LOANS = 3

    def __init__(self, data: MemberData) -> None:
        self.__id: int = data.id
        self.__username: str = data.username
        self.__email: str = data.email
        self.__password: str = data.password
        self.__address: str = data.address
        self.__active_loans: list[Loan] = []

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_username(self) -> str:
        return self.__username

    def get_email(self) -> str:
        return self.__email

    def get_password(self) -> str:
        return self.__password

    def get_address(self) -> str:
        return self.__address

    def get_active_loans(self) -> list[Loan]:
        return self.__active_loans.copy()

    # Setters
    def set_username(self, username: str) -> None:
        self.__username = username

    def set_email(self, email: str) -> None:
        self.__email = email

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_address(self, address: str) -> None:
        self.__address = address

    # Verifica se il membro può prendere in prestito un libro (massimo 3 prestiti attivi)
    def can_borrow(self) -> bool:
        return len(self.__active_loans) < self.MAX_ACTIVE_LOANS

    # Aggiunge un prestito attivo al membro, se possibile
    def add_active_loan(self, loan: Loan) -> None:
        if self.can_borrow():
            self.__active_loans.append(loan)
        else:
            raise ValueError("Il membro ha già 3 prestiti attivi.")

    # Rimuove un prestito attivo dal membro, se presente
    def remove_active_loan(self, loan: Loan) -> None:
        if loan in self.__active_loans:
            self.__active_loans.remove(loan)
        else:
            raise ValueError("Il prestito non è attivo per questo membro.")

    # Rappresentazione testuale dell'oggetto Member
    def __str__(self) -> str:
        result: str = (
            f"Member(id={self.__id}, username='{self.__username}', email='{self.__email}', address='{self.__address}', active_loans={len(self.__active_loans)})"
        )
        if self.__active_loans:
            result += "\nActive Loans:\n"
            for loan in self.__active_loans:
                result += f"  - {loan}\n"
        return result
