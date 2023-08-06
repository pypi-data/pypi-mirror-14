from cubicweb_celery import app


@app.cwtask
def newgroup(self, name):
    return self.cw_cnx.create_entity('CWGroup', name=name).eid


@app.cwtask
def newgroup_retried(self, name):
    try:
        1 / 0
    except Exception as ex:
        self.retry(ex, countdown=5)
