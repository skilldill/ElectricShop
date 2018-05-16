from flask import Flask, request, render_template, session, redirect, url_for
import mysqlworker

dbConfig={'host':'127.0.0.1',
          'user':'root',
          'password':'7543221erhjgerhjgerhjg',
          'database':'ElShop'}

user=mysqlworker.User(dbConfig)
shop=mysqlworker.Shop(dbConfig)
admin=mysqlworker.Admin(dbConfig)
        
app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def main():
    catigorys=shop.GetCategorys()
    products=shop.GetProducts()
    return render_template('products.html', title_text="Электроника",
                           Catigorys=catigorys,Products=products)

@app.route('/admin')
def adminIn():
    catigorys=shop.GetCategorys()
    if ('login' in session) and ('pass' in session):
        return render_template('admin_page.html',title_text="Админка",
                               Catigorys=catigorys)
    
    return render_template('admin_log.html', title_text="Вход",
                           Catigorys=catigorys, attention="")

@app.route('/admin_page', methods=['POST'])
def administrate():
    catigorys=shop.GetCategorys()
    if request.method=='POST':
        login=request.form['login']
        password=request.form['pass']
        if admin.GetLoginAndPass()==login+password:
            session['login']=login
            session['pass']=password
            return render_template('admin_page.html',title_text="Админка",
                                   Catigorys=catigorys)
        return render_template('admin_log.html',title_text="Вход",
                           Catigorys=catigorys, attention="*Неверный логин или пароль")
           
    return render_template('admin_log.html',title_text="Вход",
                           Catigorys=catigorys, attention="")

@app.route('/admin_out')
def logout():
    session.pop('login')
    session.pop('pass')
    return redirect(url_for('adminIn'))

@app.route('/about')
def about():
    return 'Магазин основан в 2018 году ближе к лету'
    
@app.route('/catalog')
def showCatalog():
    catigorys=getCatArrayFromSQL('select name from categories')
    products=getFromSQL('''select * from products''')
    return render_template('catalog.html',title_text="Каталог" ,
                           Products=products,
                           Catigorys=catigorys)

@app.route('/admin_command', methods=['POST'])
def UpdateDb():
    if(request.form['name_command']=="add"):
        param=[request.form['name'],
               request.form['discription'],
               request.form['cat_name'],
               request.form['image'],
               ]
                
        admin.AddProduct()

@app.route('/image')
def showImage():
    image='template/1.jpg'
    #image=getFromSQL('''select image from products where id=1''')[0][0]
    return render_template('baseimage.html', Image=image)

@app.route('/admin/setorder')#, methods=['POST'])
def getOrder():
    catigorys=shop.GetCategorys()
    orders=admin.CheckOrders()
    return render_template('grid_order.html', title_text='Заказы',
                           Orders=orders,
                           Catigorys=catigorys)

if __name__ == '__main__':
    app.run(debug=True)


