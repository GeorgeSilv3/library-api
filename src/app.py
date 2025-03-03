from flask import Flask, request, jsonify
from models.book import Book

app = Flask(__name__)

db_file = "src/db/books.csv"

def verify_last_id():
    try:
        with open(db_file, "r") as file:
            last_line = file.readlines()[-1]
            delimiter_index = last_line.find(";")
            last_id = int(last_line[:delimiter_index])
            print(last_id)
    except FileNotFoundError:
        print("File Not Found!")
        return -1
    except ValueError:
        print("Error trying convert to integer")
        return -1
    except Exception:
        print("Something Was Wrong.")
        return -1
    else:
        return last_id


@app.route("/books", methods=["POST"])
def add_book():
    book_id_controller = verify_last_id()+1
    if book_id_controller != 0:
        data = request.get_json()
        book = Book(id=book_id_controller, name=data.get("name"), author=data.get("author"), edition=data.get("edition", None))
        book_id_controller += 1

        with open(db_file, "a") as file:
            file.write(f"\n{book.get_id()};{book.get_name()};{book.get_author()};{book.get_edition()}")

        return jsonify({"message": "Cadastrado com sucesso"})
    else:
        return jsonify(db_bad), 500
    

@app.route("/books", methods=["GET"])
def get_books():
    books = []
    try:
        with open(db_file, "r") as file:
            for line in file.readlines():
                book = line.split(";")
                book = Book(id=int(book[0]), name=book[1], author=book[2], edition=book[3])
        
                books.append(book.to_dict())
    except FileNotFoundError:
        print("File not Found")
        return jsonify(db_bad), 500

    else:
        return jsonify({"books": books, "books_quantity": len(books)})
    

def db_bad():
    return {"message": "Data Base is bad!"}

if __name__ == "__main__":
    app.run(debug=True)
    pass