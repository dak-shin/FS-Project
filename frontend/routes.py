from flask_wtf import form
from .app import app
from flask import render_template, redirect, url_for, flash, request
from .model import Games, Users, check_duplicate_games, Admin
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, PurchaseForm, GameForm, GameEditForm, GameDeleteForm, SearchForm


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", active_home="active")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():

    purchase_form = PurchaseForm()
    search_form = SearchForm()
    message = ""

    if request.method == "POST":
        if purchase_form.submit.data and purchase_form.validate():
            purchased_item = request.form.get('purchased_item')
            if check_duplicate_games(current_user.id, purchased_item):
                flash(
                    f"{purchased_item} already exists in your library!!", category="danger")
            else:
                Games.purchase_game(purchased_item, current_user)
                flash(f"{purchased_item} purchased successfully!! : )",
                      category='success')
        return redirect(url_for('market_page'))

    games = Games.get_all_games()

    if request.method == "GET":
        if request.args.get('game_name', None):
            rrn = Games.get_rrn(request.args["game_name"])
            if rrn:
                games = Games.get_arr(rrn)
            else:
                message = "No game found"
    return render_template('market.html', items=games, active_market="active", purchase_form=purchase_form, search_form=search_form, message=message)


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
    return render_template("library.html", active_lib="active", items=list(items))


@app.route("/admin")
def admin_page():
    logout_user()
    return redirect(url_for('admin_login_page'))


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.get_user_by_name(form.username.data)
        if user and user.password.strip() == form.password.data.strip():
            login_user(user)
            flash(
                f"Logged in Successfully as admin !! Welcome {current_user.username}", category="success")
            return redirect(url_for('admin_home_page'))
        else:
            flash('Invalid credentials, Please try again',
                  category="danger")

    return render_template('admin_login.html', form=form, active_login="active")


@app.route("/admin/home", methods=['GET', "POST"])
@login_required
def admin_home_page():
    gameform = GameForm()

    if request.method == "POST":
        if gameform.validate_on_submit():  # validates the user input using the validators and then just returns true when the form is submitted
            game_obj = Games(gameform.name.data, gameform.genre.data, " ".join(gameform.pf.data),
                             gameform.desc.data, gameform.pub.data, str(gameform.r_date.data.year), str(gameform.price.data), )
            game_obj.pack()

            flash(gameform.name.data+" added successfully", category="success")
            return redirect(url_for("admin_home_page"))
        if gameform.errors != {}:
            # Validation errors
            for err_msg in gameform.errors.values():
                flash(f'Error : {err_msg}', category="danger")

        return redirect(url_for("admin_home_page"))

    if request.method == "GET":
        games = Games.get_all_games()
        return render_template('admin_home.html', items=games, gameform=gameform)


@login_required
@app.route('/admin/edit/<name>', methods=['GET', 'POST'])
def edit_page(name):
    game_delForm = GameDeleteForm()
    gameEditForm = GameEditForm()
    edited_item = request.form.get('og_name')
    rrn = Games.get_rrn(name)
    game = Games.get(rrn)

    if game_delForm.submit2.data and game_delForm.validate():
        name = request.form.get('game_name')
        Games.delete(name)
        flash(name+" is deleted successfully!!", category="success")
        return redirect(url_for("admin_home_page"))

    if gameEditForm.submit1.data and gameEditForm.validate():
        new_rrn = Games.get_rrn(edited_item)
        if new_rrn:
            game_obj = Games(gameEditForm.name.data, gameEditForm.genre.data, " ".join(gameEditForm.pf.data),
                             gameEditForm.desc.data, gameEditForm.pub.data, str(gameEditForm.r_date.data), str(gameEditForm.price.data), )

            game_obj.modify(rrn, gameEditForm.og_name.data)
            flash("Changes saved successfull", category="success")
        return redirect(url_for("admin_home_page"))
    if gameEditForm.errors != {}:
        # Validation errors
        for err_msg in gameEditForm.errors.values():
            flash(f'Error : {err_msg}', category="danger")

    return render_template('edit_item.html', item=game, gameEditForm=gameEditForm, game_delForm=game_delForm)
