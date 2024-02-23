from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = '965ac1256822a7b537cad696f9e28616265575b638946db526d9ce2667fb5b59'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libmanage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=1)
    transactions = relationship("Transaction", back_populates="book")


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    debt = db.Column(db.Float, default=0.0)
    pending_amount = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    rent_fee = db.Column(db.Float, default=0.0)  # Total rent fee charged at return
    daily_rent_fee = db.Column(db.Float, default=10.0)  #  this line for daily rent fee
    book = relationship("Book", back_populates="transactions")



# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        # Handle book creation
        title = request.form.get('title')
        author = request.form.get('author')
        stock = request.form.get('stock', type=int)
        if title and author and stock is not None:
            new_book = Book(title=title, author=author, stock=stock)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
        else:
            flash('Missing information. Please make sure all fields are filled out.', 'danger')
        return redirect(url_for('books'))

    # Handle book search and display
    search_query = request.args.get('search', '')  # Get the search query from the URL parameters
    if search_query:
        # Filter books based on the search query
        books = Book.query.filter((Book.title.contains(search_query)) | (Book.author.contains(search_query))).all()
    else:
        # If there is no search query, display all books
        books = Book.query.all()

    return render_template('books.html', books=books, search_query=search_query)

# route for adding a book to accept both GET and POST methods
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        stock = request.form.get('stock', type=int)

        if title and author and stock is not None:
            new_book = Book(title=title, author=author, stock=stock)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('books'))
        else:
            flash('Missing information. Please make sure all fields are filled out.', 'danger')

    return render_template('add_book.html')  # Render the add_book.html template for GET requests


@app.route('/books/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.stock = request.form['stock']
        db.session.commit()
        flash('Book updated successfully', 'success')
        return redirect(url_for('books'))
    return render_template('update_book.html', book=book)


@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully', 'success')
    return redirect(url_for('books'))

@app.route('/issue-selected-books', methods=['POST'])
def issue_selected_books():
    book_ids = request.form.getlist('book_ids')
    if book_ids:
        # Redirect to the issue_book route with selected book IDs as URL parameters
        return redirect(url_for('issue_book', book_ids=','.join(book_ids)))
    else:
        flash('No books selected.', 'danger')
        return redirect(url_for('issue_book'))
    
@app.route('/delete-all-books', methods=['POST'])
def delete_all_books():
    try:
        # Delete all book records
        Book.query.delete()
        db.session.commit()
        flash('All books have been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting books: {}'.format(e), 'danger')
    
    return redirect(url_for('books'))

@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        name = request.form['name']
        new_member = Member(name=name)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('members'))
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)

@app.route('/add-member', methods=['POST'])
def add_member():
    name = request.form.get('name')
    if not name:
        flash('Member name is required.', 'error')
        return redirect(url_for('members'))
    
    new_member = Member(name=name)
    db.session.add(new_member)
    try:
        db.session.commit()
        flash('New member added successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding member: {e}', 'error')

    return redirect(url_for('members'))  # Redirect to the members list page after adding the member


