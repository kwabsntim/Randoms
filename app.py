from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/ping')
def ping():
    return 'pong', 200


if __name__ == '__main__':
    app.run(debug=True)