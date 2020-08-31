import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # Select user's owns
    purchase_history = db.execute("SELECT symbol, SUM(shares) FROM purchase WHERE id = :user_id GROUP BY symbol",
                                  user_id=session["user_id"])

    # Ensure the first time log in
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                      user_id=session["user_id"])
    if purchase_history == None:
        return render_template("index.html", purchases=None, balance=cash)

    # Sort the purchases table out
    balance = 0
    for i in range(len(purchase_history)):

        # Get the current price through lookup
        purchase_history[i]["current_price"] = lookup(purchase_history[i]["symbol"])["price"]

        # Assign the total(current_price * shares)
        purchase_history[i]["total"] = round(purchase_history[i]["current_price"] * purchase_history[i]["SUM(shares)"], 2)

        # Calculate the current balance(stock's total plus cash)
        balance = purchase_history[i]["total"] + balance

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                      user_id=session["user_id"])[0]["cash"]
    balance += cash

    return render_template("index.html", purchases=purchase_history, cash=cash, balance=round(balance, 2))

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure current password was submitted
        elif not request.form.get("current password"):
            return apology("must provide current password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current password")):
            return apology("invalid username and/or current password", 403)

        # Ensure new password and confirmation exit
        new = request.form.get("new password")
        confirmation = request.form.get("confirmation")

        if (not new) or (not confirmation):
            return apology("must provide new password and/or confirmation", 403)

        # Ensure new password and confirmation the same
        elif new != confirmation:
            return apology("must provide same new password and confirmation", 403)

        # Query database for changing password
        db.execute("UPDATE users SET hash = :new WHERE id = :user_id",
                   new=generate_password_hash(new), user_id=session["user_id"])

        # Log out
        return redirect("/logout")

    else:
        return render_template("password.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        # Get the symbol into memory
        symbol = request.form.get("symbol")

        # Go through lookup
        lookup_dic = lookup(symbol)

        # Ensure symbol was submitted and exists
        if (not symbol) or (not lookup_dic):
            return apology("correct symbol is required", 403)

        # Ensure shares were submitted
        elif (not request.form.get("shares")):
            return apology("must provide shares", 403)

        # Ensure shares were integer
        try:
            float(request.form.get("shares"))

            # Ensure shares were positive integer
            if (not float(request.form.get("shares")).is_integer()) or float(request.form.get("shares")) <= 0.00:
                return apology("must provide positive integer", 403)
        except ValueError:
            return apology("invalid shares", 403)

        # Get the cash the user has
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        # Ensure user can afford the price
        total_price = float(request.form.get("shares")) * lookup_dic["price"]
        if cash[0]["cash"] < total_price:
            return apology("cannot afford the purchase", 403)

        # Record purchase in table purchase
        db.execute("INSERT INTO purchase (id, symbol, price, shares, 'purchase/sale') VALUES (:user_id, :symbol, :price, :shares, :purchase)",
                   user_id=session["user_id"], symbol=symbol, price=-total_price, shares=request.form.get("shares"), purchase='purchase')

        # Update data in users
        value = 10000.00 - total_price
        db.execute("UPDATE users SET cash = :value WHERE id = :user_id",
                   value=value, user_id=session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, price, shares, 'purchase/sale', Timestamp FROM purchase WHERE id = :user_id ORDER BY Timestamp ASC",
                              user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":

        # Get name, price and symbol via lookup
        dictionary = lookup(request.form.get("symbol"))

        # Redirect user to a new page
        return render_template("quoted.html",
               name=dictionary["name"], price=dictionary["price"], symbol=dictionary["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST
    if request.method == "POST":

        # Assign username into memory
        username = request.form.get("username")

        # Assign password
        password = request.form.get("password")

        # Ensure username was provided
        if not username:
            return apology("must provide username", 403)

        # Ensure username not exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        if rows:
            return apology("username already exists", 403)

        # Ensure password was provided
        elif not password:
            return apology("must provide password", 403)

        # Ensure password not exists
        password_hash = generate_password_hash(request.form.get("password"))

        rows = db.execute("SELECT * FROM users WHERE hash = :password",
                          password=password_hash)

        if rows:
            return apology("password already exists", 403)

        # Ensure passwords provided were same
        elif password != request.form.get("confirmation"):
            return apology("not the same passwords", 403)

        # Insert into database
        db.execute("INSERT INTO users (username, hash, cash) VALUES (:username, :password, :cash)",
                   username=username, password=password_hash, cash=10000.00)

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Get all the histories
    purchases = db.execute("SELECT symbol, SUM(shares) FROM purchase WHERE id = :user_id GROUP BY symbol",
                           user_id=session["user_id"])

    if request.method == "POST":

        # Ensure symbol was selected
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 403)

        # Ensure shares was integer
        try:
            float(request.form.get("shares"))

            if not float(request.form.get("shares")).is_integer():
                return apology("must provide integer", 403)
        except ValueError:
            return apology("invalid shares", 403)

        # Ensure shares was positive
        if float(request.form.get("shares")) <= 0.00:
            return apology("must provide positive shares", 403)

        # Ensure user has enough shares
        for i in range(len(purchases)):
            if purchases[i]["symbol"] == request.form.get("symbol"):
                shares = purchases[i]["SUM(shares)"]
                break
        if float(request.form.get("shares")) > shares:
            return apology("must have enough shares", 403)

        # Ensure the current price
        current_price = lookup(request.form.get("symbol"))["price"]
        price = current_price * float(request.form.get("shares"))

        # Record in purchase table
        db.execute("INSERT INTO purchase (id, symbol, price, shares, 'purchase/sale') VALUES (:user_id, :symbol, :price, :shares, 'sale')",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), price=price, shares=float(request.form.get("shares")))

        # Update in user table
        value = db.execute("SELECT cash FROM users WHERE id = :user_id",
                           user_id=session["user_id"])[0]["cash"] + price
        db.execute("UPDATE users SET cash = :value WHERE id = :user_id",
                   value=value, user_id=session["user_id"])

        return redirect("/")

    else:

        # Ensure user has shares of the symbol
        symbols = []

        for i in range(len(purchases)):
            if purchases[i]["SUM(shares)"] <= 0:
                del purchases[i]
            else:
                symbols.append(purchases[i]["symbol"])

        return render_template("sell.html", symbols=symbols)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
