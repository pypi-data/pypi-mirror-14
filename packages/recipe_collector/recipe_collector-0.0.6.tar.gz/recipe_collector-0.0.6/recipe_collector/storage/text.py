import os
import string
from urllib.parse import urlparse
from recipe_collector.utils.decorators import coroutine


file_name_tpl = '{0}-{1}.html'
name_trans_table = {ord(k): '-' for k in string.punctuation}


@coroutine
def html_text_file(file_dir, mode):
    """
    This coroutine receives tuples of url and HTML values and saves them to a text file.
    """
    while True:
        source_url, html = yield
        parsed = urlparse(source_url)
        file_name = file_name_tpl.format(
            parsed.hostname.translate(name_trans_table),
            parsed.path.translate(name_trans_table))
        with open(file_name, mode) as f:
            f.write(html)
