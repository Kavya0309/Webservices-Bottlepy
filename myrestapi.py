import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection
from bson.objectid import ObjectId
import datetime
import bottle_mysql
import MySQLdb

connection = Connection('localhost', 27017)
db = connection.nodetest1
sqldb=MySQLdb.connect("localhost","root","kavya","test")

@route('/shirts', method='POST')
def post_document():
    data = request._get_body_string()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    print entity['shirtId']
    if not entity.has_key('shirtId'):
        abort(400, 'No shirtId specified')
    try:
        d=datetime.datetime.now()
        date1=d.strftime("%d/%m/%y")
        entity['createdDate']=date1
        db['shirts'].save(entity)
        return "OK"
    except ValidationError as ve:
        abort(400, str(ve))

@route('/shirt/:shirtId', method='GET')
def get_document(shirtId):
    entity = db['shirts'].find_one({'shirtId':shirtId})
    if not entity:
        abort(404, 'No document with id %s' % shirtId)
    try:
        del entity['_id']
        return entity
    except ValidationError as ve:
        abort(400,str(ve))

@route('/shirts',method='PUT')
def put_document():
    data = request._get_body_string()
    entity=json.loads(data)
    entity1 = db['shirts'].find_one({'shirtId':entity['shirtId']})
    if not entity1:
        abort(404, 'No document found with id %s' % entity['shirtId'])
    try:
        db['shirts'].update({'shirtId':entity1['shirtId']},{'$set':{'shirtName':entity1['shirtName']}})
        return "OK"
    except ValidationError as ve:
        abort(400,str(ve))

@route('/shirts',method='DELETE')
def del_document():
    data=request._get_body_string()
    entity=json.loads(data)
    entity1 = db['shirts'].find_one({'shirtId':entity['shirtId']})
    if not entity1:
        abort(404, 'No document found with id %s' % entity['shirtId'])
    try:
        db['shirts'].remove({'shirtId':entity['shirtId']})
        return "OK"
    except ValidationError as ve:
        abort(400,str(ve))



@route('/shoe/:shoeId', method='GET')
def show(shoeId):
    c=sqldb.cursor()
    c.execute("SELECT * from shoes where shoeID='%s'"%(shoeId))
    row=c.fetchone()
    if not row:
        abort(404,'No document with id %s'%shoeId)
    try:
        column = [t[0] for t in c.description]
        #for row in rows:
        myjson = {column[0]: row[0],column[1]:row[1],column[2]:row[2],column[3]:row[3],column[4]:row[4]}
        myresult = json.dumps(myjson, indent=3)
        return myresult
    except ValidationError as ve:
        abort(400,str(ve))
        
@route('/shoes',method='POST')
def post():
    data=request.body
    if not data:
        abort(400,'No data received')
    entity=json.load(data)
    print entity
    if not entity.has_key('shoeId'):
        abort(400,'No shoeId specified')
    try:
        cursor=sqldb.cursor()
        d=datetime.datetime.now()
        date1=d.strftime("%d/%m/%y")
        sql="""INSERT INTO shoes(shoeID,shoeName,shoeQuantity,createdBy,createdDate) VALUES(%s,%s,%s,%s,%s)"""
        data1=(entity['shoeId'],entity['shoeName'],entity['shoeQuantity'],entity['createdBy'],date1)
        cursor.execute(sql,data1)
        db.commit()
        return "OK"
    except ValidationError as ve:
        abort(400,str(ve))

@route('/shoes',method='PUT')
def show():
    data=request.body
    entity=json.load(data)
    c=sqldb.cursor()
    c.execute("SELECT * from shoes where shoeID='%s'"%(entity['shoeId']))
    row=c.fetchone()
    if not row:
        abort(404,'No document found with id %s'%entity['shoeId'])
    try:
        data1=(entity['shoeName'],entity['shoeId'])
        sql="""update shoes set shoeName=(%s) where shoeID=(%s)"""
        c.execute(sql,data1)
        db.commit()
        return "OK"
    except ValidationError as ve:
        abort(400,str(ve))

@route('/shoes',method='DELETE')
def show1():
    data=request.body
    entity=json.load(data)
    c=sqldb.cursor()
    c.execute("SELECT * from shoes where shoeID='%s'"%(entity['shoeId']))
    row=c.fetchone()
    if not row:
        abort(404,'No document found with id %s'%entity['shoeId'])
    try:
        data1=(entity['shoeId'])
        sql="""delete from shoes where shoeID=(%s)"""
        c.execute(sql,data1)
        db.commit()
        return "OK"
    except ValidationError as ve:
        abort(400,str(ve))
        

run(host='localhost', port=8080)
