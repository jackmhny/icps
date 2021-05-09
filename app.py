from flask import Flask, request, render_template
from balance2 import *

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        reactants = request.form["reactants"]
        products = request.form["products"]
        result = run(reactants, products)
        return render_template("base.html", result=result)
    return render_template("base.html", )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port="5001"
    )