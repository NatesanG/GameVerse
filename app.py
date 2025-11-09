from flask import Flask,render_template,request,session,redirect,flash,url_for
from flask_mysqldb import MySQL
from pymongo import MongoClient
from bson import ObjectId
import os

app=Flask(__name__)
app.secret_key="NA123tE456sAn789"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="login"

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Store']
game = mongo_db['Games']
newss=mongo_db['News']
ev=mongo_db['Events']

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store')
def store():
    query=request.args.get('q','').strip()
    if query:
        search=list(game.find({
            "$or":[
                {"name":{"$regex":query,"$options":"i"}}
            ]
        }))
        new_games=popular_games=search
    else:
        new_games=list(game.find({"cat":"new"}))
        popular_games=list(game.find({"cat":"popular"}))
    return render_template('store.html',new_games=new_games,popular_games=popular_games)

@app.route('/game/<id>')
def game_details(id):
    single_game=game.find_one({"_id":ObjectId(id)})
    if not single_game:
        return "No Game found 404"
    return render_template('game.html',games=single_game)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/event')
def event():
    comp_ev =list(ev.find({"status":"completed"}))
    ong_ev =list(ev.find({"status":"ongoing"}))
    return render_template('event.html',comp_ev=comp_ev,ong_ev=ong_ev)

@app.route('/support')
def support():
    return render_template('supprt.html')

@app.route('/news')
def news():
    new=list(newss.find())
    return render_template('news.html',new=new)

@app.route('/login',methods=['GET'])
def login():
    return render_template("login.html")
 
@app.route('/account',methods=['GET'])
def open():
    return render_template('account.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = 0

    for item in cart_items:
        price_str = str(item.get('price', '0'))
        price_num = int(price_str.replace('₹', '').replace(',', '').strip())
        total += price_num

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/store',methods=['POST'])
def save():
    email=request.form['email']
    password=request.form['password']
    cur=mysql.connection.cursor()
    cur.execute('select * from account where Email=%s and Password=%s',(email,password))
    user=cur.fetchone()
    cur.close()
    if user:
        return render_template('store.html')
    else:
        return render_template('account.html')

@app.route('/login',methods=['POST'])
def account():
    name=request.form['name']
    email=request.form['email']
    password=request.form['password']
    confirm=request.form['confirm']
    cur=mysql.connection.cursor()
    cur.execute('insert into account(Name,Email,Password,Confirm_Password) values (%s,%s,%s,%s)',(name,email,password,confirm))
    mysql.connection.commit()
    cur.close()
    return render_template('login.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    game_id = request.form.get('game_id')
    game_data = game.find_one({'_id': ObjectId(game_id)})

    if game_data:
        if 'cart' not in session:
            session['cart'] = []
        game_data['_id'] = str(game_data['_id'])
        session['cart'].append(game_data)
        flash(f"{game_data['name']} added to cart!")

    return redirect(url_for('store'))

@app.route('/remove_from_cart/<game_id>')
def remove_from_cart(game_id):
    if 'cart' in session:
        session['cart'] = [g for g in session['cart'] if g['_id'] != game_id]
    return redirect(url_for('cart'))


if __name__=="__main__":
    app.run(debug=True)