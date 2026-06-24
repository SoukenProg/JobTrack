from flask import Flask, render_template

app = Flask(__name__)

# モックデータ
stats ={
    "companies": 0,
    "active": 0,
    "interview":0,
    "success":0,
}
@app.route('/')
def top():
    return render_template('index.html',stats=stats)


if __name__ == '__main__':
    app.run()
