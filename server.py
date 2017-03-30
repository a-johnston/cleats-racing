#!/usr/bin/env python3
from flask import Flask, render_template
from flask_shelve import get_shelve, init_app


settings = {
    'SHELVE_FILENAME':'points',
}

app = Flask(__name__)
app.config.update(settings)

init_app(app)


@app.route('/')
def index():
    points_dict = get_shelve('r')
    return render_template('index.html')


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if __name__ == '__main__':
    app.run()
