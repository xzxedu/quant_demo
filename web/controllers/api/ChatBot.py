## chatterbot
from flask import Flask, render_template, request
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from web.controllers.api import route_api
from chatterbot import ChatBot
from application import app,db

bot = ChatBot("weixinchatbot")
bot.set_trainer(ListTrainer)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.english")

@route_api.route("/chatbot/index")
def home():
    return render_template("home.html")

@route_api.route("/chatbot/chat")
def get_bot_response():
    userText = (request.values)['msg']
    return str(bot.get_response(userText))