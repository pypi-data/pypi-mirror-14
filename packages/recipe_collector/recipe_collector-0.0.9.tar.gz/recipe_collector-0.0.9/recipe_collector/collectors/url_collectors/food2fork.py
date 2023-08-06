from urllib.parse import urlparse
import requests
from recipe_collector.utils.decorators import coroutine


def get_recipes(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        # TODO: raise better exception
        raise Exception
    data = resp.json()
    return data['recipes']


@coroutine
def food2fork(done, successor=None):
    """
    This coroutine requests a batch of results from a food2fork API url, sending the returned
    title and source_url values to done.

    Args:

    * done: A coroutine that receives a URL from food2fork for further processing
    * successor: A coroutine process next if this one receives a URL that is not from food2fork
    """
    while True:
        url = yield
        if urlparse(url).hostname == 'food2fork.com':
            try:
                recipes = get_recipes(url=url)
            except:
                # TODO: log failed request
                pass
            else:
                for recipe in recipes:
                    done.send((recipe['source_url'], ))
        elif successor:
            successor.send(url)
