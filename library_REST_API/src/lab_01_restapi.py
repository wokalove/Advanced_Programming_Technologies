from flask import Flask,request,json
import sqlite3
import os


app = Flask(__name__)
from datetime import datetime


def connect_to_db():
    dir = os.chdir("../doc")
    db_con = sqlite3.connect('library.db')
    db_con.row_factory = sqlite3.Row
    return db_con
    
@app.route('/api')
def api():
  return "RestApi Bilioteka 2022 - TEST ROUTE"


@app.route('/users', methods=['GET', 'POST'])
def users():
  data = []
  db = connect_to_db()
  cur = db.cursor()
  if request.method == 'GET':
      rows = cur.execute("SELECT * FROM tbl_users;").fetchall()
      for row in rows:
        data.append([x for x in row])
      data = json.dumps(data)
    
      return app.response_class(response=data,
                            status=200,
                            mimetype='application/json')

  if request.method == 'POST':
    json_data = request.get_json()['name']

    user = cur.execute("insert into tbl_users (name) values (?)",(json_data,)).fetchall()
    db.commit()
    return app.response_class(response='Użytkownik dodany do systemu z powodzeniem',
                            status=201,
                            mimetype='application/json')

@app.errorhandler(404) 
@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
def user(id):
    data = []
    db = connect_to_db()
    cur = db.cursor()
    
    if id is None or isinstance(id,int)==False:
        return app.response_class(
                            response ='Nie podano ID użytkownika lub ID w złym formacie',
                            status=400,
                            mimetype='application/json')


    if request.method == 'GET':
        row = cur.execute("SELECT * FROM tbl_users WHERE id=?;",(id,)).fetchall()
        if not row:
            return app.response_class(response ='Użytkownik o podanym ID nie istnieje',
                            status=404,
                            mimetype='application/json')
    
        for r in row:
            data.append([x for x in r])
        
        return app.response_class(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')

    if request.method == 'DELETE':

        row = cur.execute("SELECT * FROM tbl_users WHERE id=?;",(id,)).fetchall()
        if not row:
            return app.response_class(response ='Użytkownik o podanym ID nie istnieje',
                            status=404,
                            mimetype='application/json')
    
        books_left = cur.execute("SELECT return_date FROM tbl_rentals WHERE userid_fk=? and return_date is not null",(id,)).fetchall()
        print(books_left)
        if not books_left:
            return app.response_class(response = 'Nie można usunąć użytkownika z powodu nie zwrócenia wszystkich książek',
                            status=200,
                            mimetype='application/json')
    
        
        to_delete = cur.execute("DELETE FROM tbl_users WHERE id=(?)",(id,)).fetchall()
    
        db.commit()
        return app.response_class(response = 'Usunięcie użytkownika z systemu zakończyło się powodzeniem',
                            status=200,
                            mimetype='application/json')


@app.route('/books', methods=['GET'])
def books():
    data = []
    db = connect_to_db()
    cur = db.cursor()
    if request.method == 'GET':
        rows = cur.execute("SELECT * FROM tbl_books;").fetchall()
        for row in rows:
            data.append([x for x in row])
        data = json.dumps(data)
        return app.response_class(response=data,
                                status=200,
                                mimetype='application/json')

@app.route('/books/<int:id>', methods=['GET'])
def book(id):
    data = []
    db = connect_to_db()
    cur = db.cursor()

    if request.method == 'GET':
        row = cur.execute("SELECT * FROM tbl_books WHERE id=?;",(id,)).fetchall()
        print(row)
        for r in row:
            data.append([x for x in r])
        
        return app.response_class(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')


@app.errorhandler(404) 
@app.route('/books/rent/<int:id>', methods=['PATCH'])
def rent_book(id):
    user = request.headers['user']
    db = connect_to_db()
    cur = db.cursor()
    
    if not user:
        return app.response_class(response = 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy',
                            status=400,
                            mimetype='application/json')

    if id is None or isinstance(id,int)==False:
        return app.response_class(response = 'Podany identyfikator książki nie istnieje lub jest nieprawidłowy',
                            status=401,
                            mimetype='application/json')

    avaiable_books = cur.execute("select quantity from tbl_books where id=?",(id,)).fetchall()
    for book in avaiable_books:
        if book[0]<=0:
            return app.response_class(response = 'Nie ma dostępnych wolnych egzemplarzy dla podanego identyfikatora książki',
                             status=409,
                             mimetype='application/json')

    
    rental_date = datetime.now()
    rent_book = cur.execute("insert into tbl_rentals (userid_fk,bookid_fk,rental_date) values (?,?,?)",(user,id,rental_date)).fetchall()
    update_book = cur.execute("update tbl_books set quantity=quantity-1 Where id=?",(id,)).fetchall()
    db.commit()
    return app.response_class(response = 'Wypożyczenie egzemplarza zakończone powodzeniem',
                            status=201,
                            mimetype='application/json')

@app.errorhandler(404) 
@app.route('/books/return/<int:id>', methods=['PATCH'])
def return_book(id):
    db = connect_to_db()
    cur = db.cursor()
    user = request.headers['user']
    
    if not user:
        return app.response_class(response = 'Podany identyfikator użytkownika nie istnieje lub jest nieprawidłowy',
                            status=401,
                            mimetype='application/json')
    if id is None or isinstance(id,int)==False:
        return app.response_class(response = 'Podany identyfikator książki nie istnieje lub jest nieprawidłowy',
                        status=401,
                        mimetype='application/json')
    
    rented_books = cur.execute("select * from tbl_rentals where userid_fk=(?)",(user,)).fetchall()
    if not rented_books:
        return app.response_class(response = 'Użytkownik nie ma aktualnie wypożyczonych egzemplarzy',
                            status=409,
                            mimetype='application/json')
    else:
        #if user has rented books check if he/she rented book with this id
        rented_books = cur.execute("select * from tbl_rentals where bookid_fk=(?) and userid_fk=(?)",(id,user,)).fetchall()
        if not rented_books:
            return app.response_class(response = 'Użytkownik nie ma aktualnie wypożyczego tego konkretnego egzemplarzu',
                                status=410,
                                mimetype='application/json')
        
  

    returned_book = cur.execute("select return_date from tbl_rentals where bookid_fk=(?) AND userid_fk=(?) and return_date is not null",(id,user,)).fetchall()
    if returned_book:
        return app.response_class(response = 'Książka została już zwrócona',
                            status=411,
                            mimetype='application/json')


    return_date = datetime.now()
    return_book = cur.execute("update tbl_rentals set return_date=? Where bookid_fk=? ",(return_date, id,)).fetchall()
    update_book = cur.execute("update tbl_books set quantity=quantity+1 Where id=?",(id,)).fetchall()
    db.commit()
    
    return app.response_class(response = 'Zwrot wypożyczonego egzemplarza zakończony powodzeniem',
                            status=200,
                            mimetype='application/json')

if __name__ == '__main__':
  app.run()