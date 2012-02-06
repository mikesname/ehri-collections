from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from contextlib import contextmanager as _contextmanager

# globals
env.project_name = 'ehriportal'

@_contextmanager
def virtualenv():
    with cd(env.path):
        with prefix(env.activate):
            yield

# environments
def remote():
    "Use the local virtual server"
    env.hosts = ['ehri01.dans.knaw.nl']
    env.path = '/home/michaelb/ehri-collections'
    env.user = 'michaelb'
    env.activate = 'source ./bin/activate'
    env.virtualhost_path = "/testportal"

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
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    #sudo('yum install -y apache2')        
    #sudo('yum install -y libapache2-mod-wsgi')
    # we want rid of the defult apache config
    #sudo('cd /etc/apache2/sites-available/; a2dissite default;')
    run('mkdir -p %s; cd %s; virtualenv --python=python2.6 .;' % (env.path, env.path))
    run('cd %s; mkdir -p releases; mkdir -p shared; mkdir -p packages;' % env.path)
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
    install_site()
    symlink_current_release()
    migrate()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    env.version = version
    run('cd %s; rm releases/previous; mv releases/current releases/previous;' % env.path)
    run('cd %s; ln -s %s releases/current' % (env.path, env.version))
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    run('cd %s; mv releases/current releases/_previous;' % env.path)
    run('cd %s; mv releases/previous releases/current;' % env.path)
    run('cd %s; mv releases/_previous releases/previous;' % env.path)
    restart_webserver()    

# Helpers. These are called by other functions rather than directly
def upload_tar_from_git():
    "Create an archive from the current Git master branch and upload it"
    local('git archive --format=tar master | gzip > %s.tar.gz' % env.release)
    run('mkdir %s/releases/%s' % (env.path, env.release))
    put('%s.tar.gz' % env.release, '%s/packages/' % env.path)
    run('cd %s/releases/%s && tar zxf ../../packages/%s.tar.gz' % (env.path, env.release, env.release))
    local('rm %s.tar.gz' % env.release)

def install_site():
    "Add the virtualhost file to apache"
    #sudo('cd %s/releases/%s; cp %s%s%s/etc/apache2/sites-available/' % (
    #    env.path, env.release, env.project_name, env.virtualhost_path, env.project_name))
    #sudo('cd /etc/apache2/sites-available/; a2ensite %s' % env.project_name) 

def install_requirements():
    "Install the required packages from the requirements file using pip"
    with virtualenv():
        run('cd %s; pip install -E . -r ./releases/%s/%s/requirements/project.txt' % (
            env.path, env.release, env.project_name))

def symlink_current_release():
    "Symlink our current release"
    with settings(warn_only=True):
        run('cd %s; rm -f releases/previous; mv releases/current releases/previous;' % env.path)
    run('cd %s; ln -s %s releases/current' % (env.path, env.release))

def migrate():
    "Update the database"
    with virtualenv():
        run('cd %s/releases/current/%s; python manage.py syncdb --noinput' % (
            env.path, env.project_name))
        run('cd %s/releases/current/%s; python manage.py migrate' % (
            env.path, env.project_name))
        run('cd %s/releases/current/%s; mkdir -p media; python manage.py collectstatic --noinput' % (
            env.path, env.project_name))

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/httpd restart')

