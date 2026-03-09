from dataclasses import dataclass
from datetime import date

from src.models.book import Book
from src.models.member import Member  # type: ignore


@dataclass
class Loan:
    daily_fine = 1.0
    id: int
    member: Member
    book: Book
    loan_date: date
    due_date: date
    return_date: date | None = None
    fine: float = 0.0

    def is_overdue(self) -> bool:
        if self.return_date is None:
            return date.today() > self.due_date
        return self.return_date > self.due_date

    def calculate_fine(self) -> float:
        if not self.is_overdue():
            return 0.0
        if self.return_date is None:
            end_date = date.today()
        else:
            end_date = self.return_date
        overdue_days = (end_date - self.due_date).days
        return overdue_days * self.daily_fine

    def close_loan(self, return_date: date) -> None:
        self.return_date = return_date
        self.calculate_fine()

    def __str__(self) -> str:
        return (
            f"Loan(id={self.id}, "
            f"member={self.member.username}, "
            f"book={self.book}, "
            f"loan_date={self.loan_date}, "
            f"due_date={self.due_date}, "
            f"return_date={self.return_date}, "
            f"fine={self.fine})"
        )
