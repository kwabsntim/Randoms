from flask import Flask, render_template, send_from_directory
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


@app.route('/sw.js')
def sw():
    response = send_from_directory(app.static_folder, 'sw.js')
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response


if __name__ == '__main__':
    app.run(debug=True)