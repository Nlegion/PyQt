import logging

logger = logging.getLogger('decorators')


def logged(func): # декортатор логирования
    def wrapper(*args, **kwargs):
        logger.debug(f'{func.__name__} - with args:{args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper
