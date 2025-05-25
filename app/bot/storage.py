from redis import Redis, exceptions

try:
    redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("Успешно подключились к Redis!")
except exceptions.ConnectionError as e:
    print(f"Ошибка подключения к Redis: {e}")
    exit()


class RedisStateStorage:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_state(self, chat_id):
        return self.redis.get(f'state_{chat_id}')

    def set_state(self, chat_id, state):
        self.redis.set(f'state_{chat_id}', state)

    def delete_state(self, chat_id):
        self.redis.delete(f'state_{chat_id}')


storage = RedisStateStorage(redis_client=redis_client)


