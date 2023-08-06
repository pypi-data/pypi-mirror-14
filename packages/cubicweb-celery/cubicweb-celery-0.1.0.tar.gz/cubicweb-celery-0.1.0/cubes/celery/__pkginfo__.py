# pylint: disable=W0622
"""cubicweb-celerytest application packaging information"""

modname = 'celery'
distname = 'cubicweb-celery'

numversion = (0, 1, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'Unlish'
author_email = 'contact@unlish.com'
description = 'Celery cube'
#web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ =  {'cubicweb': '>= 3.19.6', 'cwcelery': None}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]
