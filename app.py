from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///final.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route("/home", methods=["GET", "POST"])
def index():
    print("********************************************************************************************************")
    print(session.get("user_id"))
    breakpoint()
    if session.get("user_id"):
        if request.method == "POST":
            journal_entry = request.form.get("journal")
            db.execute("INSERT INTO JournalEntry (journal_entry) VALUES (:journal)",
                    journal=journal_entry)
            return redirect("/home")
        else:
            rows = db.execute("SELECT * FROM JournalEntry WHERE user_id = :user_id", user_id=session["user_id"])
            return render_template("home.html", rows=rows)
    else:
        print("USER NOT LOGGED IN")
        return redirect("/login")


@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        rows = db.execute("SELECT * FROM User WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists", 400)

        db.execute("INSERT INTO User (username, password) VALUES(?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM User WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/home")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        breakpoint()
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)


        rows = db.execute("SELECT * FROM User WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]


        return redirect("/home")
    else:
        return render_template("login.html")


