import redis

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
