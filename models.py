from datetime import datetime
from database import db

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    availability = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'availability': self.availability
        }

class Borrower(db.Model):
    __tablename__ = 'borrowers'
    
    borrower_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    membership_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'borrower_id': self.borrower_id,
            'name': self.name,
            'email': self.email,
            'membership_date': self.membership_date.isoformat()
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.borrower_id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    # Relationships for easy access
    book = db.relationship('Book', backref='transactions')
    borrower = db.relationship('Borrower', backref='transactions')

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'borrower_id': self.borrower_id,
            'borrower_name': self.borrower.name,
            'borrow_date': self.borrow_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False) # e.g., 'SystemAdmin' or Borrower Name
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user': self.user,
            'action': self.action,
            'timestamp': self.timestamp.isoformat()
        }
