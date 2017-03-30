#!/usr/bin/env python3
from flask import Flask, render_template
from functools import lru_cache
from data_churner import *


app = Flask(__name__)


@app.route('/')
@lru_cache(maxsize=None)
def index():
    data = parse_data()
    results = compute_all_ride_results(*data)
    overall = compute_overall_totals(results)

    return render_template('index.html', overall=overall)


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if __name__ == '__main__':
    app.run()
