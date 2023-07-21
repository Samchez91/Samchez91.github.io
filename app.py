#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 09:58:26 2023

@author: samuelschick
"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# This will store the invited participants and their selected time slots
invited_participants = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        invited_participant = request.form['invited_participant']
        available_times = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            available_times[day] = request.form.getlist(f'available_times_{day}')

        invited_participants[invited_participant] = available_times

        return redirect(url_for('thanks'))

    return render_template('index.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html', participants=invited_participants)


@app.route('/available_times')
def available_times():
    common_available_times = {}
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        common_available_times[day] = list(set.intersection(*[set(participant[day]) for participant in invited_participants.values()]))

    return render_template('available_times.html', common_times=common_available_times)


if __name__ == '__main__':
    app.run(debug=True)
