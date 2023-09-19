import datetime
from pymongo import MongoClient
from flask import Flask,render_template,request

def create_app():
    app=Flask(__name__)
    entries=[]

    @app.route("/login",methods=["GET","POST"])
    def login():
        if request.method=="POST":
            entry_content=request.form.get("content")
            format_date=datetime.datetime.today().strftime("%Y-%M-%d")
            entries.append((entry_content))
        return render_template('Login.html',entries=entries)

    @app.route("/signup")
    def sign_in():
        return render_template('sign_in.html')

    client = MongoClient("mongodb+srv://anupam-shukla:<shuklaanupam>@cluster0.hugp9.mongodb.net/?retryWrites=true&w=majority")   
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return app

