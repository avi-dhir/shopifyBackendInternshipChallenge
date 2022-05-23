from flask import Flask,render_template,request,redirect
from models import db
from models import itemModel
from replit import web

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return 'dumb error', 404

@app.route('/data/create/' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        location = request.form['location']
        quantity = request.form['quantity']
        item = itemModel(name = name, category = category, location = location, quantity = quantity)
        db.session.add(item)
        db.session.commit()
        return redirect('/data')
 
 
@app.route('/data/')
def RetrieveList():
    item = itemModel.query.all()
    return render_template('datalist.html',items = item)
 
 
@app.route('/data/<int:id>/')
def RetrieveItem(id):
    item = itemModel.query.filter_by(itemID = id).first()
    if item:
        return render_template('data.html', item = item)
    return f"Item with id ={id} Doesn\'t exist"
 
 
@app.route('/data/<int:id>/update/',methods = ['GET','POST'])
def update(id):
    item = itemModel.query.filter_by(itemID=id).first()
    if request.method == 'POST':
        if item:
            db.session.delete(item)
            db.session.commit()
            name = request.form['name']
            category = request.form['category']
            location = request.form['location']
            quantity = request.form['quantity']
            item = itemModel(name = name, category = category, location = location, quantity = quantity)
            db.session.add(item)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Item with id = {id} Doesn't exist"
 
    return render_template('update.html', item = item)
 
 
@app.route('/data/<int:id>/delete/', methods=['GET','POST'])
def delete(id):
    item = itemModel.query.filter_by(itemID=id).first()
    if request.method == 'POST':
        if item:
            db.session.delete(item)
            db.session.commit()
            return redirect('/data')

 
    return render_template('delete.html')
 

web.run(app)