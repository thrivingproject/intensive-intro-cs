import os
import time as t

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # Get user ID to query database for cash balance and current holdings
    user = session['user_id']

    # Get user's cash balance and stock portfolio to display in HTML
    cash = db.execute('SELECT cash FROM users WHERE id = ?', user)[0]['cash']
    nav = cash  # Net asset value

    stocks = db.execute(
        'SELECT symbol, SUM(shares) AS shares_owned'
        ' FROM history'
        ' WHERE user_id = ?'
        ' GROUP BY symbol'
        ' HAVING shares_owned > 0',
        user
    )

    # Iterate through stocks in portfolio to update NAV and get position info
    for stock in stocks:
        iex_api_quote = lookup(stock['symbol'])
        price = iex_api_quote['price']

        position_value = price * stock['shares_owned']
        nav += position_value

        stock['name'] = iex_api_quote['name']  # Company's name
        stock['price'] = price  # Current market price
        stock['position_value'] = position_value  # Current position value

    return render_template(
        "biz/index.html", stocks=stocks, cash=cash, nav=nav)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Handle GET request
    if request.method == 'GET':
        return render_template("biz/buy.html")

    # Validate form data because user reached route via POST
    symbol = request.form.get('symbol')
    buy_qty = request.form.get('shares')
    error = None

    if not symbol:
        error = 'Missing ticker symbol.'
    elif not buy_qty:
        error = "Missing share quantity"
    elif buy_qty.isnumeric() is False:
        error = 'Share quantity must be a natural number.'
    else:
        buy_qty = float(buy_qty)
        try:
            iex_api_quote = lookup(symbol)
            symbol = iex_api_quote['symbol']
        except TypeError:
            error = 'Ticker symbol invalid.'
    if error:
        return apology(error)

    # Get transaction info since data is valid
    user = session['user_id']
    price = float(iex_api_quote['price'])
    cost = price * buy_qty
    time = t.time()

    # Check user's balance to see if capital requirement is met
    cash = db.execute('SELECT cash FROM users WHERE id = ?', user)[0]['cash']
    cash -= cost
    if cash < 0:
        return apology('Insufficient funds.')

    # Update user's balance and record transaction
    db.execute(
        'UPDATE users'
        '   SET CASH = ?'
        ' WHERE id = ?',
        cash, user
    )

    db.execute(
        'INSERT INTO history'
        '(user_id, symbol, shares, price, time)'
        ' VALUES (?, ?, ?, ?, ?)',
        user, symbol, buy_qty, price, time
    )

    # Return to index since transaction is complete
    return redirect("/")


@app.route("/history")
@login_required
def history():
    # Get user's transaction history to load into HTML
    user_history = db.execute(
        "SELECT symbol, shares, price, datetime(time, 'unixepoch') AS time"
        ' FROM history'
        ' WHERE user_id = ?'
        ' ORDER BY time DESC',
        session['user_id']
    )

    return render_template("biz/history.html", user_history=user_history)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("auth/login.html")


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
    if request.method == 'GET':
        return render_template("biz/quote.html")

    # User reached route via POST
    symbol = request.form.get('symbol')
    if not symbol or symbol.isalpha() is False:
        return apology("Enter ticker symbol")

    # Catch invalid symbol
    try:
        iex_api_quote = lookup(symbol)
        return render_template(
            'biz/quoted.html', iex_api_quote=iex_api_quote)
    except TypeError:
        return apology("Invalid ticker symbol")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        # Validate form data
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Passwords must match.'
        if error:
            return apology(error)

        # Try to enter user info into database since data is valid
        try:  # Make sure username doesn't already exist
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, generate_password_hash(password),
            )
        except ValueError:
            return apology("Username already exists")

        # Return to login page since registration successful
        return redirect("/login")

    # Load registration form since user arrivaed via GET
    return render_template('auth/register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Get user info
    user_id = session['user_id']
    stocks = db.execute(
        'SELECT symbol, SUM(shares) AS shares_owned'
        ' FROM history'
        ' WHERE user_id = ?'
        ' GROUP BY symbol'
        ' HAVING shares_owned > 0',
        user_id
    )

    if request.method == 'GET':
        return render_template("biz/sell.html", stocks=stocks)

    # Handle POST request and validate data
    sell_symbol = request.form.get('symbol')
    sell_qty = request.form.get('shares')
    error = None

    if not sell_symbol:
        error = "Please enter symbol."
    elif not sell_qty:
        error = "Please enter amount of shares to sell."
    else:
        sell_qty = int(sell_qty)

        if sell_qty < 0:
            error = "Amount of shares to sell must be non-negative."
        else:  # Check if user owns stock they're trying to sell
            # Assign shares_avail otherwise user can force symbol via HTML form
            shares_avail = None
            for stock in stocks:
                if stock['symbol'] == sell_symbol:
                    shares_avail = stock['shares_owned']  # Num shares owned
                    break  # Break once ownership is verified

            if not shares_avail:
                error = "You do not own that stock"
            elif sell_qty > shares_avail:
                error = "You don't own that many shares."

    # Return error if data is invalid
    if error:
        return apology(error)

    # Add transaction to history and update cash balance
    iex_api_quote = lookup(sell_symbol)
    price = iex_api_quote['price']
    time = t.time()

    db.execute(
        'INSERT INTO history'
        '(user_id, symbol, shares, price, time)'
        ' VALUES (?, ?, ?, ?, ?)',
        user_id, sell_symbol, -sell_qty, price, time
    )

    cash = db.execute(
        'SELECT cash FROM users WHERE id = ?',
        user_id
    )[0]['cash']

    updated_bal = cash + price * sell_qty

    db.execute(
        'UPDATE users'
        '   SET CASH = ?'
        ' WHERE id = ?',
        updated_bal, user_id
    )

    return redirect("/")
