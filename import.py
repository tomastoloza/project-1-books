import csv
from application import db, app
from models import Book

db.init_app(app)


def import_books():
    with open("books.csv") as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for isbn, title, author, year in csvreader:
            book = Book(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
            print(f'Added book. title: {title}')
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        import_books()
