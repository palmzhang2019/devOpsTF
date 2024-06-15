from fastapi import APIRouter, Request, HTTPException
from utils import make_trello_request, handle_create_card, handle_update_card, \
    get_card_id_by_short_link, update_members, update_checklist, put_file_to_issue, \
    drop_issue, get_member_info, undo_move_if_needed
from config import TRELLO_URL, leader_user_list, dev_user_list, design_user_list, \
    review_user_list, test_user_list, IDEA_LIST, DESIGN_LIST, DEV_LIST, REVIEW_LIST, \
    TEST_LIST, RECODE_LIST, DONE, MEMO_LIST


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
                username = webhook_data.get("action", {}).get("memberCreator", "").get("username", "")
                after_list_name = data.get('listAfter', '').get('name', '')
                before_list_name = data.get('listBefore', '').get('name', '')
                list_id = data.get('old', {}).get('idList', '')
                if before_list_name in [DESIGN_LIST, IDEA_LIST]:
                    allowed_after_lists = [DESIGN_LIST, IDEA_LIST, DEV_LIST, MEMO_LIST]
                    user_lists = leader_user_list + design_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)

                elif before_list_name == DEV_LIST:
                    allowed_after_lists = [REVIEW_LIST]
                    user_lists = leader_user_list + dev_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)

                elif before_list_name == REVIEW_LIST:
                    allowed_after_lists = [TEST_LIST, RECODE_LIST, DONE]
                    user_lists = leader_user_list + review_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)

                elif before_list_name == TEST_LIST:
                    allowed_after_lists = [RECODE_LIST, DONE]
                    user_lists = leader_user_list + test_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)

                elif before_list_name == RECODE_LIST:
                    allowed_after_lists = [DEV_LIST, DESIGN_LIST]
                    user_lists = leader_user_list + design_user_list + dev_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)
                
                elif before_list_name == DONE:
                    allowed_after_lists = [IDEA_LIST, DESIGN_LIST, DEV_LIST, REVIEW_LIST, TEST_LIST, RECODE_LIST]
                    user_lists = leader_user_list
                    undo_move_if_needed(after_list_name, allowed_after_lists, user_lists, card_id, list_id, username)

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
