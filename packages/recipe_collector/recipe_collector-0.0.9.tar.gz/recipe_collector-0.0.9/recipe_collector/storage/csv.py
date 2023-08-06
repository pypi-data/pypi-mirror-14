import csv
from recipe_collector.utils.decorators import coroutine


@coroutine
def to_csv(file_path, mode='w+', delimiter=',', quotechar="'"):
    """
    This coroutine receives tuples of values and saves them to a row in a CSV file.

    Args:
    * file_path: Path to the output CSV file
    * mode: A file mode for opening the CSV file. Default: w+
    * delimiter: Delimiter character for the CSV file. Default: ,
    * quotechar: Quoted text character for the CSV file. Default: '
    """
    with open(file_path, mode) as f:
        csv_file = csv.writer(f, delimiter=delimiter)
        while True:
            (*values,) = yield
            csv_file.writerow(values)
