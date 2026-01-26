from flask import Blueprint, request, jsonify
from database import db
from models import Book, Borrower, Transaction, AuditLog
from datetime import datetime

api = Blueprint('api', __name__)

def log_audit(user, action):
    log = AuditLog(user=user, action=action)
    db.session.add(log)
    db.session.commit()

# --- BOOK ROUTES ---
@api.route('/books', methods=['GET'])
def get_books():
    query = request.args.get('q')
    if query:
        search = f"%{query}%"
        books = Book.query.filter(
            (Book.title.like(search)) | 
            (Book.author.like(search)) | 
            (Book.category.like(search))
        ).all()
    else:
        books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@api.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        category=data.get('category')
    )
    db.session.add(new_book)
    db.session.commit()
    log_audit('System/Admin', f"Added book: {new_book.title}")
    return jsonify(new_book.to_dict()), 201

# --- BORROWER ROUTES ---
@api.route('/borrowers', methods=['GET'])
def get_borrowers():
    borrowers = Borrower.query.all()
    return jsonify([b.to_dict() for b in borrowers])

@api.route('/borrowers', methods=['POST'])
def add_borrower():
    data = request.json
    new_borrower = Borrower(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_borrower)
    db.session.commit()
    log_audit('System/Admin', f"Registered borrower: {new_borrower.name}")
    return jsonify(new_borrower.to_dict()), 201

# --- TRANSACTION ROUTES ---
@api.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    book_id = data['book_id']
    borrower_id = data['borrower_id']
    
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    if not book.availability:
        return jsonify({'error': 'Book is not available'}), 400
        
    book.availability = False
    transaction = Transaction(book_id=book_id, borrower_id=borrower_id)
    db.session.add(transaction)
    db.session.commit()
    
    log_audit(f"Borrower {borrower_id}", f"Borrowed book {book_id}: {book.title}")
    return jsonify(transaction.to_dict()), 200

@api.route('/return', methods=['POST'])
def return_book():
    data = request.json
    book_id = data['book_id']
    borrower_id = data['borrower_id'] # Optional validation
    
    # Find active transaction for this book
    transaction = Transaction.query.filter_by(book_id=book_id, return_date=None).first()
    if not transaction:
        return jsonify({'error': 'Active transaction not found for this book'}), 404
        
    transaction.return_date = datetime.utcnow()
    book = db.session.get(Book, book_id)
    book.availability = True
    
    db.session.commit()
    log_audit(f"Borrower {transaction.borrower_id}", f"Returned book {book_id}: {book.title}")
    return jsonify(transaction.to_dict()), 200

@api.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.borrow_date.desc()).all()
    return jsonify([t.to_dict() for t in transactions])

# --- AUDIT LOG ROUTES ---
@api.route('/audit', methods=['GET'])
def get_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return jsonify([log.to_dict() for log in logs])
