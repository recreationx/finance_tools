from flask import Flask, request, render_template, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

data = []

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/dedup/", methods=["GET", "POST"])
def dedup():
    global data
    if request.method == "POST":
        if "clear" in request.form:
            data = []
            return render_template("dedup.html", data=data)

        if request.form["item"] and request.form["supplier"] and request.form["quantity"]:
            item = request.form["item"]
            supplier = request.form["supplier"]
            quantity = int(request.form["quantity"])
            for i in data:
                if item == i[0] and supplier != i[1]:
                    print("wrong")
                    return render_template("dedup.html",data=data, alert=f"Item not added, conflict between suppliers {supplier} and {i[1]}")
                if item == i[0] and supplier == i[1]:
                    data.remove(i)
                    new_quantity = quantity + i[2]
                    data.append([item, supplier, new_quantity])
                    return render_template("dedup.html",data=data, alert=f"Item code with same supplier exist. New quantity is {new_quantity}.")
            data.append([item, supplier, quantity])
    return render_template("dedup.html", data=data)

app.run()