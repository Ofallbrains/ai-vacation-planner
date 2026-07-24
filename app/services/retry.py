import time


def retry(function, retries=3, delay=1):
    """
    Retry a function if it raises an exception.
    """

    last_exception = None

    for attempt in range(retries):

        try:
            return function()

        except Exception as e:

            last_exception = e

            print(
                f"Retry {attempt + 1}/{retries} failed: {e}"
            )

            time.sleep(delay)

    raise last_exception