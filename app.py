from flask import Flask,render_template

from trackSpending import chooseUser


app = Flask(__name__)

@app.route('/')
def getUser():
    ids=chooseUser()

    return render_template('index.html',value=ids)

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
