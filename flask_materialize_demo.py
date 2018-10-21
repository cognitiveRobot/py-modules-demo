from flask import Flask, render_template
from flask_material import Material

app = Flask(__name__)
app.debug = True

Material(app)

@app.route('/')
def index():
    return render_template("materialize.html")


if __name__ == "__main__":
    app.run()
