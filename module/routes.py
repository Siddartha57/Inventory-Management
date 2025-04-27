from flask import render_template, redirect, session, flash, url_for, request,jsonify
from module import app,db
from module.models import User,Staff,Products, Reports, Notification
from module.forms import Login,Register
from .auth import hash, verify
from flask_login import login_user, logout_user, login_required, current_user
import pytz
from datetime import datetime
from .reports import download_report

IST = pytz.timezone("Asia/Kolkata")


@app.route('/admin/approve/<int:id>', methods=['POST'])
def create_user(id):
    user = Staff.query.filter_by(id = id).first()
    print(user)
    try:
        username= user.username
        password = user.password
        email = user.email
        u1 = User(username=username,password=password,email=email)
        db.session.add(u1)
        db.session.commit()
    except Exception as e:
        print(f'error occured {e}')

    finally:
        flash('User Approved','success')
        db.session.close()

    return delete_user(id)

@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = Staff.query.filter_by(id = id).first()
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(f'error occured {e}')

    finally:
        db.session.close()
    return redirect(url_for('dash_page'))

@app.route('/admin/permanent_remove/<int:id>',methods=['POST','GET'])
@login_required
def permanent_remove(id):
    user = User.query.filter_by(id=id).first()
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(f'error occured {e}')

    finally:
        flash(f"user {user.username} has been removed",'info')
        db.session.close()
    return redirect(url_for('staff_list_page'))    


def verify_user():
    try:
        username='siddartha'
        password='siddu123'
        u1 = User.query.filter_by(username=username).first()
        if u1:
            status = verify(u1.password,password)
        else:
            print('user not exist')
    except Exception as e:
        print('error occured {e}')

    return f'{status}'  


# main

@app.route('/')
def base_page():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and verify(user.password,form.password.data):
            if user.role == 'admin':
                db.session.refresh(user)
                login_user(user)
                session.permanent = True
                session['username'] = user.username
                session['email'] = user.email
                flash(f'ADMIN: Logged in as {user.username} ','success')
                return redirect(url_for('ad_home_page'))
            else:
                login_user(user)
                session.permanent = True
                session['username'] = user.username
                session['email'] = user.email
                flash(f'STAFF: Logged in as {user.username} ','success')
                return redirect(url_for('st_dash_page'))   
            
        flash('Invalid details','danger')
    return render_template('login.html',form=form) 

@app.route('/register',methods=['GET','POST'])
def register_page():
    form =Register()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.email.data).first():
                flash('username or email already exist','danger')
                return redirect(url_for('register_page'))
            else:    
                hashed_password = hash(form.password.data)
                new_user = Staff(username=form.username.data,email=form.email.data,password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
        except Exception as e:
            print(f"error occured {e}")
        finally:
            db.session.close()
        flash('Application under process','info')     
        return base_page()
    return render_template('register.html',form=form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('logged out','info')
    return redirect(url_for('base_page'))

@app.route('/clear/alerts',methods=['GET','POST'])
@login_required
def clear_alerts():
    try:
        data = Notification.query.all()
        if data:
            for d in data:
                db.session.delete(d)
            flash(f"Alerts Cleared",'success')    
        else:
            flash("no alerts found",'warning')        
        db.session.commit()
    except Exception as e:
        flash(f"{e}",'danger')
    return redirect(url_for('send_notification'))


# admin

@app.route('/admin/applications')
@login_required
def dash_page():
    data = Staff.query.all()
    return render_template('admin/staff_request.html',users=data)

@app.route('/admin/dashboard')
@login_required
def ad_home_page():
    return render_template('admin/ad_home.html')

@app.route('/admin/staff')
@login_required
def staff_list_page():
    user = User.query.all()
    count =1
    return render_template('admin/staff_list.html',staff=user,count=count)


@app.route('/admin/profile')
@login_required
def admin_profile_page():
    return render_template('admin/admin_profile.html')

@app.route('/admin/stock')
@login_required
def stock_list_page():
    items = Products.query.all()
    return render_template('admin/stock_data.html',items=items)

@app.route('/admin/stock/delete/<string:name>',methods=['GET','POST'])
@login_required
def stock_delete(name):
    item = Products.query.filter_by(name=name).first()
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        db.session.close()        
    return redirect(url_for('inventory_page'))

@app.route('/admin/stock/add',methods=['GET','POST'])
@login_required
def items_add():
    try:
        name= request.form['name']
        price= request.form['price']
        quantity = request.form['quantity']
        item = Products(name=name,price=price,quantity=quantity)
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        flash(f"{e}",'danger')
    finally:
        db.session.close()        
    return redirect(url_for('stock_list_page'))

@app.route('/admin/send/alerts')
@login_required
def send_alert_page():
    return render_template('/admin/send_alerts.html')

@app.route('/admin/send_notification',methods=['GET','POST'])
@login_required
def send_notification():
    try:
        msg = request.form.get('message')
        alert = Notification(content=msg)
        db.session.add(alert)
        db.session.commit()
        flash(f"Notification sent successfully",'success')
    except Exception as e:
        flash(f"")
    finally:
        db.session.close()
    return render_template('/admin/send_alerts.html')


#staff
@app.route('/staff/dashboard')
@login_required
def st_dash_page():
    return render_template('staff/staff_page.html')

@app.route("/get_notifications")
@login_required
def get_notifications():
    notifications = Notification.query.all()
    return render_template("notifications.html", notifications=notifications)


@app.route('/staff/profile')
@login_required
def staff_profile_page():
    return render_template('staff/staff_profile.html')

@app.route('/staff/inventory')
@login_required
def inventory_page():
    item = Products.query.all()
    return render_template('staff/inventory.html',items=item)

@app.route('/staff/inventory/list/<int:id>',methods=['POST','GET'])
@login_required
def items_update(id):
    item = Products.query.filter_by(id=id).first()
    print(item.name)
    try:
        if item:
            item.name = request.form['name']
            item.quantity= request.form['quantity']
            item.price = request.form['price']
            item.updated_date = datetime.now(IST)
            db.session.commit()
    except Exception as e:
        print(e)
    finally:
        db.session.close()    
    return redirect(url_for('inventory_page'))

@app.route('/staff/billing/',methods=['POST','GET'])
@login_required
def billing_page():
    items = Products.query.all()
    id = request.form.get("item")
    qty = request.form.get("quantity")
    item = Products.query.filter_by(id=id).first()
    try:
        if item.quantity < int(qty) and item.quantity>0:
            flash(f'Sorry Only {item.quantity} Units available','danger')
        elif item.quantity==0:
            flash(f"Stock is not available",'danger')    
        else:
            item.quantity = item.quantity - int(qty)
            report = Reports(name=item.name,quantity=int(qty),price=item.price)
            db.session.add(report)
            db.session.commit()
            flash("Bill Generated",'success')

    except Exception as e:
        flash(f"Enter details to bill",'warning')          
    return render_template('staff/billing_page.html',items=items)

@app.route('/stock/reports')
@login_required
def stock_reports_page():
    reports  = Reports.query.all()
    return render_template('stock_report.html',reports=reports)

@app.route('/stock/reports/pdf',methods=['GET','POST'])
def get_pdf():
    return download_report()


# @app.route('/test')
# def test():
#     username = 'Rakshitha'
#     password = 'welcome'
#     hashed = hash(password)
#     user = User(username=username,password=hashed,email='rakshithapagadala29@gmail.com',role='admin')
#     db.session.add(user)
#     db.session.commit()
#     return "user created"