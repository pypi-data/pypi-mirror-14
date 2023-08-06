import cubicweb_celery


def registration_callback(vreg):
    cubicweb_celery.app.setup_cw(vreg.config)
