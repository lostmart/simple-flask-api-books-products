from flask import Flask, request, jsonify

app = Flask(__name__)

# home
@app.route('/',)
def index():
    return {'res': "welcome to the books API.",
           "get books endpoint": "/api/books"
           }


books_list = {
  1 : {
    "id": 1,
    "title": "Lord Of The Rings",
    "imgUrl": "https://cdn.kobo.com/book-images/7a557cb3-f72a-47c3-992b-951c9566e4d4/1200/1200/False/the-fellowship-of-the-ring-the-lord-of-the-rings-book-1-1.jpg",
    "year": "1978"
    
  },
  2 : {
    "id": 2,
    "title": "Réseaux & télécoms",
    "imgUrl": "https://www.dunod.com/sites/default/files/styles/principal_desktop/public/thumbnails/image/9782100592586-X.jpg",
    "year": "2013"
    
  }
}

# gerers les livres (READ, CREATE)
@app.route('/api/books', methods=["GET", "POST"])
def handle_books():
  if request.method == "GET":
    return {'res': books_list}
  else:
    sent_data = request.json
    book_array = list(books_list.items())
    new_id = len(book_array) + 1
    new_book =   {
            "id": new_id,
            "title": request.json['title'] ,
            "imgUrl": "https://www.dunod.com/sites/default/files/styles/principal_desktop/public/thumbnails/image/9782100592586-X.jpg",
            "year": "2013"
            
        }
    books_list[ int(new_id) ] = new_book
    return {'res': sent_data}, 201

# gerer une seul livre (READ, UPDATE, DELETE)
@app.route('/api/books/<int:id>', methods=["GET", "PUT", "DELETE"])
def one_book(id):
  # find the book
  if not books_list.get(id):
    return {"res": "livre not found" }, 404
  else:
    if request.method == "GET":
        return { "res": books_list.get(id) }, 200
    elif request.method == "PUT":
        new_title = request.json.get('title') 
        new_year = request.json.get('year')
        new_imgUrl = request.json.get('imgUrl')

        if new_title:
          books_list[int(id)].update({"title": new_title})
        if new_year:
          books_list[int(id)].update({"year": new_year})
        if new_imgUrl:
          books_list[int(id)].update({"imgUrl": new_imgUrl})

        return { "res": books_list[int(id)] }, 202
    elif request.method == "DELETE":
        # add try/catch block
        books_list.pop(int(id))

        return { "res": f"livre id: {id} deleted " }, 202



app.debug = True
app.run()
