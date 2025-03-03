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
                print(book.get_edition())
                books.append(book.to_dict())
            
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
    return last_book["id"]


@app.route("/books", methods=["POST"])
def add_book():
    global last_id
    book_id_controller = last_id+1
    print(book_id_controller)
    if book_id_controller != 0:
        data = request.get_json()
        book = Book(id=book_id_controller, name=data.get("name"), author=data.get("author"), edition=data.get("edition", None))
        
        last_id += 1

        books.append(book.to_dict())

        save_books_db()

        return jsonify({"message": "Cadastrado com sucesso"})
    else:
        return jsonify(db_bad()), 500
    

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({"books": books, "books_quantity": len(books)})
    

def db_bad():
    return {"message": "Data Base is bad!"}


def save_books_db():
    with open(db_file, "w") as file:
            for book in books:
                file.write(f"{book["id"]};{book["name"]};{book["author"]};{book["edition"]}\n")


load_books()

if __name__ == "__main__":
    app.run(debug=True)
    pass