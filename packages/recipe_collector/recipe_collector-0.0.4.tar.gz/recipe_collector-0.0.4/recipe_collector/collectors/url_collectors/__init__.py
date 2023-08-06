from .food2fork import food2fork


def url_pipeline(done):
    """
    This function sets up the full chain of coroutines for the URL processing pipeline.
    """
    pipeline = food2fork(done=done, successor=None)
    return pipeline
