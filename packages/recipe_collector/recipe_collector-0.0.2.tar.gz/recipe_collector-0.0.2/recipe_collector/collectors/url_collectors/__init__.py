from .food2fork import food2fork


def url_pipeline(storage):
    """
    This function sets up the full chain of coroutines for the URL processing pipeline.
    """
    pipeline = food2fork(storage=storage, successor=None)
    return pipeline
