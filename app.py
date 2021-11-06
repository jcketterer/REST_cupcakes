"""Flask app for Cupcakes"""
from flask import Flask, json, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "donttellemmorty"

connect_db(app)
db.create_all()


@app.route("/")
def index():
    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)


@app.route("/api/cupcakes")
def list_cupcakes():
    cupcake = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcake)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    cupcake = Cupcake(
        flavor=request.json["flavor"],
        rating=request.json["rating"],
        size=request.json["size"],
        image=request.json["image"] or None,
    )

    db.session.add(cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.query(Cupcake).filter_by(id=id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Bye Bye Cupcake Deleted")
