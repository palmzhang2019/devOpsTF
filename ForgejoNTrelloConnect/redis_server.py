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
    存储或更新角色和用户信息到一个名为 'roles' 的 Redis 键中
    """
    # 将整个 roles_users 列表转换为 JSON 字符串
    roles_users_json = json.dumps(roles_users)
    
    # 将 JSON 字符串存储在名为 'roles' 的 Redis 键中
    r.set('roles', roles_users_json)
    print("Stored or updated roles with users information")

def get_roles_users():
    """
    从 Redis 中获取所有角色和用户信息
    """
    roles_users_json = r.get('roles')
    if roles_users_json:
        roles_users = json.loads(roles_users_json)
        return roles_users
    return None