@app.route('/members/update/<int:member_id>', methods=['GET', 'POST'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    if request.method == 'POST':
        member.name = request.form['name']
        db.session.commit()
        flash('Member updated successfully', 'success')
        return redirect(url_for('members'))
    return render_template('update_member.html', member=member)


@app.route('/members/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully', 'success')  # Set flash message after successful deletion
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting member: {e}', 'error')  # Set error flash message if deletion fails
    return redirect(url_for('members', _anchor='members_flash'))



@app.route('/search-members', methods=['GET'])
def search_members():
    search_query = request.args.get('search', '').lower()
    filtered_members = Member.query.filter(Member.name.ilike(f'%{search_query}%')).all()
    return render_template('members.html', members=filtered_members, search_query=search_query)

@app.route('/delete-all-members', methods=['POST'])
def delete_all_members():
    try:
        # Delete all member records
        Member.query.delete()
        db.session.commit()
        flash('All members have been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting members: {}'.format(e), 'danger')
    
    return redirect(url_for('members'))


@app.route('/import-books', methods=['GET', 'POST'])
def import_books():
    if request.method == 'POST':
        title = request.form.get('title', '')
        authors = request.form.get('authors', '')
        isbn = request.form.get('isbn', '')
        publisher = request.form.get('publisher', '')
        page = request.form.get('page', 1, type=int)
        number_of_books = request.form.get('number_of_books', 20, type=int)

        books_imported = 0
        while books_imported < number_of_books:
            response = requests.get(f"https://frappe.io/api/method/frappe-library?page={page}&title={title}&authors={authors}&isbn={isbn}&publisher={publisher}")
            if response.status_code == 200:
                data = response.json()
                for book in data['message']:
                    if books_imported >= number_of_books:
                        break
                    # Create and insert book record
                    new_book = Book(title=book['title'], author=book['authors'], stock=1)  # Assuming stock=1 for imported books
                    db.session.add(new_book)
                    books_imported += 1
                db.session.commit()
                page += 1
            else:
                flash('Failed to import books from Frappe API', 'danger')
                break

        flash(f'Successfully imported {books_imported} books', 'success')
        return redirect(url_for('import_books'))

    return render_template('import_books.html')  



@app.route('/issue-book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        member_id = request.form.get('member_id')
        daily_rent_fee = float(request.form.get('daily_rent_fee', 10.0))  # Get daily rent fee from form
        #to get issue_date from the form
        issue_date_str = request.form.get('issue_date')
        issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d') if issue_date_str else datetime.utcnow()

        
        book = Book.query.get(book_id)
        if book and book.stock > 0:
            transaction = Transaction(member_id=member_id, book_id=book_id, daily_rent_fee=daily_rent_fee,issue_date=issue_date)
            book.stock -= 1  # Decrease the book stock
            # Calculate and set the initial rent fee
            transaction.rent_fee = 0.0
            db.session.add(transaction)
            db.session.commit()
            flash('Book issued successfully with a daily rent fee of Rs.{}'.format(daily_rent_fee), 'success')
        else:
            flash('Book is out of stock', 'danger')
        return redirect(url_for('issue_book'))

    books = Book.query.all()
    members = Member.query.all()
    issue_date = datetime.utcnow()

    return render_template('issue_book.html', books=books, members=members,issue_date=issue_date)

@app.route('/return-book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        transaction_id = request.form.get('transaction_id')
        if not transaction_id:
            flash('No transaction ID provided', 'danger')
            return redirect(url_for('return_book'))

        transaction = Transaction.query.get(transaction_id)
        if transaction and not transaction.return_date:
            try:
                transaction.return_date = datetime.utcnow()
                days_issued = (transaction.return_date - transaction.issue_date).days
                transaction.rent_fee = days_issued * transaction.daily_rent_fee
                db.session.commit()
                flash('Book returned successfully. Total rent fee: Rs.{}'.format(transaction.rent_fee), 'success')
            except Exception as e:
                current_app.logger.error(f'Error when returning book: {e}')
                db.session.rollback()
                flash('An error occurred while returning the book', 'danger')
        else:
            flash('Invalid transaction or book already returned', 'warning')

    transactions = db.session.query(Transaction, Book.title, Member.name)\
        .join(Book, Transaction.book_id == Book.id)\
        .join(Member, Transaction.member_id == Member.id)\
        .filter(Transaction.return_date.is_(None)).all()
    return render_template('return_book.html', transactions=transactions)



@app.route('/delete-all-transactions', methods=['POST'])
def delete_all_transactions():
    try:
        # Delete all transaction records
        Transaction.query.delete()
        db.session.commit()
        flash('All transactions have been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting transactions: {}'.format(e), 'danger')
    
    return redirect(url_for('transactions'))



import logging
@app.route('/transactions')
def transactions():
    try:
        transactions_data = []

        # Retrieve all transactions sorted by issue_date in descending order
        all_transactions = Transaction.query.order_by(Transaction.issue_date.desc()).all()

        # Group transactions by issue date
        transactions_by_date = {}
        for transaction in all_transactions:
            issue_date_str = transaction.issue_date.strftime('%Y-%m-%d')
            if issue_date_str not in transactions_by_date:
                transactions_by_date[issue_date_str] = []
            transactions_by_date[issue_date_str].append(transaction)

        # Sort transactions within each date by transaction ID in ascending order
        for issue_date_str, transactions in transactions_by_date.items():
            sorted_transactions = sorted(transactions, key=lambda x: x.id)
            for transaction in sorted_transactions:
                book = Book.query.get(transaction.book_id)
                member = Member.query.get(transaction.member_id)

                if book:
                    book_title = book.title
                else:
                    book_title = "Book Deleted"

                if member:
                    member_name = member.name
                else:
                    member_name = "Member Deleted"

                if not transaction.return_date:
                    days = (datetime.utcnow() - transaction.issue_date).days
                    daily_rent_fee = transaction.daily_rent_fee if transaction.daily_rent_fee is not None else 10.0
                    pending_amount = days * daily_rent_fee
                else:
                    pending_amount = None

                rent_fee = transaction.rent_fee if transaction.return_date else None

                transactions_data.append({
                    'transaction_id': transaction.id,
                    'book_title': book_title,
                    'member_name': member_name,
                    'issue_date': issue_date_str,
                    'return_date': transaction.return_date.strftime('%Y-%m-%d') if transaction.return_date else 'Not Returned',
                    'rent_fee': rent_fee if rent_fee else 'N/A',
                    'pending_amount': pending_amount if pending_amount else 'N/A'
                })

        return render_template('transactions.html', transactions=transactions_data)
    except Exception as e:
        logging.error(f"Error in /transactions route: {e}")
        flash('An error occurred while processing transactions.', 'danger')
        return redirect(url_for('index'))




@app.route('/delete-selected-transactions', methods=['POST'])
def delete_selected_transactions():
    try:
        data = request.get_json()  # Get JSON data from the request
        transaction_ids = data.get('transactionIds')  # Access transactionIds from the JSON data
        if not transaction_ids:
            raise ValueError('No transaction IDs provided')

        # Delete selected transactions by their IDs
        for transaction_id in transaction_ids:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                db.session.delete(transaction)

        db.session.commit()  # Commit the changes to the database
        flash('Selected transactions have been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an error
        flash('An error occurred while deleting transactions: {}'.format(e), 'danger')

    return redirect(url_for('transactions'))  # Redirect to the transactions page


if __name__ == '__main__':
    with app.app_context():  # Pushes an application context manually
        db.create_all()  
    app.run(debug=True)
