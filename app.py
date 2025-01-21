from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import json

app = Flask(__name__)
app.secret_key = "secret_key"

# Load users data
try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# Save users data
def save_users():
    with open("users.json", "w") as file:
        json.dump(users, file)

# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("game"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("game"))
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Username already exists. Please choose another.", "error")
        else:
            users[username] = password
            save_users()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if "username" not in session:
        return redirect(url_for("login"))
    
    result = None
    if request.method == "POST":
        choices = ["rock", "paper", "scissors"]
        user_choice = request.form["choice"]
        computer_choice = random.choice(choices)
        if user_choice == computer_choice:
            result = "It's a draw!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"
        return render_template("game.html", user_choice=user_choice, computer_choice=computer_choice, result=result)
    
    return render_template("game.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
