from fastapi import APIRouter, Request
from utils import make_trello_request, handle_create_card, handle_update_card, \
    get_card_id_by_short_link, update_members, update_checklist, put_file_to_issue, \
    drop_issue
from config import TRELLO_URL


router = APIRouter()

@router.post("/add-card-by-webhook/")
async def receive_webhook(request: Request):
    webhook_data = await request.json()
    if webhook_data.get('action') != "edited":
        return False

    issue_title = webhook_data.get('pull_request', {}).get('title', 'No title provided')
    issue_body = webhook_data.get('pull_request', {}).get('body', 'No body provided')

    data = {
        "name": issue_title,
        "desc": issue_body,
        "pos": "top",
    }

    response = make_trello_request("POST", TRELLO_URL, data=data)
    return {"status": "success", "data": response}

@router.post("/test/")
async def receive_test(request: Request):
    body = await request.json()
    action = body.get('action', 'No action provided')
    issue_title = body.get('issue', {}).get('title', 'No title provided')
    issue_body = body.get('issue', {}).get('body', 'No body provided')
    return {"status": "success", "data": {}}

@router.api_route("/trello-webhook/", methods=["POST", "HEAD"])
async def trello_webhook(request: Request):
    if request.method == "POST":
        webhook_data = await request.json()
        if 'custom-action' in webhook_data.keys():
            card_id, card_content = get_card_id_by_short_link(webhook_data.get('card_id'))
            update_members(card_id)
            update_checklist(card_id, card_content)
        action_type = webhook_data.get('action', {}).get('type', '')
        data = webhook_data.get('action', {}).get('data', {})
        card_id = data.get('card', {}).get('id', '')
        if action_type == 'createCard':
            return handle_create_card(data, card_id)
        elif action_type == 'updateCard':
            if "listBefore" in data:
                user_id = data["action"]["idMemberCreator"]
            return handle_update_card(data, card_id)
        elif action_type == "addAttachmentToCard":
            attachment = data.get("attachment", "")
            put_file_to_issue(card_id, attachment)
        elif action_type == "deleteCard":
            drop_issue(card_id)
        else:
            print(action_type)
    elif request.method == "HEAD":
        return {"status": "OK"}
