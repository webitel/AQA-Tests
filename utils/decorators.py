import functools


def common_decorator():
    """

    """
    def po_wrapper(func):
        @functools.wraps(func)
        def wrapper(app, *args, **kwargs):
            try:
                func(app, *args, **kwargs)
            except Exception as e:
                raise e
            finally:
                pass
        return wrapper
    return po_wrapper


def calculate_time(func):
    """
    # decorator to calculate duration
    # taken by any function.

    # from utils.helpers.decorator import calculate_time
    # @calculate_time
    """
    import time
    from datetime import timedelta

    def inner1(*args, **kwargs):
        start_time = time.monotonic()
        func(*args, **kwargs)
        end_time = time.monotonic()
        print("\nTotal time taken in function <%s> - <%s>\n"
              % (func.__name__, timedelta(seconds=end_time - start_time)))
    return inner1
