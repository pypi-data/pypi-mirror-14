
try:
    from io import BytesIO  # py3
except ImportError:
    from cStringIO import StringIO as BytesIO  # py2

import collections
import getpass
import json
import logging
from os.path import expanduser, join, isfile
import os
import re
import sys
import time
import urlparse


import click
import requests

from config_reader import ProjectReader, VersionReader
from .util import make_archive, normalize_url


log = logging.getLogger("cocaine-cli")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(message)s"))
log.addHandler(stdout_handler)
log.setLevel(logging.INFO)

AUTH_FILE = join(expanduser("~"), ".cocaine-pipelinerc")
PROJECT_FILE = './project.json'

NO_AUTH_COMMANDS = ("login", "init")
NO_CONFIG_COMMANDS = ("login", "init", "reschedule", "task", "status", "clusters_info", "clusters_create")

YANDEX_PIPELINE_URL = "http://pipeline.ape.yandex-team.ru"

BASE = None
TOKEN = None
USER = None
DEBUG = False

CONFIG = collections.OrderedDict()

API_VERSION = (0, 0, 10)

headers = {'content-type': 'application/json'}


def validate_item(prompt, validator, help_message):
    def wrapper(ctx, param, value):
        while not validator(value):
            click.echo("%s. Try again, please" % help_message)
            value = click.prompt(prompt)
        return value
    return wrapper


def is_project_name_valid(project_name):
    return re.match(r"^[a-z]+[a-z0-9_-]*$", project_name) is not None


def is_version_valid(version):
    return re.match(r"^[a-z0-9_-]+$", version) is not None

class URLParam(click.ParamType):
    name = "URL"

    def convert(self, value, param, ctx):
        u = urlparse.urlparse(value)
        if u.scheme not in ("http", "https"):
            self.fail("URL has unsupported scheme %s. Must be `http` or `https`" % u.scheme)
        elif not u.netloc:
            self.fail("hostname must be specified")
        return value


class MyGroup(click.Group):

    def __init__(self, commands=None, **kwargs):
        super(MyGroup, self).__init__(commands=commands, **kwargs)

        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return list(self.commands)


b = ""


def blank():
    global b
    b += " "
    return b


def _command_need_auth(cmd):
    return cmd not in NO_AUTH_COMMANDS


def _command_need_config(cmd):
    return cmd not in NO_CONFIG_COMMANDS


def _validate_url(url):
    u = urlparse.urlparse(url)

    assert u.scheme == "http" or u.scheme == "https", "url scheme should be http or https, `%s` got instead" % u.scheme

    assert 0 < len(u.netloc), "host should be specified: `%s`" % u.netloc

    assert len(u.query) == 0 and len(u.fragment) == 0 and len(u.params) == 0, (
        "query, fragment and params should be absent in url")


def _load_auth(ctx, token, base):
    global BASE
    global TOKEN
    global DEBUG
    if token and base:
        TOKEN, BASE = token, base
        try:
            _validate_url(base)
            BASE = normalize_url(base)
            return True
        except Exception as e:
            log.exception(e)
            click.echo('Base url broken. Please, use cocaine login with correct arguments (url ex. http://some.host:1234)')
            ctx.abort()

    elif not isfile(AUTH_FILE):
        return False
    try:
        rc_file = file(AUTH_FILE)
        data = json.load(rc_file)
        rc_file.close()
        try:
            _validate_url(data.get("base"))
            BASE = normalize_url(data.get("base"))
        except Exception as e:
            log.exception(e)
            click.echo('Base url broken. Please, use cocaine login with correct arguments (url ex. http://some.host:1234)')
            ctx.abort()
        TOKEN = data["token"]

        if "debug" in data:
            DEBUG = data["debug"]

        return True
    except (ValueError, KeyError):
        click.echo('Please, use `coke login` first!')
        ctx.abort()


def _check_api_version(ctx):
    r = requests.get(normalize_url(BASE + "/version/"), params={"debug": DEBUG})
    if r.status_code >= 400:
        click.echo("Can't check API version")
        ctx.abort()
    parsed_api_version = tuple([int(v) for v in r.text.split(".")])
    for level in xrange(3):  # TODO: use xrange(2) after 0.1 version
        if int(parsed_api_version[level]) != API_VERSION[level]:
            click.echo("Client API version %s doesn't match that of the server %s. Please, update your client using `pip install cocaine-cli`." % (API_VERSION, parsed_api_version))
            ctx.abort()


