from flask import request, render_template, jsonify
from flask_app import app
import requests
from datetime import date


datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


@app.route("/")
def index():
    return render_template("index.html", datetoday = datetoday ,datetoday2 = datetoday2)


@app.route("/home", methods=["GET", "POST"])
def users_finder():
        user_url = f"http://api.github.com/search/users?q={request.form['name']}"
        response = requests.get(user_url)
        if response.status_code == 200:
            users_data =  response.json().get("items", [])
            # print(users_data)
            return render_template( "index.html", data =  users_data)
        else:
            return jsonify({"message : Failed to fetch data from Githunb API"}), 500


@app.route("/search", methods = ["GET"])
def search_git_api():
    github_api_base_url = "http://api.github.com"

    if request.method == "GET":
        user_name = request.args.get('username')

        user_url = f"{github_api_base_url}/users/{user_name}"
        user_response = requests.get(user_url)

        repos_url = f"{github_api_base_url}/users/{user_name}/repos"
        repos_response =  requests.get(repos_url)

        if user_response.status_code == 200 and repos_response.status_code == 200: 
            user_data = user_response.json()
            repos_data = repos_response.json()

            user_info = {
                "avatar_url": user_data["avatar_url"],
                "name": user_data["name"],
                "bio": user_data["bio"],
                "location": user_data["location"],
                "following": user_data["following"],
                "followers": user_data["followers"],
                "public_repos": user_data["public_repos"],
                "blog": user_data["blog"],
                "html_url": user_data["html_url"],
            }

            repo_info = []
            for repo in repos_data:
                repo_info.append({
                    "name": repo["name"],
                    "html_url": repo["html_url"]
                })
                
            return render_template("user.html", base_info = user_info, repos_info = repo_info)
        
        else:
            return "message : Failed to fetch data from Githunb API", 500
        
    return redirect("/user")


































