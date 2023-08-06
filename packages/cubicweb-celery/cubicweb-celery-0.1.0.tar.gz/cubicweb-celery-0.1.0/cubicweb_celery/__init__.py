import logging
import os.path as osp

from optparse import make_option

from celery import Celery
from celery import signals, task

from cubicweb.cwconfig import CubicWebConfiguration as cwcfg
from cubicweb.cwvreg import CWRegistryStore

log = logging.getLogger(__name__)


class CWTask(task.Task):
    need_cnx = False
    abstract = True

    def __call__(self, *args, **kwargs):
        if self.need_cnx:
            with self.app.cwrepo.internal_cnx() as cnx:
                try:
                    self.cw_cnx = cnx
                    ret = super(CWTask, self).__call__(*args, **kwargs)
                except:
                    cnx.rollback()
                    raise
                else:
                    cnx.commit()
                    return ret
                finally:
                    self.cw_cnx = None
        else:
            return super(CWTask, self).__call__(*args, **kwargs)


class CWCelery(Celery):
    task_cls = 'cubicweb_celery:CWTask'

    defaults = {
        'CELERY_TASK_SERIALIZER': 'json',
        'CELERY_RESULT_SERIALIZER': 'json',
        'CELERY_ENABLE_UTC': True,
    }

    conf_freezed = False

    def freeze_conf(self):
        self.conf_freezed = True
        self.dummy_conf = dict(self.conf)

    @property
    def cubes_conf(self):
        if self.conf_freezed:
            return self.dummy_conf
        else:
            return self.conf

    def setup_cw(self, cwconfig):
        self.cwconfig = cwconfig

        celery_config = self.defaults.copy()
        if cwconfig.mode == 'test':
            celery_config['CELERY_ALWAYS_EAGER'] = True

        if self.conf_freezed:
            return

        if cwconfig.apphome is not None:
            fpath = osp.join(cwconfig.apphome, 'celeryconfig.py')
            if osp.isfile(fpath):
                with open(fpath, 'rb') as fobj:
                    exec(fobj.read(), celery_config)
        self.config_from_object(celery_config)

    def cwtask(self, *args, **opts):
        opts.setdefault('bind', True)
        opts.setdefault('need_cnx', True)
        if len(args) == 1:
            return self.task(**opts)(args[0])
        return self.task(*args, **opts)

app = CWCelery()

app.user_options['preload'].add(
    make_option(
        '-i', '--instance',
        default=None,
        help='CubicWeb instance name.'),
)

app.user_options['preload'].add(
    make_option(
        '--debug',
        action='store_true',
        default=False,
        help='Enable cubicWeb debug mode.'),
)

user_options = {}


def init_repo(cwconfig):
    # We do NOT want cubicweb to mess with logging because celery is already
    # doing acrobatic things with it.
    vreg = CWRegistryStore(cwconfig, initlog=False)
    return cwconfig.repository(vreg)


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    global user_options
    user_options.update({
        'instance': options['instance'],
        'debug': options['debug']
    })
    cwconfig = cwcfg.config_for(
        user_options['instance'], debugmode=user_options['debug'])

    # load the repo
    repo = app.cwrepo = init_repo(cwconfig)
    # make sure the 'celery' cube is loaded. The cube has taken care of
    # setting up the app.
    # Any cube depending on the celery cube may update the configuration
    # in its registration callback.
    if 'celery' not in repo.get_cubes():
        raise ValueError("The 'celery' cube must be installed in the instance")


@signals.worker_process_init.connect
def on_worker_process_init(**kw):
    # Use a fresh new repository to avoid sharing anything with the forked one.

    global user_options
    cwconfig = cwcfg.config_for(
        user_options['instance'], debugmode=user_options['debug'])

    # Prevent cubes from modifying the configuration
    app.freeze_conf()
    repo = app.cwrepo = init_repo(cwconfig)
    repo.hm.call_hooks('server_startup', repo=repo)
