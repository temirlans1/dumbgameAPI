import flask
from flask import request, jsonify
from flask_cors import CORS
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r"/api/*": {"origins": "*"}})
try:
    conn = sqlite3.connect('dumbgame.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE records ([Player_Name] text, [Player_Time] text)""")
    conn.commit()
except: 
    pass

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Testing python api</h1>'''


@app.route('/api/v1/resources/records/all/', methods=['GET'])
def api_all():
    conn = sqlite3.connect('dumbgame.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    records = cur.execute('SELECT * FROM records ORDER BY Player_Time ASC;').fetchall()
    for record in records:
        print(record)
    return jsonify(records)

@app.route('/api/v1/resources/records/', methods=['POST'])
def api_insert_record():
    print(request.json['params'])
    name = request.json['params']['name']
    score = request.json['params']['score']
    print(name + " " + score)
    record = []
    record.append(name)
    record.append(score)
    query = '''INSERT INTO records(Player_Name, Player_Time) VALUES(?,?);'''
        
    try:
        conn = sqlite3.connect('dumbgame.db')
        cur = conn.cursor()
        cur.execute(query, record)
        conn.commit()
        return "Record saved successfully"
    except Exception as e:
        print(e)
        return "An error occured while inserting data"

@app.route('/api/v1/resources/records/', methods=['DELETE'])
def api_delete_record():
    name = ""
    score = ""
    if 'name' in request.args:
        name = request.args.get("name")
    if 'score' in request.args:
        score = request.args.get("score")
    record = []
    
    if name == "" and score == "":
        query = '''DELETE from records;'''
    else :
        
        record.append(name)
        record.append(score)
        query = '''DELETE from records WHERE Player_Name=? and Player_Time=?'''
        
    try:
        conn = sqlite3.connect('dumbgame.db')
        cur = conn.cursor()
        if not record:
            cur.execute(query)
        else :
            cur.execute(query, record)
        conn.commit()
        return "Record deleted successfully"
    except Exception as e:
        print(e)
        return "An error occured while inserting data"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run(threaded=True, port=5000)