from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

# globals
env.project_name = 'ehriportal'

@_contextmanager
def virtualenv():
    with prefix(env.activate):
        yield

# environments
def remote():
    "Use the local virtual server"
    env.hosts = ['ehri01.dans.knaw.nl']
    env.path = '/home/michaelb/ehri-collections'
    env.user = 'michaelb'
    env.activate = 'source %s/bin/activate' % env.path
    env.solrconf = '/opt/apache-solr-3.5.0/portal/solr/conf'

# tasks
def test():
    "Run the test suite and bail out if it fails"
    local("cd %s; python manage.py test" % env.project_name)

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', provided_by=[local])
    require('path')
    sudo('yum install -y python-setuptools')
    sudo('yum-builddep -y python26-mysqldb')
    # PIL requirements
    sudo('yum install -y libjpeg-devel')
    sudo('yum install -y libpng-devel')
    sudo('easy_install pip')
    sudo('pip install virtualenv')

    run('mkdir -p %(path)s' % env)
    with cd(env.path):
        run('virtualenv --python=python2.6 .')
        run('mkdir -p releases shared packages site_media/media site_media/static')
        put("%(project_name)s/production_settings.py.sample" % env,
                "shared/production_settings.py") 
    deploy()

def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and 
    then restart the webserver
    """
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    upload_tar_from_git()
    install_requirements()
    symlink_current_release()
    activate_production_settings()
    migrate()
    collectstatic()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    require('path')
    env.version = version
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous;')
        run('ln -s %(version)s releases/current' % env)
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    with cd(env.path):
        run('mv releases/current releases/_previous')
        run('mv releases/previous releases/current')
        run('mv releases/_previous releases/previous')
    restart_webserver()    

# Helpers. These are called by other functions rather than directly
def upload_tar_from_git():
    "Create an archive from the current Git master branch and upload it"
    require("path", "release")
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    run('mkdir %(path)s/releases/%(release)s' % env)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    with cd("%(path)s/releases/%(release)s" % env):
        run('tar zxf ../../packages/%(release)s.tar.gz' % env)
    local('rm %(release)s.tar.gz' % env)

def install_requirements():
    "Install the required packages from the requirements file using pip"
    require("path", "project_name")
    with virtualenv():
        with cd(env.path):
            run('pip install -E . -r ./releases/%s/%s/requirements/project.txt' % (
                env.release, env.project_name))

def symlink_current_release():
    "Symlink our current release"
    require("path", "release")
    with settings(warn_only=True):
        with cd(env.path):
            run('rm -f releases/previous; mv releases/current releases/previous;')
            run('ln -s %(release)s releases/current' % env)

def activate_production_settings():
    """Copy shared/production_settings.py to the release
    folder where they will be imported by settings.py"""
    require("path", "release")
    with cd(env.path):
        put("%(project_name)s/production_settings.py.sample" % env,
                "shared/production_settings.py") 
        run("cp shared/production_settings.py releases/%(release)s/%(project_name)s/production_settings.py" % env)


def migrate():
    "Update the database"
    with virtualenv():
        with cd("%(path)s/releases/%(release)s/%(project_name)s" % env):
            run('python manage.py syncdb --noinput')
            run('python manage.py migrate')

def collectstatic():
    "Save static files to serve location."
    with virtualenv():
        with cd("%(path)s/releases/%(release)s/%(project_name)s" % env):
            run('python manage.py collectstatic --noinput')

def update_solr_schema():
    """Update the Solr schema.xml."""
    require("path", "project_name", "solrconf")
    with virtualenv():
        with cd("%(path)s/releases/current/%(project_name)s" % env):
            run('python manage.py build_solr_schema > _schema.xml')
            sudo('mv _schema.xml %(solrconf)s/schema.xml' % env)
            restart_solr()
            # fudge
            run('sleep 10')
            rebuild_index()

def reset_south():
    """Reset the south table."""
    with virtualenv():
        with cd("%(path)s/releases/current/%(project_name)s" % env):
            run('python manage.py reset south --noinput')
            run('rm -r portal/migrations')
            run('python manage.py convert_to_south portal')

def update_index():
    """Rebuild document index from database."""
    with virtualenv():
        with cd("%(path)s/releases/current/%(project_name)s" % env):
            run('python manage.py update_index')

def rebuild_index():
    """Rebuild document index from database."""
    with virtualenv():
        with cd("%(path)s/releases/current/%(project_name)s" % env):
            run('python manage.py rebuild_index --noinput')

def restart_solr():
    "Restart Solr (via Jetty)"
    sudo('/etc/init.d/jetty restart')


def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/httpd restart')

