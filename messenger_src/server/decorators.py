import logging

logger = logging.getLogger('decorators')


def logged(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'{func.__name__} - with args:{args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper
