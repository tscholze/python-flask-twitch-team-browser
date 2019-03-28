from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/meep")
def meep():
    return render_template("meep.html")

if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)