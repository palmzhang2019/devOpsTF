import os
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()

trello_label_dict = {
    "Normal": "663330a81dc51400ebc08252",
    "Bug": "664eebceb77c4d0ccfcdda96",
    "Question": "664eec26c9a86dadf672875c",
    "High": "663330a81dc51400ebc0824c",
    "Enhancement": "664eebf858412765b6899b92",
    "Low": "663330a81dc51400ebc08250"
}

forgejo_label_dict = {
    "Bug": 1,
    "Enhancement": 3,
    "Question": 6,
    "High": 10,
    "Normal": 9,
    "Low": 8
}

label_dict = {
    trello_label_dict["Normal"]: forgejo_label_dict["Normal"],
    trello_label_dict["Low"]: forgejo_label_dict["Low"],
    trello_label_dict["High"]: forgejo_label_dict["High"],
    trello_label_dict["Question"]: forgejo_label_dict["Question"],
    trello_label_dict["Enhancement"]: forgejo_label_dict["Enhancement"],
    trello_label_dict["Bug"]: forgejo_label_dict["Bug"],
}

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
LIST_ID = os.getenv("LIST_ID")
FORGEJO_ACCESS_TOKEN = os.getenv("FORGEJO_ACCESS_TOKEN")

# 配置常量

OWNER = "devPalmOps"
REPO = "helloworld"
BASE_URL = "http://localhost:3000/api/v1"
FORGEJO_URL = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"
TRELLO_URL = f"https://api.trello.com/1/cards?key={TRELLO_KEY}&token={TRELLO_TOKEN}&idList={LIST_ID}"

HEADERS = {'Authorization': f'Bearer {FORGEJO_ACCESS_TOKEN}'}

CARD_INFO_URL = "https://api.trello.com/1/cards/{short_link}?key={TRELLO_KEY}&token={TRELLO_TOKEN}"

CARD_MEMBERS_URL = "https://api.trello.com/1/cards/{card_id}/members?key={TRELLO_KEY}&token={TRELLO_TOKEN}"

PATCH_ISSUE_URL = "{BASE_URL}/repos/{OWNER}/{REPO}/issues/{index}"

CARD_CHECKLIST_URL = "https://api.trello.com/1/cards/{card_id}/checklists?key={TRELLO_KEY}&token={TRELLO_TOKEN}"

FORGEJO_LABEL_URL = "{BASE_URL}/repos/{OWNER}/{REPO}/issues/{index}/labels"

FORGEJO_ATTACHMENT_URL = "{BASE_URL}/repos/{OWNER}/{REPO}/issues/{issue_index}/assets"

TRELLO_MEMBER_URL  = "https://api.trello.com/1/members/{id}?key={TRELLO_KEY}&token={TRELLO_TOKEN}"

design_user_list = ['designpalm']

dev_user_list = ['devpalm', 'devpalm2']

review_user_list = ['reviewpalm']

test_user_list = ['testpalm1']

leader_user_list = ['palmleader']

MEMO_LIST = "メモ"
IDEA_LIST = '思い出す'
DESIGN_LIST = '設計中'
DEV_LIST = 'コーディング'
REVIEW_LIST = 'Review'
TEST_LIST = 'テスト'
RECODE_LIST = '改修必要'
DONE = '完了'