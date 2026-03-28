"""Domain entities for library members: MemberData dataclass and
Member class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.loan.loan import Loan


@dataclass
class MemberData:
    """Data transfer object carrying the basic fields needed to build a
    Member."""

    id: int
    username: str
    email: str
    password: str
    address: str = ""


class Member:
    """Domain entity representing a library member, managing personal data
    and active loans."""

    MAX_ACTIVE_LOANS = 3

    def __init__(self, data: MemberData) -> None:
        self.__id: int = data.id
        self.__username: str = data.username
        self.__email: str = data.email
        self.__password: str = data.password
        self.__address: str = data.address
        self.__active_loans: list[Loan] = []

    def get_id(self) -> int:
        """Return the member's unique identifier."""
        return self.__id

    def get_username(self) -> str:
        """Return the member's username."""
        return self.__username

    def get_email(self) -> str:
        """Return the member's email address."""
        return self.__email

    def get_password(self) -> str:
        """Return the member's hashed password."""
        return self.__password

    def get_address(self) -> str:
        """Return the member's postal address."""
        return self.__address

    def get_active_loans(self) -> list[Loan]:
        """Return a defensive copy of the active loans list."""
        return self.__active_loans.copy()

    def set_username(self, username: str) -> None:
        """Set the member's username."""
        self.__username = username

    def set_email(self, email: str) -> None:
        """Set the member's email address."""
        self.__email = email

    def set_password(self, password: str) -> None:
        """Set the member's hashed password."""
        self.__password = password

    def set_address(self, address: str) -> None:
        """Set the member's postal address."""
        self.__address = address

    def can_borrow(self) -> bool:
        """Return True if the member has fewer than MAX_ACTIVE_LOANS
        active loans."""
        return len(self.__active_loans) < self.MAX_ACTIVE_LOANS

    def add_active_loan(self, loan: Loan) -> None:
        """Add a loan to the active list; raise ValueError if the limit is
        reached."""
        if self.can_borrow():
            self.__active_loans.append(loan)
        else:
            raise ValueError("Il membro ha già 3 prestiti attivi.")

    def remove_active_loan(self, loan: Loan) -> None:
        """Remove a loan from the active list; raise ValueError if not
        found."""
        if loan in self.__active_loans:
            self.__active_loans.remove(loan)
        else:
            raise ValueError("Il prestito non è attivo per questo membro.")

    def __str__(self) -> str:
        result: str = (
            f"Member(id={self.__id}, username='{self.__username}', "
            f"email='{self.__email}', address='{self.__address}', "
            f"active_loans={len(self.__active_loans)})"
        )
        if self.__active_loans:
            result += "\nActive Loans:\n"
            for loan in self.__active_loans:
                result += f"  - {loan}\n"
        return result
