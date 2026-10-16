import time


def retry(function, retries=3, delay=1):
    """
    Retry a function if it raises an exception.
    """
    if retries < 1:
        raise ValueError("retries must be at least 1")

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
            
            if last_exception is not None:
                raise last_exception
            
            raise RuntimeError("Retry failed without an exception")
