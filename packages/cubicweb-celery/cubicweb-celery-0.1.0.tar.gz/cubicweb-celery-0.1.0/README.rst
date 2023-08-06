===============
CubicWeb Celery
===============

Celery integration with CubicWeb

Getting Started
---------------

Enable the 'celery' cube in your ``myapp`` cubicweb instance::
  
  $ cubicweb-ctl shell myapp
  entering the migration python shell
  just type migration commands or arbitrary python code and type ENTER to execute it
  type "exit" or Ctrl-D to quit the shell and resume operation
  >>> add_cube('celery')
  >>> ^D

If needed, configure the broker_url in ``all-in-one.conf``. By
default, and only when using a postgresql database, the trunk_
transport will be used for the broker; make sure it is installed.

.. _trunk: https://github.com/cyberdelia/trunk


Write a task::

  from cubicweb_celery import app

  @app.cwtask
  def ping(self):
      return 'pong'

  @app.cwtask
  def users(self):
      return [str(x[0]) for x in self.cw_cnx.execute('String L WHERE U login L')]
      
      
or as a class::

    from cubicweb_celery import app

    class MyTask(app.Task):
        need_cnx = True  # if false (the default), self.cw_cnx will not be set
                         # before running the task

        def run(self):
	    self.cw_cnx.execute('Any X WHERE ...')
	    
.. Note:: In order to make the task automatically available by the
          celery worker, you must ensure the you should write it in a
          python file that is automatically loaded by CubicWeb, best
          candidate being the ``sobjects`` module of a cube (see the
          `CubicWeb's regitries documentation`_).

	  
Then start a celery worker::

    celery -A cubicweb_celery -i INSTANCE_NAME worker [ --beat ]


Then you can make the worker execute a task by calling it, eg. from
an Operation_. You may also run a task from a ``cubicweb-ctl shell``::

  $ cubicweb-ctl shell myapp
  >>> from cubes.myapp.sobjects import ping, users
  >>> print ping.delay().wait()
  'pong'
  >>> print users.delay().wait()
  ['anon', 'admin']
  
  
.. _`CubicWeb's regitries documentation`: https://docs.cubicweb.org/book/intro/concepts.html#the-registry
    
.. _Operation: https://docs.cubicweb.org/book/devrepo/repo/hooks.html#operations
