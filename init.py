import sqlite3, datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from bs4 import BeautifulSoup
import requests, random
# configuration
DATABASE = 'valids.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def add_to_db(seq):
	with g.db:
	    g.db.execute("insert into emergencies (sequence, begin) values (?, ?);",(seq,datetime.datetime.now()))


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/<seq>',methods=['GET'])
def show_entries(seq):    
    statement="select * from emergencies where sequence = '%s';"%seq
    cur = g.db.execute(statement).fetchall()
    if len(cur)>0:
    	cur=cur[0]
    else:
    	return render_template('notfound.html')
    if cur[3] is None:
    	return render_template('house.html')
    else:
    	return render_template('notfound.html')

@app.route('/map',methods=['POST'])
def retrieve_map():
    headers={"Authorization":"Basic bGVhcm5pbmc6bGVhcm5pbmc="}
    r=requests.get('https://10.10.20.11/api/contextaware/v1/maps?username=learning&password=learning',headers=headers, verify=False)
    r=BeautifulSoup(r.text)
    floor=r.maps.campus.building.floor
    response={"image":floor.image["imagename"],"dimensions":{"width":floor.dimension["width"],"height":floor.dimension["length"]}, "building":{"width":r.maps.campus.building.dimension["width"],"height":r.maps.campus.building.dimension["length"]}}
    return str(response)

@app.route('/people',methods=['POST'])
def retrieve_people():
    headers={"Authorization":"Basic bGVhcm5pbmc6bGVhcm5pbmc="}
    r=requests.get('https://10.10.20.11/api/contextaware/v1/location/clients?username=learning&password=learning',headers=headers,verify=False)
    r=BeautifulSoup(r.text)
    clients=""
    for c in list(r.locations):
        clients+="%s|%s,"%(c.mapcoordinate['x'],c.mapcoordinate['y'])
    return clients[0:-1]

@app.route('/report',methods=['POST'])
def send_report():
    seq=request.form[""]
    seq=seq[seq.index('.com/')+5:]
    with g.db:
        g.db.execute("update emergencies set end = %s where sequence = '%s'"%(datetime.datetime.now(),seq))

if __name__ == '__main__':
    app.run()