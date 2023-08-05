import os

import six
from fabric.api import local
from fabric.decorators import task
from fabric.operations import put
from fabric.api import cd
from fabric.state import env
from utils import dockerfile
import settings as skeppa_settings
import ext


@task
def ping():
    '''
    Test command
    '''
    env.run('echo pong!')

    env.run("cat /etc/*-release")  # List linux dist info


@task
def setup():
    '''
    Perform initial setup (create docker-compose-config and mount dirs)
    '''
    settings = skeppa_settings.get_settings()

    # Create compose config files
    remote_conf_dir = os.path.join(env.path, settings.env_files_dir)
    env.run('mkdir -p {0}'.format(remote_conf_dir))

    # Create mount dir
    mount_dir = os.path.join(env.path, settings.mount_dir)
    env.run('mkdir -p {0}'.format(mount_dir))

    # Upload files
    if env.get('env_files', None):
        _upload_env_files(env.env_files)

    if env.get('compose_files', None):
        _upload_compose_files(env.compose_files)

    if env.get('files', None):
        _upload_files(env.files)


def _upload_files(files):
    settings = skeppa_settings.get_settings()

    mount_dir = os.path.join(env.path, settings.mount_dir)
    local_files_dir = os.path.join(os.getcwd(), settings.files_dir)
    formatted_list = []

    # Construct a formatted files to be uploaded/created list
    for target_file in files:
        remote_path = None
        local_path = None

        if isinstance(target_file, six.string_types):
            remote_path = target_file

            if ":" in target_file:
                struct = target_file.split(":")
                remote_path = struct[0]
                local_path = struct[1]
        else:
            remote_path, local_path = target_file.popitem()

        formatted_list.append((remote_path, local_path))

    for remote_path, local_path in formatted_list:
        if not local_path:
            remote_path = os.path.join(mount_dir, remote_path)
            env.run('mkdir -p {0}'.format(remote_path))
            continue

        remote_path = os.path.join(mount_dir, remote_path)
        local_path = os.path.join(local_files_dir, local_path)
        remote_dir = os.path.dirname(remote_path)

        env.run('mkdir -p {0}'.format(remote_dir))
        put(local_path, remote_path)


def _upload_env_files(env_files):
    settings = skeppa_settings.get_settings()

    current_dir = os.getcwd()
    local_conf_dir = os.path.join(current_dir, settings.env_files_dir)
    remote_conf_dir = os.path.join(env.path, settings.env_files_dir)

    env_files = env_files
    for env_file in env_files:
        env_path = os.path.join(local_conf_dir, env_file)
        remote_path = os.path.join(remote_conf_dir, env_file)
        put(env_path, remote_path)


def _upload_compose_files(compose_files):
    current_dir = os.getcwd()

    compose_files = compose_files
    for compose_file in compose_files:
        local_path = os.path.join(current_dir, compose_file)
        remote_path = os.path.join(env.path, compose_file)
        put(local_path, remote_path)


@task
def build():
    '''
    Build docker image(s)
    '''
    _build_image(env.image)


def _build_image(image):
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, image.get('path'))
    version = dockerfile.read_tag(image_path)

    # Tag release (master/develop)
    use_versioning = image.get('use_versioning', False)
    repository = image.get('repository')
    release_tag = image.get('tag', 'latest')
    extra_args = image.get('extra_args', "")

    local("docker build {0} -t {1}:{2} {3}".format(extra_args,
                                                   image.get('name'),
                                                   release_tag,
                                                   image_path))

    if use_versioning and version:
        local("docker build {0} -t {1}:{2} {3}".format(extra_args,
                                                       repository['url'],
                                                       version,
                                                       image_path))

    local("docker tag {0}:{1} {2}:{3}".format(image['name'], release_tag,
                                              repository['url'], release_tag))


@task
def push():
    '''
    Push image to registry and cleanup previous release
    '''
    _push_image(env.image)


def _push_image(image):
    ext.dispatch("before_push", image)

    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, image.get('path'))
    version = dockerfile.read_tag(image_path)
    use_versioning = image.get('use_versioning', False)

    repository = image.get('repository')
    release_tag = image.get('tag', 'latest')

    if use_versioning and version:
        local("docker push {0}:{1}".format(repository['url'], version))

    local("docker push {0}:{1}".format(repository['url'], release_tag))


@task
def deploy():
    '''
    Pull latest image and restart containers
    '''
    with cd(env.path):
        image = env.image
        compose_file = env.compose_files[0]

        ext.dispatch("before_deploy", image)

        repository = image.get('repository')
        release_tag = image.get('tag', 'latest')

        # Pull latest repro changes
        env.run("docker pull {0}:{1}".format(repository['url'], release_tag))

        # Restart web container
        env.run("docker-compose -f {0} -p {1} up -d".format(compose_file,
                                                            env.project))
