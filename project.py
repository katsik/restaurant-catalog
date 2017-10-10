from flask import Flask
from flask import render_template,url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem 

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

app = Flask(__name__)

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant1 = session.query(Restaurant).filter_by(id = restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant = restaurant1).all()
    return jsonify(menuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    restaurant1 = session.query(Restaurant).filter_by(id = restaurant_id).first()
    item = session.query(MenuItem).filter_by(restaurant = restaurant1, id = menu_id).first()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants/')
def restaurantsList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants = restaurants, counter = 0)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant_1 = session.query(Restaurant).filter_by(id = restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant = restaurant_1).all()
    return render_template('menu.html',restaurant = restaurant_1,items=items)


# This function is used for creating new menu items 
@app.route('/restaurants/<int:restaurant_id>/new/',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        return render_template('newmenuitem.html',restaurantId = restaurant_id)
    elif request.method == 'POST':
        flash('Your item was created successfully')
        new_item = MenuItem(name = request.form['name'], price = request.form['price'], course= request.form['course'], description = request.form['description'] ,restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

    # return "page to create a new menu item. Task 1 complete!"

# This function is used for editing menu items

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    if request.method == 'GET':
        return render_template('editmenuitem.html',restaurantId = restaurant_id,menuId = menu_id, item = item)
    elif request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.course = request.form['course']
        session.add(item)
        session.commit()
        flash('%s was editted successfully' %request.form['name'])         
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

# This function is called for deleting menu items 

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    if request.method == 'GET':
        return render_template('deletemenuitem.html',item = item)
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('%s was deleted successfully' %item.name)
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))


#This function is called for creating new Restaurant instances
@app.route('/restaurants/new',methods = ['GET','POST'])
def createRestaurant():
    if request.method == 'GET':
        return render_template('createrestaurant.html')
    elif request.method == 'POST':
        restaurant = Restaurant(name = request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("%s was added successfully to the restaurant list" %restaurant.name)
        return redirect(url_for('restaurantsList'))


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0',port=5000)