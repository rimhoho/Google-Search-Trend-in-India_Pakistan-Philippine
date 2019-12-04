from flask import Flask, request, jsonify, render_template, redirect
import pandas as pd
import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://rimho:0000@cluster0-yehww.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['google_search_db']
collections = [db[c] for c in ['2006', '2007', '2008', '2009', '2011']]
documents =  [collection.find() for collection in collections]

app = Flask(__name__)
@app.route("/")
def home():
    products = []
    for document in documents:
        for p in document:
            products.append(p)
    print(products)
    return render_template("googletrends.html", products=products)

# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
