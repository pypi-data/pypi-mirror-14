import csv
from recipe_collector.utils.decorators import coroutine


@coroutine
def urls_csv(file_path, mode):
    """
    This coroutine receives tuples of title and url values and saves them to a CSV file.
    """
    with open(file_path, mode) as f:
        csv_file = csv.writer(f, delimiter=',')
        while True:
            title, source_url = yield
            csv_file.writerow([title, source_url])


@coroutine
def html_csv(file_path, mode):
    """
    This coroutine receives tuples of url and HTML values and saves them to a CSV file.
    """
    with open(file_path, mode) as f:
        csv_file = csv.writer(f, delimiter=',', quotechar="'")
        while True:
            source_url, html = yield
            csv_file.writerow([source_url, html])
