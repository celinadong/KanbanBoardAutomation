import requests
import json

token = "407d5ce13b882270fcb7763569f7444b28a2f93d"
gh_user = "VaniOFX"
gh_repo = "GlobalHackathon"
gh_project_id = 2841438
gh_column_id = 5768952
gh_card_id = 23293878
default_location = "Others"
accept = "application/vnd.github.inertia-preview+json"
header = {
    "Accept":accept,
    "Authorization": "token {}".format(token)
}

api_repo_projects = "https://api.github.com/repos/{}/{}/projects"
api_get_project = "https://api.github.com/projects/{}"
api_get_column = "https://api.github.com/projects/columns/{}"
api_get_card = "https://api.github.com/projects/columns/cards/{}"

def get_repo_projects(user, repo):
    response = requests.get(api_repo_projects.format(user, repo), headers=header)
    for project in response.json():
        print(project["id"], project["name"])
    return response.json()
    # TODO: more sanitisation

def get_project_by_id(id):
    response = requests.get(api_get_project.format(id), headers=header)
    return response.json() 

def create_project(name, user, repo, description=""):
    payload = {
        "name": name,
        description: description
    }
    response = requests.post(api_repo_projects.format(user, repo), headers=header, data=json.dumps(payload))
    return response.json()

def get_columns(project_id):
    response = requests.get(api_get_project.format(project_id) + "/columns", headers=header)
    for column in response.json():
        print(column["id"], column["name"])
    return response.json()

def create_column(name, project_id):
    payload = {
        "name": name
    }
    response = requests.post(api_get_project.format(project_id) + "/columns", headers=header, data=json.dumps(payload))
    print(response.json())
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()["id"]


def edit_column_name(name, column_id):
    payload = {
        "name": name
    }
    response = requests.patch(api_get_column.format(column_id), data=json.dumps(payload), headers=header)

    return response.json()

def get_cards(column_id):
    response = requests.get(api_get_column.format(column_id) + "/cards", headers=header)
    return response.json()

def get_cards_by_url(url):
    response = requests.get(url, headers=header)
    return response.json()


def create_card(note, column_id):
    payload = {
        "note": note
    }
    response = requests.post(api_get_column.format(column_id) + "/cards", headers=header, data=json.dumps(payload))
    print(response.json())
    if response.status_code != 200:
        response.raise_for_status()

def edit_card_note(note, card_id):
    payload = {
        "note": note
    }
    response = requests.patch(api_get_card.format(card_id), data=json.dumps(payload), headers=header)

    return response.json()

def update_card_by_id(project_id, card_id, note, column_name=None):
    if column_name is None:
        column_name = default_location
    
    columns = get_columns(project_id)
    for column in columns:
        for card in get_cards_by_url(column["cards_url"]):
            if (card["id"] == card_id):
                print("yes")
                edit_card_note(note, card_id)
                return

    # By default, put it in "To do"
    for column in columns:
        if column["name"] == column_name:
            create_card(note, column["id"])
            return
    
    column_id = create_column(column_name, project_id)
    create_card(note, column_id)
