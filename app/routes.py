from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request


# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description
# books = [
#     Book(1, "Untamed", "A fantasy novel set in an imaginary world."),
#     Book(2, "Winnie the Pooh", "A fantasy novel set in an imaginary world."),
#     Book(3, "Pout Pout Fish", "A fantasy novel set in an imaginary world.")
# ] 
    
books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)

    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        return make_response(
            f"Book {new_book.title} created", 201
            )


@books_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_single_book(id):
    book = Book.query.get(id)
    if book is None:
        return make_response("", 404)
    if request.method == "GET":
        # for book in books:
        #     if book.id == int(id):
        return jsonify({
            "id": book.id,
            "title": book.title,
            "description": book.description
            })
    elif request.method == "PUT":
        form_data = request.get_json()
        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()
        return  make_response(
            f"Book {book.id} sucessfully updated"
            )
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")