def _fill_config(name, version, profile, main, user):
    # title
    CONFIG["name"] = name
    # version
    CONFIG["version"] = version
    # members
    CONFIG["members"] = CONFIG.get("members", {})
    u_name_default = USER or getpass.getuser()
    if not user:
        while click.confirm("Add user to config?", default=False):
            u_name = click.prompt("User name", default=u_name_default)
            u_roles = click.prompt("User roles", default="admin, developer")
            CONFIG["members"][u_name] = u_roles.replace(" ", "").split(",")

        u_roles_default = CONFIG["members"].get(u_name_default)

        if not u_roles_default:
            if click.confirm("""WARNING: your current user %s is not a memeber of the project.
So after push this user will not be able to do anything with the project. Add you?""" % u_name_default, default=True):
                CONFIG["members"][u_name_default] = ("admin", "developer")
        elif "admin" not in u_roles_default:
            if click.confirm("""Warning: your current user %s doesn't have an `admin` role in project.
So after project creation this user will not be able to update project settings or
deploy to production clusters. Should I add `admin` role to user %s?""" % (u_name_default, u_name_default), default=True):
                u_roles_default.append("admin")
    else:
        for u_rule in user:
            CONFIG["members"][u_rule[0]] = u_rule[1].replace(" ", "").split(",")

    # clusters
    # TODO get /clusters from API
    CONFIG["clusters"] = {
        "unstable": _gen_cluster_cnf("unstable", main, profile, ye="stress"),
        "testing": _gen_cluster_cnf("testing", main, profile),
        "production": _gen_cluster_cnf("production", main, profile)
    }


def _gen_cluster_cnf(name, slave, profile, ye=None):
    return {
        "profile": profile,
        "manifest": {
            "slave": slave,
            "environment": {
                "YANDEX_ENVIRONMENT": ye or name
            }
        }
    }


def handle_streaming_response(r):
    log.debug("response %s", r)
    log.debug("headers %s", r.headers)
    status = 0
    for ch in r.iter_lines(chunk_size=1):

        log.debug("got chunk %s", ch)
        try:
            r = json.loads(ch)
            if "error" in r and r["error"]:
                status = 2
                log.error(r["message"])

                if r.get("request-id"):
                    log.error("request-id: %s", r["request-id"])

                if DEBUG:
                    log.error(r["traceback"])
            else:
                if "b64" in r and r["b64"]:
                    m = r["message"].decode("base64")
                else:
                    m = r["message"]
                log.info(m)
        except Exception:
            log.debug("undecodable chunk %s", ch)
    if status != 0:
        raise click.Abort()


@click.group(cls=MyGroup)
@click.pass_context
@click.option('sets', '--set', nargs=2, multiple=True, required=False,
              metavar="<k.e.y> <val>",
              help="override or provide corresponding fields of ./project.json")
@click.option('--no-config', "--nc", is_flag=True,
              help="don't load ./project.json (to manage projects other than current)")
@click.option('--save', is_flag=True,
              help="store --set fields to ./project.json")
@click.option('--debug', is_flag=True,
              help="spew more logs")
@click.option('--token', metavar='AUTH_TOKEN', type=click.STRING)
@click.option('--base-url', metavar='BASE_API_URL', type=click.STRING)
def cli(ctx, debug, nc, sets, save, token, base_url):
    """DON'T PANIC.

    Deliver your project to the public cloud with steps listed below
    in the Commands section.

    Or take your time and get acquainted with their --help messages.
    """

    global DEBUG
    global CONFIG

    DEBUG = debug
    if _command_need_config(ctx.invoked_subcommand) and not nc:  # no_config
        try:
            with open(PROJECT_FILE, 'r') as prj_file:
                CONFIG = json.load(prj_file, object_pairs_hook=collections.OrderedDict)
        except (ValueError, IOError) as e:
            click.echo('Can`t load %s' % PROJECT_FILE)
            click.echo(e)
            click.echo('You can use `coke init` command to make a default one, then modify it and try again.')
            ctx.abort()
    else:
        CONFIG = collections.OrderedDict()

    for s in sets:
        path = s[0].split(".")
        last_path = path.pop()
        item = CONFIG
        for section in path:
            if section not in item:
                item[section] = {}
            item = item[section]
        item[last_path] = s[1]

    if save:
        with file(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)

    if DEBUG:
        log.setLevel(logging.DEBUG)

    if _command_need_auth(ctx.invoked_subcommand):
        if _load_auth(ctx, token, base_url):
            _check_api_version(ctx)


