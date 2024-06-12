import requests
import io
from config import label_dict, TRELLO_KEY, TRELLO_TOKEN, BASE_URL, FORGEJO_LABEL_URL,\
 FORGEJO_URL, HEADERS, OWNER, REPO, CARD_INFO_URL, CARD_MEMBERS_URL, PATCH_ISSUE_URL, \
    FORGEJO_ATTACHMENT_URL, CARD_CHECKLIST_URL
from redis_server import store_card_url, get_forgejo_id_by_card_id, delete_card_id


# 工具函数
def get_trello_api_url(endpoint):
    return f"https://api.trello.com/1/{endpoint}?key={TRELLO_KEY}&token={TRELLO_TOKEN}"


def make_forgejo_request(method, url, **kwargs):
    response = requests.request(method, url, headers=HEADERS, **kwargs)
    if response.status_code in [200, 201]:
        return response.json()
    response.raise_for_status()


def make_trello_request(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()


def handle_create_card(data, card_id):
    card_name = data.get('card', {}).get("name", "")
    payload = {'title': card_name}
    response = make_forgejo_request("POST", FORGEJO_URL, json=payload)
    store_card_url(card_id, response.get('id'))
    return {"status": "success", "data": response}


def handle_update_card(data, card_id):
    api_url = get_url_from_card_id(card_id)
    old_body = data.get("old", {})
    for key, value in old_body.items():
        new_value = data.get("card", {}).get(key, "")
        payload_key = map_key_to_payload_key(key)
        if payload_key:
            if payload_key == "labels":
                add_label_to_issue(new_value, card_id)
            else:
                payload = {payload_key: new_value}
                response = make_forgejo_request("PATCH", api_url, json=payload)
    return {"status": "success"}


def map_key_to_payload_key(key):
    key_mapping = {
        "name": "title",
        "desc": "body",
        "idLabels": "labels",
        "due": "due_date"
    }
    return key_mapping.get(key)


def get_url_from_card_id(card_id):
    forgejo_id = get_forgejo_id_by_card_id(card_id)
    return f"{BASE_URL}/repos/{OWNER}/{REPO}/issues/{forgejo_id}"


def add_label_to_issue(label_id_list, card_id):
    index = get_forgejo_id_by_card_id(card_id)
    api_url = FORGEJO_LABEL_URL.format(BASE_URL=BASE_URL, OWNER=OWNER, REPO=REPO, index=index)
    forgejo_label_id_list = [label_dict[label_id] for label_id in label_id_list]

    payload = {
        "labels": forgejo_label_id_list
    }
    response = make_forgejo_request("PUT", api_url, json=payload)
    return {"status": "success", "data": response}


def put_file_to_issue(card_id, attachment):
    if not attachment:
        return {"status": "error", "message": "No attachment provided"}

    issue_index = get_forgejo_id_by_card_id(card_id)
    api_url = FORGEJO_ATTACHMENT_URL.format(BASE_URL=BASE_URL, OWNER=OWNER, REPO=REPO, issue_index=issue_index)
    attachment_url = attachment.get("url", "")
    attachment_name = attachment.get("name", "")
    headers = {
        'Authorization': f'OAuth oauth_consumer_key="{TRELLO_KEY}", oauth_token="{TRELLO_TOKEN}"'
    }

    response = requests.get(attachment_url, headers=headers)
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to download attachment: {response.text}"}

    attachment_content = io.BytesIO(response.content)
    files = {'attachment': (attachment_name, attachment_content)}

    response = make_forgejo_request("POST", api_url, files=files)
    return {"status": "success", "data": response}

def get_card_id_by_short_link(short_link):
    url = CARD_INFO_URL.format(short_link=short_link, TRELLO_KEY=TRELLO_KEY, TRELLO_TOKEN=TRELLO_TOKEN)
    data = make_trello_request("GET", url)
    return data.get('id', ''), data.get('desc')

def update_members(card_id):
    url = CARD_MEMBERS_URL.format(card_id=card_id, TRELLO_KEY=TRELLO_KEY, TRELLO_TOKEN=TRELLO_TOKEN)
    data = make_trello_request("GET", url)
    full_names = [member["fullName"] for member in data]
    full_names = ["palmleader" if x == "PalmZhang" else x for x in full_names]
    issue_index = get_forgejo_id_by_card_id(card_id)
    forgego_api = PATCH_ISSUE_URL.format(BASE_URL=BASE_URL, OWNER=OWNER, REPO=REPO, index=issue_index)
    forgego_data = make_forgejo_request("PATCH", forgego_api, json={"assignees":full_names})
    return forgego_data

def update_checklist(card_id, card_content):
    url = CARD_CHECKLIST_URL.format(card_id=card_id, TRELLO_KEY=TRELLO_KEY, TRELLO_TOKEN=TRELLO_TOKEN)
    checklists = make_trello_request("GET", url)
    checklist_markdown = ''
    for checklist in checklists:
        checklist_markdown += f"### {checklist['name']}\n"
        for item in checklist['checkItems']:
            state = '[x]' if item['state'] == 'complete' else '[ ]'
            checklist_markdown += f"- {state} {item['name']}\n"

    update_content = card_content + '\n' + checklist_markdown
    forgejo_api = get_url_from_card_id(card_id) 
    payload = {'body': update_content}
    result = make_forgejo_request("PATCH", forgejo_api, json=payload)
    print(result)


def drop_issue(card_id):
    forgejo_api = get_url_from_card_id(card_id)
    result = make_forgejo_request("DELETE", forgejo_api)
    delete_card_id(card_id)
    print(result)
