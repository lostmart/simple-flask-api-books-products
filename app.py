from flask import Flask, request, jsonify

app = Flask(__name__)

# home
@app.route('/')
def index():
    return 'Bienvenue sur notre API REST simple (avec Python et Flask)'
 
books_list = {
  1: {
    "id": 1,
    "title": "Lord Of The Rings",
    "imgUrl": "https://cdn.kobo.com/book-images/7a557cb3-f72a-47c3-992b-951c9566e4d4/1200/1200/False/the-fellowship-of-the-ring-the-lord-of-the-rings-book-1-1.jpg",
    "year": "1978"
  },
  2: {
    "id": 2,
    "title": "Réseaux & télécoms",
    "imgUrl": "https://www.dunod.com/sites/default/files/styles/principal_desktop/public/thumbnails/image/9782100592586-X.jpg",
    "year": "2013"
  }
}

@app.route('/api/books')
def api():
    return jsonify(books_list)


@app.route('/api/books', methods=['POST'])
def add_book():
    if not request.json:
        return jsonify({"status": "error", "message": "Please provide the book details!"}), 400
    
    # Calculate new ID from dictionary keys
    new_id = max(books_list.keys()) + 1 if books_list else 1
    
    book = {
        "id": new_id,
        "title": request.json['title'],
        "imgUrl": request.json.get('imgUrl', ""),
        "year": request.json.get('year', "")
    }
    
    # Add to dictionary
    books_list[new_id] = book
    
    return jsonify({"status": "success", "message": "Book added successfully!", "book": book})


@app.route('/api/books/<int:id>', methods=["GET", "PUT", "DELETE"])
def get_book(id):
    # Check if book exists
    if id not in books_list:
        return jsonify({
            "status": "error", 
            "message": f"Book with id {id} not found"
        }), 404
    
    # Delete book
    if request.method == "DELETE":
        deleted_book = books_list.pop(id)
        return jsonify({
            "status": "success",
            "message": f"Book with id {id} deleted successfully",
            "deleted_book": deleted_book
        }), 200
    
    # Update book
    if request.method == "PUT":
        books_list[id]["title"] = request.json.get('title', books_list[id]["title"])
        books_list[id]["imgUrl"] = request.json.get('imgUrl', books_list[id]["imgUrl"])
        books_list[id]["year"] = request.json.get('year', books_list[id]["year"])
        
        return jsonify({
            "status": "success",
            "message": "Book updated successfully",
            "book": books_list[id]
        }), 200
    
    # Return the book if GET request
    return jsonify({
        "status": "success",
        "book": books_list[id]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)