#!/usr/bin/env python

import os
from app_and_db import app, db
from flask import request, make_response
from bot_app import bot_app

bot = bot_app()
bot.after_webhook_notification(lambda notification: print(notification.json))