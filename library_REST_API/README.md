# **LABORATORIUM 01** - Implementacja API w oparciu o wzorzec architektoniczny REST w języku Python
<br />

___
###  **Temat Zadania**
 *W oparciu o mikroframework Flask oraz wzorzec REST zaimplementuj API obsługujące proces wypożyczania książek w bibliotece.*
___ 
<br>

## 1. Definicja enpoint`ów dla API:
1. Pobieranie listy użytkowników z bazy biblioteki:
   >  GET /api/users
      
2. Pobieranie szczegółowych informacji o koncie użytkownika dla podanego `id`:
    > GET /api/users/<<id: integer>>

3. Dodawanie nowego użytkonika do systemu:
    > POST /api/users

4. Usuwanie użytkownika o podanym `id` z bazy biblioteki
    > DELETE API/user/<<id: integer>>

5. Pobieranie lista tytułów książek z bazy biblioteki:
    > GET /api/books

6. Pobieranie szczegółowych informacji n/t tytułu o podanym `id`:
    > GET /api/books/<<id: integer>>

7. Obsługa wypożyczenia egzemplarza tytułu książki o podanym `id`:
    > PATCH /api/books/rent/<<id: integer>> 

8. Obsługa zwrotu egzemplarza tytułu książki o podanym `id`:
    > PATCH /api/books/return/<<id: integer>>

<br />

Szczegółowa definicja implentacji zapytań oraz odpowiedzi HTTP zostały opisana w pliku [rest-biblioteka-swagger.yaml](./doc/rest-biblioteka-swagger.yaml) w katalogu [doc](./doc/) zgodnie z standartem [OpenApi](https://spec.openapis.org/oas/v3.0.3).

Do otwarcia pliku [rest-biblioteka-swagger](./doc/rest-biblioteka-swagger.yaml) użyj aplikacji Postman opisanej w sekcji [Praca z aplikacją Postman](#praca-z-aplikacją-postman).


## 2. Konfiguracja środowiska developerskiego.
1. Przejdź do katalogu w którym przechowujesz repozytoria do przedmiotu ZTP. Jeśli jeszcze takiego nie posiadasz utwórz nowy katalog np. o nazwie `lab-ztp`.
2. Do katalogu `lab-ztp` sklonuj repozytorium  `pk_ztp_lab_01_python_rest-<<username>>`:
   
    > `git clone pk_ztp_lab_01_python_rest-<<username>>`

3. Przejdź do folderu zawierajacego sklonowane repozytorium.
4. Utwórz wirtualne środowisko python:
    > `python3 -m venv .venv`

5. Aktywuj wirtualne środowisko:
    > `.ven\Scripts\activate`

6. Zainstaluj framework Flask:
   > `pip install flask`

7. Przejdź do katalogu `src\` i utwórz plik aplikacji o nazwie `lab_01_restapi.py`. 

***Cały kod aplikacji powinnien być umieszczony w pliku `lab_01_restapi.py`***

8. Upewnij się, że pracujesz na gałęzi `main`:
    > `git status`
  
    jeśli nie, przełącz się na gałąź `main`:

    > `git checkout main`

9.  Dodaj katalog .venv to pliku .gitignore.

10. Utwórz migawkę kodu do repozytorium:
    > `git add .`\
    > `git commit -m "Konfiguracja środowiska developerskiego"`
## 3. Implementacja szkieletu aplikacji 

1. Otwórz plik `lab_01_restapi.py` i rozpocznij implementacje.
2. Zaimportuj klasę Flask z modułu flask:
   > `from flask import Flask`

3. Utwórz obiekt klasy Flask:
    > 'app = Flask(__name__)

4. Ta część pliku jest przeznaczona na implementacje endpoint'ów zdefiniownaych w sekcji [Definicja enpoint'ów dla API](#1-definicja-enpointów-dla-api).
5. Zaimplementujmy pierwszego endpoit'a `/api` który zwróci przykładowy tekst:
    ```python
    @app.route('/api')
    def api():
      return "RestApi Bilioteka 2022"

    ```

6. Na końcu pliku wstaw kod który będzie uruchamiał naszą aplikacje bezpośrednio z tego skryptu dla domyślnych wartości `host` oraz `port`
    ```python
    if __name__ == '__main__':
      app.run()
    ```

7. Uruchom aplikację poleceniem:
    > `python -m lab_01_restapi`

8. Popraw błędy jeśli aplikacja się nie uruchomiła poprawnie.
9. Otwórz przeglądarkę i wpisz adres: `http://127.0.0.1:5000/api` i sprawdź czy został wyświetlony tekst z utworzonego endpoint'u.
10. Utwórz migawkę kodu dodając komentarz "Implementacja szkieletu aplikacji."







## 4. Ocena rozwiązania
* poprawnie zaimplementowanie wymaganych endpoint'ów, 
* poprawnie zaimplementowanie obsługa parametrów przesyłanych w zapytaniach,
* zaimplementowanie zwracanych kodów błędów oraz danych zgodnie ze specyfikacją,


## 5. Przykłady implementacji

### 5.1. Definiowanie endpoint'ów przy pomocy dekoratora Flask `@route` - przykad


```python
# app.py
from flask import request

@app.route('/users', methods=['GET', 'POST'])
def users():
  if request.method == 'GET':
    pass

  if request.method == 'POST':
    pass


@app.route('/books/rent/<int: id>', methods=['PATCH'])
def rent_book(id):
    pass
```

### 5.2 Odczytywanie danych z zapytania.

```python
from flask import request
...

@app.route('/books/rent/<int: id>', methods=['PATCH'])
def rent_book(id):
  '''
  Parametr przesyłany w nagłówku zapytania:
  curl -X PATCH http://localhost:5000/books/return/3 \
    -H 'accept: application/json' \
    -H 'user: 20' \
    -H 'Content-Type: application/json' \
    -d '{ 'username": "Jan Nowak" }'
  '''
    # Odczytanie wartości parametru 'user' z nagłówka zapytania:
    user = request.headers['user']

    # Odczytanie struktury JSON z parametrem 'username':
    json_data = request.get_json()
    pass


@app.route('/books', methods=['GET'])
def books():
  '''
  Dla parametru przekazanego w postaci querery:
  curl -X PATCH http://localhost:5000/books?author=Grzegorczyk \
    -H 'accept: application/json'
  '''

  author = request.args.get('author')
  pass

```

### 5.3. Zwracanie dany w formacie JSON oraz statusu.

```python
from flask import json

@app.route('/books', methods=['GET'])
def books():
  .
  .
  .
  return app.response_class(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')

```
## 5. Baza danych SQLite3
* Baza danych w pamięci RAM:
```python
# app.py
import sqlite3
# Podłączenie do bazy
db_con = sqlite3.connect(:memory:)
db_con.row_factory = sqlite3.Row

# Inicjalizacja przykładowej bazy danych


with open('doc/create_library_db.sql','r') as f:
  db_con.executescript(f.read())
  db_con.commit()
  
# Wywołanie kwerendy SQL

cur = db_con.cursor()
row = cur.execute("SELECT * FROM tbl_books;").fetchall()

# konwersja do JSON'a
data = json.dumps(row)
```





