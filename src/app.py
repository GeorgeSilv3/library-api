from flask import Flask, request, jsonify
from models.book import Book

app = Flask(__name__)

db_file = "src/db/books.csv"
books = []

def load_books():
    global last_id
    try:
        with open(db_file, "r") as file:
            for line in file.readlines():
                book = line.split(";")
                book = Book(id=int(book[0]), name=book[1], author=book[2], edition=book[3].replace("\n",""))
                books.append(book)
            
        last_id = verify_last_id()
    except FileNotFoundError:
        print("File Not Found!")
        return -1
    except ValueError:
        print("Error trying convert to integer")
        return -1
    except Exception:
        print("Something Was Wrong.")
        return -1


def verify_last_id():
    last_book = books[-1]
    return last_book.get_id()


@app.route("/books", methods=["POST"])
def add_book():
    global last_id
    book_id_controller = last_id+1
    if book_id_controller != 0:
        data = request.get_json()
        book = Book(id=book_id_controller, name=data.get("name"), author=data.get("author"), edition=data.get("edition", None))
        
        last_id += 1

        books.append(book)

        save_books_db()

        return jsonify({"message": "Cadastrado com sucesso", "id": book.get_id()})
    else:
        return jsonify(db_bad_message()), 500
    

@app.route("/books", methods=["GET"])
def get_books():
    list_all_books = [book.to_dict() for book in books]
    print(list_all_books)
    return jsonify({"books": list_all_books, "books_quantity": len(books)})


@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = search_book(id)
    print(book)
    if book != -1:
        return jsonify(book.to_dict())
    return jsonify(not_found_message()), 404


@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.get_json()
    book = search_book(id)
    if book != -1:
        book.set_name(data["name"])
        book.set_author(data.get("author"))
        book.set_edition(data.get("edition"))
        save_books_db()
        return jsonify({"message": "Alterado com sucesso"})
    else:
        return jsonify(not_found_message()), 404


def search_book(id):
    for book in books:
        if book.get_id() == id:
            return book
        
    return -1


def db_bad_message():
    return {"message": "Data Base is bad!"}

def not_found_message():
    return {"message": "Not Found"}

def save_books_db():
    with open(db_file, "w") as file:
            for book in books:
                file.write(f"{book.get_id()};{book.get_name()};{book.get_author()};{book.get_edition()}\n")


load_books()

if __name__ == "__main__":
    app.run(debug=True)
    pass