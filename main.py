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
    return 'Unlucky, no items are here when you walk this PATH', 404

@app.route('/create/' , methods = ['GET','POST'])
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
        return redirect('/')
 
 
@app.route('/')
def RetrieveList():
    items = itemModel.query.filter_by(deleted = False).all()
    return render_template('datalist.html',items = items)
 
@app.route('/deletedItems/')
def RetrieveDeletedList():
    items = itemModel.query.filter_by(deleted = True).all()
    return render_template('datalistDeleted.html',items = items)
	
@app.route('/<int:id>/')
def RetrieveItem(id):
    item = itemModel.query.filter_by(itemID = id).first()
    if item:
        if item.deleted == False:
	        return render_template('data.html', item = item)
        else:
            return render_template('deletedData.html', item = item)
    return f"Item with id = {id} Doesn\'t exist"
 
 
@app.route('/<int:id>/update/',methods = ['GET','POST'])
def update(id):
    item = itemModel.query.filter_by(itemID=id).first()
    if request.method == 'POST':
        if item:
            db.session.commit()
            item.name = request.form['name']
            item.category = request.form['category']
            item.location = request.form['location']
            item.quantity = request.form['quantity']
            db.session.commit()
            return redirect(f'/{id}')
        return f"Item with id = {id} Doesn\'t exist"
 
    return render_template('update.html', item = item)
 
 
@app.route('/<int:id>/delete/', methods=['GET','POST'])
def delete(id):
    item = itemModel.query.filter_by(itemID=id).first()
    if request.method == 'POST':
        if item:
            item.deleted = True
            item.deletionComment = request.form['comment']
            db.session.commit()
            return redirect('/')

 
    return render_template('delete.html')

@app.route('/<int:id>/undelete/', methods=['GET','POST'])
def undelete(id):
    item = itemModel.query.filter_by(itemID=id).first()
    if request.method == 'POST':
        if item:
            item.deleted = False
            db.session.commit()
            return redirect('/')

 
    return render_template('undelete.html')
 

web.run(app)