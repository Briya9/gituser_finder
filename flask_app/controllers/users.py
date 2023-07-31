from flask import request, render_template, jsonify
from flask_app import app
import requests



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods = ["POST"])
def search_git_api():
    github_api_base_url = "http://api.github.com"

    lower_case_name = request.form["name"].lower()
    user_url = f"{github_api_base_url}/users/{lower_case_name}"
    user_response = requests.get(user_url)

    repos_url = f"{github_api_base_url}/users/{lower_case_name}/repos"
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

        repo_names_url = [{"name": repo['name'], "html_url" : repo['html_url']}for repo in repos_data] 
        
        return render_template("user.html", base_info = user_info, repos_info = repo_names_url)
        
    else:
        return jsonify({"message : Failed to fetch data from Githunb API"}), 500
    
    






