@cli.command(short_help="set and verify a cloud API entry point and an auth token")
@click.pass_context
@click.option('--url', metavar="URL", type=URLParam(),
              default=YANDEX_PIPELINE_URL, help="API server [%s]" % YANDEX_PIPELINE_URL)
@click.option('--token', metavar="AUTH_TOKEN", type=click.STRING)
@click.option('--debug', is_flag=True)
def login(ctx, url, token, debug):
    "set and verify a cloud API entry point and an auth token"

    global DEBUG
    DEBUG = DEBUG or debug

    try:
        _validate_url(url)
        url1 = normalize_url(url)
    except Exception as e:
        log.exception(e)
        log.error(e.message)
        click.echo("Url validation failed. Please, use cocaine login with correct --url parameter")
        click.echo("  (e.g. --url http://some.host:1234)")
        raise click.Abort()

    if not token:
        click.echo("Please get the authentication token with your browser at %s" % normalize_url(url + "/login"))
        click.echo("and provide it in the --token parameter")
        raise click.Abort()

    # verify token
    params = {"token": token}
    r = requests.get(normalize_url(url + "/token/"), params=params)
    if r.status_code != 200:
        if not click.confirm("unable to verify token via API. Save it anyway?", default=False):
            raise click.Abort()
    else:
        if not json.loads(r.text)["ok"] == "valid":
            click.echo("provided token is invalid")
            raise click.Abort()

    with open(AUTH_FILE, "w") as rc_file:
        os.chmod(AUTH_FILE, 0600)
        json.dump({
            "base": url1,
            "token": token,
            "debug": DEBUG
        }, rc_file, indent=2)
    click.echo("Successfully logged in. Auth information has been written to %s" % AUTH_FILE)


@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass


@cli.command(
    short_help="""initialize a new ./project.json file with defaults and blanks.
tweak generated project.json to suit to your needs""")
@click.option('--name', prompt="name (project title)",
              callback=validate_item("name (project title)", is_project_name_valid,
                                     "Project title must start from a letter and contain only [a-z0-9_] (e.g. my-awesome-app)"),
              default=CONFIG.get("name"), required=True)
@click.option('--version', prompt="Project version",
              callback=validate_item("Project version", is_version_valid,
                                     "Version must match [a-zA-Z0-9_-]+ (e.g. 32, 1-12-3, abcde-32-abc)"),
              default=CONFIG.get("version"), required=True)
@click.option('--profile', prompt="Name of the Cocaine profile (leave it empty if you don't know what it is)", default="docker-one", required=True)
@click.option('--main', prompt="Path to the executable file inside the container/archive. Cocaine will use exactly this path to launch a worker", required=True)
@click.option('--user', nargs=2, multiple=True)
@click.option('--yes', is_flag=True)
def init(name, version, profile, main, user, yes):

    # use project_name, version_tag, main, user
    # generate profile, manifest, clusters (testing, production)
    # save to ./project.json

    _fill_config(name, version, profile, main, user)

    click.echo(json.dumps(CONFIG, indent=2))
    if yes or click.confirm("Save?", default=True, show_default=True):
        with file(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)


@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass


@cli.command(short_help="create a new cloud project described in ./project.json")
@click.pass_context
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing project")
def create(ctx, force, **kwargs):
    "create a new project in a cloud described in ./project.json"

    params = {
        "force": force,
        "token": TOKEN,
        "debug": DEBUG
    }

    project_def = ProjectReader.read(CONFIG)

    missing_fields = [f for f in ("name", "members", "clusters")
                      if f not in CONFIG]

    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    print "creating project:"
    print json.dumps(project_def, indent=2).encode("utf8")

    r = requests.post(normalize_url(BASE + "/create/"),
                      headers=headers,
                      params=params,
                      data=json.dumps(project_def, indent=2))
    handle_streaming_response(r)


@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass


def _validate_version(version):

    if not isinstance(version, (str, unicode)):
        log.error("version '%s' should be str/unicode, but is %s instead", version, type(version))
        raise click.Abort()

    if not re.search(r'^[a-zA-Z0-9_-]+$', version):
        log.error("version '%s' should match /^[a-zA-Z0-9_-]+$/ regex", version)
        raise click.Abort()


