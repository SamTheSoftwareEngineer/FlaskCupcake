"""Flask app for Cupcakes"""
from flask import Flask, request,  render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = 'secret'

connect_db(app)

@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")

@app.route("/api/cupcakes")
def cupcake_list():
    """Returns a serialized list of all cupcakes in system."""
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about the new cupcake."""
    data = request.json
    
    cupcake = Cupcake(
        flavor=data["flavor"],
        rating=data["rating"],
        size=data["size"],
        image=data["image"] or None
    )

    """Add this cupcake to the database."""
    db.session.add(cupcake)
    db.session.commit()
    
    #POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Returns a serialized cupcake object."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods =["PATCH"])
def update_cupcake_info(cupcake_id):
    """Update cupcake info and return updated cupcake."""
    data = request.json
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data["flavor"]
    cupcake.rating = data["rating"]
    cupcake.size = data["size"]
    cupcake.image = data["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted cupcake.")