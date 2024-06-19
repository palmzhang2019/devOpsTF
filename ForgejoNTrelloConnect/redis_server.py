import redis
import json

# 连接到 Redis 服务器
r = redis.Redis(host='localhost', port=6379, db=1)


def store_card_url(card_id, forgejo_id):
    """
    将 card_id 和 url 存储在 Redis 中
    """
    r.set(card_id, forgejo_id)
    print(f"Stored card_id: {card_id} with forgejo_id: {forgejo_id}")


def get_forgejo_id_by_card_id(card_id):
    """
    通过 card_id 获取对应的 url
    """
    forgejo_id = r.get(card_id)
    if forgejo_id:
        forgejo_id = forgejo_id.decode('utf-8')
    return forgejo_id


def delete_card_id(card_id):
    """
    从 Redis 中删除指定的 card_id 及其对应的 forgejo_id
    """
    response = r.delete(card_id)
    if response == 1:
        print(f"Deleted card_id: {card_id}")
    else:
        print(f"No record found for card_id: {card_id} to delete")

def store_temp_variable(key, value, ttl=1):
    """
    将 key 和 value 存储在 Redis 的 temp 哈希表中，并设置过期时间
    """
    temp_key = "temp"
    r.hset(temp_key, key, value)
    # 设置 temp 哈希表的过期时间为 ttl 秒
    r.expire(temp_key, ttl)
    print(f"Stored key: {key} with value: {value} in temp with TTL of {ttl} seconds")


def is_temp_variable_exists(key):
    """
    检查 Redis 的 temp 哈希表中是否存在指定的 key
    """
    temp_key = "temp"
    exists = r.hexists(temp_key, key)
    return exists

def store_or_update_roles_users(roles_users):
    """
    存储或更新角色和用户信息
    """
    for role in roles_users:
        title = role["title"]
        users = role["users"]
        for user in users:
            user_id = user["id"]
            user_info = {
                "fullName": user["fullName"],
                "username": user["username"]
            }
            # 将用户信息存储在 Redis 的哈希表中，键名为 "role:{title}"
            r.hset(f"role:{title}", user_id, json.dumps(user_info))
            print(f"Stored or updated user_id: {user_id} with info: {user_info} under role: {title}")

def get_users_by_role(title):
    """
    通过角色标题获取所有用户信息
    """
    users = r.hgetall(f"role:{title}")
    users_info = {}
    for user_id, user_info in users.items():
        users_info[user_id.decode('utf-8')] = json.loads(user_info.decode('utf-8'))
    return users_info
