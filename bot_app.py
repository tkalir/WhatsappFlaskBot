#!/usr/bin/env python

import os
from app_and_db import app, db
from flask import request, make_response

class bot_app:
    def __init__(self):
        pass

    def after_webhook_notification(self, func):
        self.after_webhook_notification = func

@app.route('/webhook', methods=['POST'])
def recieve_message():
    return make_response("", 200)
