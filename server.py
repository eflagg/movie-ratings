"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Show user details."""

    user = User.query.get(user_id)

    return render_template("user_details.html", user=user)


@app.route("/register")
def display_registration_form():
    """ Show sign up form """

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def process_registration():
    """ Add new user to database, sign them in, then redirect to homepage """

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['current_user'] = email
        flash("Logged in as %s" % email)

    return redirect(url_for("show_user_details", user_id=new_user.user_id))


@app.route("/login")
def show_login_form():
    """ Show log in form """

    return render_template("login_form.html")


@app.route("/login", methods=['POST'])
def process_login():
    """ Check if username and password match and if so, log in """

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user.password == password:
        session['current_user'] = email
        flash("Logged in as %s" % email)

        return redirect(url_for("show_user_details", user_id=user.user_id))
    
    else:
        flash("Wrong password!")

        return redirect("/login")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
