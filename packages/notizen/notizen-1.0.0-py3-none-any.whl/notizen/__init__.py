# coding: utf-8

__version__ = '1.0.0'

__main_author_name__ = 'Pablo Figue'
__main_author_email__ = 'pfigue posteo de'
__authors__ = (
    '%s <%s>' % (__main_author_name__, __main_author_email__),
)
__license__ = 'MIT'
__program_name__ = 'notizen'
__short_description__ = 'Indexing and searching of personal notes.'
__url__ = 'https://github.com/pfigue/notizen'


def get_platform_id() -> str:
    '''Returns a string with the description of the platform.

E.g.:
    Linux-3.8.1-1-mainline; x86_64-64bit; CPython-3.4.3'''

    import platform
    msg = '{platform}; {arch}; {python_implementation}-{python_version}'
    msg = msg.format(
        platform=platform.system() + '-' + platform.release(),
        arch=platform.machine() + '-' + platform.architecture()[0],
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
    )
    del(platform)
    return msg
