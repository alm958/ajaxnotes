from flask import Flask, render_template, request, redirect, flash, session, jsonify
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'notesajax')

@app.route('/')
def index():
    return render_template('ajaxnotes.html')

@app.route('/notes')
def posts():
    notes = mysql.query_db("SELECT * FROM notes")
    return jsonify(notes)

@app.route('/notes/create', methods=['post'])
def create():
    query = "INSERT INTO notes (title, content, created_at, updated_at) VALUES(:title,:note,NOW(), NOW());"
    data = {'title':request.form['title'],'note':request.form['content']}
    new_note_ID = mysql.query_db(query, data)
    nquery = "SELECT * FROM notes WHERE id = :new_note_ID"
    ndata = {'new_note_ID':new_note_ID}
    new_post = mysql.query_db(nquery,ndata)
    return jsonify(new_post)

@app.route('/notes/delete', methods=['post'])
def delete():
    query = "DELETE FROM notes WHERE id = :id"
    data = {'id':request.form['id']}
    print data
    print request.form['id']
    delid = mysql.query_db(query, data)
    return jsonify(delid)

if __name__ == "__main__":
    app.run(debug=True)
