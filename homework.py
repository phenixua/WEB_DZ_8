from typing import List, Any, Dict

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> List[str | None]:
    print(f"Find by tag: {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> Dict[str, List[Any]]:
    print(f"Find by author: {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def process_command(command: str) -> None:
    parts = command.split(':')
    if len(parts) == 1 and parts[0].strip().lower() == 'exit':
        print("Exiting the script.")
        exit()

    if len(parts) != 2:
        print("Invalid command format. Please use 'name:', 'tag:', 'tags:', or 'exit'")
        return

    action, value = parts[0].strip().lower(), parts[1].strip()

    if action == 'name':
        result = find_by_author(value)
    elif action == 'tag':
        result = find_by_tag(value)
    elif action == 'tags':
        tags = value.split(',')
        result = {}
        for tag in tags:
            tag_result = find_by_tag(tag)
            result[tag] = tag_result
    else:
        print("Invalid action. Please use 'name:', 'tag:', 'tags:', or 'exit'")
        return

    print("Result:")
    print(result)


if __name__ == '__main__':
    while True:
        user_input = input("Enter a command: ")
        process_command(user_input)
