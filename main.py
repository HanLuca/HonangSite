import os

from flask import Flask, redirect, url_for, render_template, request, session
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from _dataReceiver import DataReceiver

from zenora import APIClient
from config import TOKEN, CLIENT_SECRET, REDIRECT_URI, OAUTH_URI

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(TOKEN, client_secret = CLIENT_SECRET)

@app.route("/")
def home():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer = True)
        current_user = bearer_client.users.get_current_user()
        if DataReceiver.check(current_user.id) == True:
            #! User Account Info !#
            userAccountB = ["2_Coin", "3_Exp", "4_Level", "5_Time"]; userAccount = []
            for i in range(0, len(userAccountB)):   
                userAccount.append(DataReceiver.get(f"USERDATA/{current_user.id}", f"{userAccountB[i]}"))

            return render_template("userInfo.html", current_user = current_user, account = userAccount) 

        else: return render_template("userInfo.html", current_user = current_user, error = False) 

    return render_template("userInfo.html", oauth_uri = OAUTH_URI)

@app.route("/oauth/callback")
def callback():
    code = request.args["code"] 
    access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
    session["token"] = access_token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)