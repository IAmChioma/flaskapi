import flask
from flask import request, jsonify
import sqlite3
app = flask.Flask(__name__)
app.config['DEBUG'] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return "<h1> This is an API prototype</h1>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def all_books():
    return jsonify(books)


@app.route('/api/v1/resources/books/id', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    result = []
    for book in books:
        if book['id'] == id:
            result.append(book)

    return jsonify(result)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d


@app.route('/api/v2/resources/books/all', methods=['GET'])
def api_db_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)


@app.errorhandler(400)
def page_not_found(e):
    return "<h1>404, The resource couls not be found</h1>",404


@app.route('/api/v2/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)

    if author:
        query += ' author=? AND'
        to_filter.append(author)

    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)
app.run()
