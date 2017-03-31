#!/usr/bin/env python3
from flask import Flask, render_template
from functools import lru_cache
from data_churner import *


app = Flask(__name__)


def add_rankings(l, nmax=5):
    l[0] = (1, *l[0])
    for i in range(1, len(l)):
        l[i] = (l[i-1][0] if l[i][-1] == l[i-1][-1] else i + 1, *l[i])
    l = (l + [('-', '-', '-')] * nmax)[:nmax]
    return l


@app.route('/')
@lru_cache(maxsize=None)
def index():
    data = parse_data()
    results = compute_all_ride_results(*data)
    overall = compute_overall_totals(results)

    for category in overall:
        overall[category] = add_rankings(overall[category])

    return render_template('index.html', overall=overall)


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('


if __name__ == '__main__':
    app.run()
