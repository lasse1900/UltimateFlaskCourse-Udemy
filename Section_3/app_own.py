from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g, sqlite3

app = Flask (__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sglite3'):
         g.sqlite3_db = connect_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None)
    return "Hello Flask!"

@app.route('/home/', methods=['POST', 'GET'], defaults={'name':'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display = True, mylist=['one','two','three'], listofdictionaries=[{'name':'Zoe'}, {'name':'John'}])

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Not in the session'
    return jsonify({'key':'value','key2':[1,2,3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

@app.route('/theform', methods =['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        # return 'Hello {}. You are from {}. You have submitted the form succesfully!'.format(name, location)
        return redirect(url_for('home', name=name, location=location))
'''
@app.route('/theform', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return 'Hello {}. You are from {}. You have submitted the form succesfully!'.format(name, location)
'''

@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result': 'Success!', 'name': name, 'location' :location, 'randomkeyinlist': randomlist[1]})

if __name__ == '__main__':
    app.run()
