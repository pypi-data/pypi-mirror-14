import requests
from recipe_collector.utils.decorators import coroutine


@coroutine
def html(done):
    """
    This coroutine receives a URL and retrevies HTML.
    """
    while True:
        url = yield
        resp = requests.get(url)
        if resp.status_code == 200:
            done.send((url, resp.text))
        else:
            # TODO: log request failure
            pass
