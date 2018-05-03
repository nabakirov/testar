from testar import app
from flask import render_template


@app.route('/')
def index_template():
    return render_template("index.html")