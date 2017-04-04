#!/usr/bin/env python3
from flask import Flask, abort, render_template, redirect
from functools import lru_cache

from data_churner import *
from config import SITE_TITLE, EVENT_TITLE


_flags = {
    'gc': '/static/Jersey_yellow.png',
    'kom': '/static/Jersey_polkadot.png',
    'qom': '/static/Jersey_polkadot.png',
    'sprint': '/static/Jersey_green.png',
}


app = Flask(__name__)


@lru_cache()
def get_raw_results():
    return parse_data()


@lru_cache()
def get_results(nmax=5):
    data = get_raw_results()
    results = compute_all_ride_results(*data, nmax)
    overall = compute_overall_totals(results, nmax)

    return data, results, overall


@app.route('/')
def index():
    data, results, overall = get_results(5)
    return render_template(
        'index.html',
        overall=overall,
        stages=results,
        flags=_flags,
        site_title=SITE_TITLE,
        event_title=EVENT_TITLE,
    )


@app.route('/stage/<int:stage_id>')
def stage(stage_id):
    data, results, overall = get_results(3)
    for stage in results:
        if stage[0].id == stage_id:
            return render_template(
                'stage.html',
                stage=stage[0],
                intermediate=stage[1],
                totals=stage[2],
                flags=_flags,
                site_title=SITE_TITLE,
                event_title=EVENT_TITLE,
            )
    abort(404)


@app.route('/reload')
def reload():
    # this is *super bad*. Ideally would at least hold up this request while
    # loading new data rather than hold up a random request in between this
    # and the redirect resolution
    get_raw_results.cache_clear()
    get_results.cache_clear()
    return redirect('/', code=302)


@app.errorhandler(404)
@app.errorhandler(500)
def error(err):
    return 'not a page :('
