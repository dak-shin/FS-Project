from .app import app
from flask import render_template, redirect, url_for, flash, request
from .model import Games, Users, check_duplicate_games
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, PurchaseForm


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", active_home="active")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():

    purchase_form = PurchaseForm()

    if request.method == "POST":
        if purchase_form.validate_on_submit():
            purchased_item = request.form.get('purchased_item')
            if check_duplicate_games(current_user.id, purchased_item):
                flash(
                    f"{purchased_item} already exists in your library!!", category="danger")
            else:
                Games.purchase_game(purchased_item, current_user)
                flash(f"{purchased_item} purchased successfully!! : )",
                      category='success')
        return redirect(url_for('market_page'))

    if request.method == "GET":
        games = Games.get_all_games()
        #owned_games = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=games, active_market="active", purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():  # validates the user input using the validators and then just returns true when the form is submitted
        new_user = Users(Users.get_count()+1, form.username.data,
                         form.password.data)
        new_user.pack()
        login_user(new_user, force=True)
        #raise Exception(current_user)
        flash(f"Account created and logged in succeffully", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        # Validation errors
        for err_msg in form.errors.values():
            flash(f'Error : {err_msg}', category="danger")
    return render_template('register.html', form=form, active_register="active")

# Login page


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_user_by_name(form.username.data)
        if user and user.password.strip() == form.password.data.strip():
            print(user.password, form.password.data)
            login_user(user)

            flash(
                f"Logged in Successfully!! Welcome {current_user.username}", category="success")
            return redirect(url_for('home_page'))
        else:
            flash('Invalid credentials, Please try again', category="danger")

    return render_template('login.html', form=form, active_login="active")

# Logout


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('Logged out successfully', category='info')
    return redirect(url_for('home_page'))


@app.route("/library")
@login_required
def library_page():
    items = Games.get_owned_games(current_user.id)
    # print(list(items))
    return render_template("library.html", active_lib="active", items=list(items))