@cli.command(short_help="push an app version to the cloud, then build it")
@click.pass_context
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing version")
@click.option('--no-build', '-n', is_flag=True,
              help="don't schedule build of a container")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
def push(ctx, force, no_build, no_docker, increment, version, **kwargs):
    "push an app version to the cloud, then build it"

    new_version = version
    old_version = CONFIG.get("version", "0-0-0")

    # build_docker_image = True
    # archive = not no_docker

    # if build_docker_image and not archive:
    #     click.echo("-a required for --build-docker-image")
    #     raise click.Abort()

    if increment and version:
        click.echo("options -i and -v are mutually exclusive")
    elif increment:
        cocs_suffix = re.search(r'-cocaine-(\d+)?$', old_version)

        if cocs_suffix:
            try:
                new_version_patch = str(int(cocs_suffix.group(1)) + 1)
            except ValueError:
                click.echo("Please update version in project.json manually")
            new_version = re.sub(r'\d+$', new_version_patch, old_version)
        else:
            new_version = old_version + "-cocaine-1"

        CONFIG["version"] = new_version

    _validate_version(CONFIG.get("version"))

    if new_version:
        with open(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)
        log.info("incrementing version from %s to %s", old_version, new_version)

    params = {
        "force": force,
        "no-build": no_build,
        "token": TOKEN,
        "sync": True,
        "debug": DEBUG,
    }

    version_def = VersionReader.read(CONFIG)

    missing_fields = [f for f in ("name", "version", "clusters")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    archive = True

    if CONFIG.get("source"):
        s = CONFIG.get("source")
        if isinstance(s, dict) and s.get("type") == "docker":
            archive = False

    if not archive:
        assert not no_docker, "can't upload source.type==docker with no-docker option"

        r = requests.post(normalize_url(BASE + "/push/"),
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)

    else:
        key = "%(name)s_%(version)s" % (version_def)

        version_def["source"] = {
            "namespace": "app-archive",
            "key": key,
            "tags": ("APP_ARCHIVE",),
            "type": "archive"
        }

        version_def["source"]["do_build"] = not no_docker

        log.info("creating archive")

        tarball = make_archive(".")

        log.info("uploading archive")

        files = {"archive": ("archive.tar", BytesIO(tarball), "application/octet-stream", {})}

        r = requests.post(normalize_url(BASE + "/app-archive"),
                          data={"key": key},
                          params={"debug": DEBUG},
                          files=files)

        if r.status_code != 200:
            try:
                m = json.loads(r.text)
                log.error("server error: %s", m.get("message"))
                log.error(m.get("traceback"))
            except Exception:
                log.error("non-ok status code on archive upload")
                log.error("%s\n%s", r, r.text)

            raise click.Abort()

        log.info("upload done")

        log.info("pushing and building version")

        r = requests.post(normalize_url(BASE + "/push/"),
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)


@cli.command(short_help="deploy an alredy built version to the <target> cluster")
@click.pass_context
@click.option('-u', is_flag=True,
              help="undeploy version from cluster")
@click.argument("target", metavar="<target>")
def deploy(ctx, target, u, **kwargs):
    "deploy an alredy built version to the <target> cluster"

    event = "deploy"

    if u:
        event = "undeploy"

    missing_fields = [f for f in ("name", "version")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    r = requests.post(normalize_url(BASE + "/%s/%s/" % (event, target)),
                      data=json.dumps(CONFIG, indent=2),
                      params={"sync": True,
                              "token": TOKEN,
                              "debug": DEBUG},
                      stream=True)

    handle_streaming_response(r)


@cli.command(short_help="balance a load between versions at the <target> cluster")
@click.pass_context
@click.option("--prestable-only", is_flag=True,
              help="apply balance settings only to prestable Routing Group")
@click.argument("target", metavar="<target>")
def balance(ctx, target, prestable_only, **kwargs):
    """
    balance load between versions at the <target> cluster

    looks up routing info in your project.json, updates
    cluster configuration for the project, and performs
    a corresponding balance task.
    """

    bad_routing_msg = """
  To update routing with 'balance' command, you should have 'routing' section for
particular cluster configured like this:
  "clusters": {
    "%s": {
      "routing": {
        "<project_name>_<versionA>": 100,
        "<project_name>_<versionB>": 200
      }
    }
  }
""" % target

    missing_fields = [f for f in ("name", "version")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    try:
        routing = CONFIG.get("clusters").get(target).get("routing")
        if 0 == len(routing):
            raise TypeError("routing should not be empty")
        for k, v in routing.items():
            if not isinstance(k, (str, unicode)):
                raise TypeError("routing key '%s' should be a str/unicode" % k)
            if not isinstance(v, int):
                try:
                    routing[k] = int(v)
                except ValueError as err:
                    raise TypeError("routing value %s at key '%s' should be an int" % (k, v))

    except (TypeError, KeyError, AttributeError) as err:
        click.echo(bad_routing_msg)
        raise err
    else:
        if not isinstance(routing, dict):
            click.echo(bad_routing_msg)
            raise click.Abort()

    CONFIG["prestable_only"] = prestable_only

    r = requests.post(normalize_url(BASE + "/balance/%s/" % target),
                      data=json.dumps(CONFIG, indent=2),
                      params={"sync": True,
                              "token": TOKEN,
                              "debug": DEBUG},
                      stream=True)

    handle_streaming_response(r)


@cli.command(name="deliver", short_help="perform all three of the above steps with one command")
@click.pass_context
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.argument("target", metavar="<target>")
def deliver(ctx, increment, version, no_docker, target, **kwargs):
    """
    perform all three of the above steps with one command

    pushes, deploys to <target> cluster and configures routing
    with one route, pointing to version it pushed with weight of 10
    """
    # NOTE: unused variable
    force = False

    new_version = version
    old_version = CONFIG.get("version", "0-0-0")

    if increment and version:
        click.echo("options -i and -v are mutually exclusive")
    elif increment:
        cocs_suffix = re.search(r'-cocaine-(\d+)?$', old_version)

        if cocs_suffix:
            try:
                new_version_patch = str(int(cocs_suffix.group(1)) + 1)
            except ValueError:
                click.echo("Please update version in project.json manually")
            new_version = re.sub(r'\d+$', new_version_patch, old_version)
        else:
            new_version = old_version + "-cocaine-1"

        CONFIG["version"] = new_version

    if new_version:
        with open(PROJECT_FILE, "w") as prj_file:
            json.dump(CONFIG, prj_file, indent=2)
        log.info("incrementing version from %s to %s", old_version, new_version)

    params = {"force": False,
              "no-build": False,
              "token": TOKEN,
              "sync": True,
              "debug": DEBUG}

    params["autorelease_to"] = target

    version_def = VersionReader.read(CONFIG)

    missing_fields = [f for f in ("name", "version", "clusters")
                      if f not in CONFIG]
    if len(missing_fields):
        click.echo("The config must have '%s' fields!" % missing_fields)
        raise click.Abort()

    archive = True

    if CONFIG.get("source"):
        s = CONFIG.get("source")
        if isinstance(s, dict) and s.get("type") == "docker":
            archive = False

    if not archive:

        assert not no_docker, "can't upload source.type==docker with no-docker option"

        r = requests.post(normalize_url(BASE + "/push/"),
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)

    else:
        key = "%(name)s_%(version)s" % (version_def)

        version_def["source"] = {
            "namespace": "app-archive",
            "key": key,
            "tags": ("APP_ARCHIVE",),
            "type": "archive"
        }

        version_def["source"]["do_build"] = not no_docker

        log.info("creating archive")

        tarball = make_archive(".")

        log.info("uploading archive")

        files = {"archive": ("archive.tar", BytesIO(tarball), "application/octet-stream", {})}

        r = requests.post(normalize_url(BASE + "/app-archive"),
                          data={"key": key},
                          params={"debug": DEBUG},
                          files=files)

        if r.status_code != 200:
            try:
                m = json.loads(r.text)
                log.error("server error: %s", m.get("message"))
                log.error(m.get("traceback"))
            except Exception:
                log.error("non-ok status code on archive upload")
                log.error("%s\n%s", r, r.text)

            raise click.Abort()

        log.info("upload done")

        log.info("pushing and building version")

        r = requests.post(normalize_url(BASE + "/push/"),
                          headers=headers,
                          params=params,
                          data=json.dumps(version_def, indent=2),
                          stream=True)
        handle_streaming_response(r)


# NOTE: this function is defined many times
@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass


@cli.group(cls=MyGroup, invoke_without_command=True)
@click.pass_context
def show(ctx):
    "inspect various minutae and statuses"
    if ctx.invoked_subcommand is None:
        ctx.forward(project_show)


@show.command(name="crashlog", short_help="show app crashlogs in <target> cluster")
@click.option("--list", "do_list", is_flag=True)
@click.option("--crashlog-id", help="if unknown, use --list option first")
@click.argument("target", metavar="<target>")
def show_crashlog(do_list, crashlog_id, target):
    """show app crashlogs in <target> cluster

    by default, last crashlog is shown
    """
    timestamp = crashlog_id
    project_id = CONFIG["name"]
    version_tag = CONFIG["version"]

    if do_list:
        r = requests.get(normalize_url(BASE + "/project/%s/version/%s/cluster/%s/crashlog/" % (project_id, version_tag, target)))
        crashlogs = json.loads(r.text)
        print "Date\t\t\t\tCrashlog Id"
        for timestamp, caltime, _, entry in sorted(_parseCrashlogs(crashlogs), key=lambda (ts, caltime, uuid, entry): ts):
            print "%s\t%s" % (caltime, entry)
        # for print _parseCrashlogs(crashlogs)
        # print r.text
    else:
        timestamp = timestamp or "_last"
        url = BASE + "/project/%s/version/%s/cluster/%s/crashlog/%s/" % (project_id, version_tag, target, timestamp)
        url = normalize_url(url)
        log.debug("url: %s", url)
        r = requests.get(url)
        print r.text.encode("utf8")


def _parseCrashlogs(crashlogs, timestamp=None):
    def is_filter(x):
        return x == timestamp if timestamp else True

    _list = (log.split(':', 1) + [log] for log in crashlogs)
    return [(ts, time.ctime(float(ts) / 1000000), name, entry) for ts, name, entry in _list if is_filter(ts)]


@show.command(name="task")
@click.pass_context
@click.argument("task-id")
def show_task(ctx, task_id):
    "show task status"

    ctx.forward(task_status)


@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass


@cli.group(cls=MyGroup)
def task():
    "tasks-related subcommands"
    pass


@task.command(name="status")
@click.pass_context
@click.argument("task-id")
def task_status(ctx, task_id):
    "display status for given task-id"

    r = requests.get(normalize_url(BASE + "/status/%s/" % task_id), params={"debug": DEBUG})
    print r.text.encode("utf8")
    # NOTE: does we need return here?
    return
    handle_streaming_response(r)


@task.command()
@click.pass_context
@click.argument("task-id")
def retry(ctx, task_id):
    "retry task with task-id"
    r = requests.post(normalize_url(BASE + "/task/%s/restart/" % task_id),
                      params={"sync": True,
                              "token": TOKEN,
                              "debug": DEBUG},
                      stream=True)

    handle_streaming_response(r)


@cli.group(cls=MyGroup)
def project():
    "manage project configuration"
    pass


@project.command(name="show")
def project_show():
    "show project status"

    project_id = CONFIG['name']
    r = requests.get(normalize_url(BASE + "/project/%s/" % project_id), params={"debug": DEBUG})
    print r.text.encode("utf8")
    if r.status_code != 200:
        sys.exit(2)

# @cli.group(cls=MyGroup)
# def version():
#     "manage version configuration"
#     pass


@cli.group(name=blank())
def _separator():
    pass


@cli.group(name=blank(), short_help="have to be a platform admin to do this:")
def _separator():
    pass


@cli.group(cls=MyGroup, short_help="manage cloud clusters")
def cluster():
    "manage cloud clusters (you have to be a platform admin to do this)"
    pass


@cluster.command()
@click.pass_context
def info(ctx):
    "dump cluster configuration"

    r = requests.get(normalize_url(BASE + "/clusters/"), params={"debug": DEBUG})
    print r.text.encode("utf8")
    if r.status_code != 200:
        sys.exit(2)


@cluster.command()
@click.pass_context
@click.option('-s', '--src', required=True, help="path to a file, formatted compatible to the output of `clusters_info`")
@click.option('-u', '--update', is_flag=True, default=False)
def create(ctx, src, update):
    with file(src, "r") as configs_file:
        configs = configs_file.read()
        click.echo(configs)
        if click.confirm("File is correct?", default=False):
            r = requests.post(normalize_url(BASE + "/clusters/"), params={
                "debug": DEBUG,
                "update": update,
                "token": TOKEN
            }, data=configs)
            handle_streaming_response(r)

# @cli.group(cls=MyGroup, short_help="manage global users")
# @click.pass_context
# def user(ctx):
#     "manage global users"
#     pass

# @cli.group(cls=MyGroup, name=blank())
# def _separator():
#     pass


@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


if __name__ == "__main__":
    cli()
