#!/usr/bin/env python3
"""Main cli entry points"""

from argparse import ArgumentParser, OPTIONAL, ZERO_OR_MORE, FileType
from yaml import safe_load as load_yaml
from urllib.parse import urlparse
from pprint import pprint
from subprocess import PIPE, Popen, DEVNULL
from .exit_codes import GOOD_EXIT, TRANSPORT_ERROR_EXIT, UNKNOWN_COMMAND_EXIT, error_messages
from .utils import convert_bool
from . import formatter, log as _log
from pathlib import Path
from .repo import YamlFS
from io import StringIO
import logging
import shlex
import json
import sys
import os

default_config = {
    "environ_filename": 'environ.yml',
    "hosts_filename":  'hosts.yml',
    "facts_filename": 'facts.yml',
    "tags_filename":  'tags.yml',
    "nodes_dir": 'nodes',
    "jobs_dir": 'jobs',
    }

CONFIG_ORDER = ["/etc/fission/", "~/.config/fission/"]

log = _log.getChild("cli")

def main(argv=sys.argv[1:]):
    args = ArgumentParser()
    args.add_argument('-d', '--debug', default=False, action="store_true",
        help="Enable hidden debugging (fire up pdb on exceptions)")
    args.add_argument('-c', '--config', type=FileType('r'),
        help="Config file to load the base settings from")
    args.add_argument('-t', '--transport', default="local://",
        help="The transport to use for API operations")
    args.add_argument('-v', '--verbosity', action='count',
        help="Increase the verbosity of the logging output")
    cmds = args.add_subparsers(dest='cmd')
    
    list_cmd = cmds.add_parser('list', help="List all the avalible instances")
    list_cmd = list_cmd.add_argument('-t', '--tags', help="Tags to select on", default='')

    allocate = cmds.add_parser('allocate', help="Allocate instances to nodes")
    allocate.add_argument("--hosts", nargs=ZERO_OR_MORE, default=[],
        help="List of hosts to allocate to")
    allocate.add_argument("nodes", nargs=ZERO_OR_MORE, default=[],
        help="The nodes to allocate to hosts")
    
    audit = cmds.add_parser('audit', help="Compare live enviroment to config and note the diffrences")
    audit.add_argument("nodes", nargs=ZERO_OR_MORE, default=[],
        help="The nodes to allocate to hosts")

    start = cmds.add_parser('start', help="Start an instances")
    start.add_argument("hostname", help="The hostname of the instance to start")

    stop = cmds.add_parser('stop', help="Stop an instance")
    stop.add_argument("hostname", help="The hostname of the instance to stop")

    modify = cmds.add_parser('modify', help="Modify an instance")

    options = args.parse_args()

    if options.cmd is None:
        print("Error: No command specified", file=sys.stderr)
        args.print_usage()
        return UNKNOWN_COMMAND_EXIT

    if options.debug:
        import pdb
        import sys
        sys.excepthook = lambda  *_: pdb.pm()

    level = {
             1: logging.CRITICAL,
             2: logging.ERROR,
             3: logging.WARNING,
             4: logging.INFO,
             5: logging.DEBUG,
            }.get(options.verbosity, logging.DEBUG)

    debug = True if level <= logging.DEBUG else False

    if options.verbosity:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(level)
    log.info("Logging initialized")

    if not options.config:
        cwd = Path('.').resolve()
        for path in [cwd] + list(cwd.parents) + CONFIG_ORDER:
            root_dir = path
            path = Path(os.path.expanduser(str(path))) / 'fission.cfg'
            log.info("Checking for config file: %s", path)
            if path.exists():
                log.info("Opening config: %s", path)
                options.config = path.open('r')
                break
        else:
            log.info("No suitable configs found, using dummy config")
            options.config = StringIO("{}")
    else:
        root_dir = Path(options.config.name).parent
        root_dir = root_dir.resolve() # we want absolute paths for debugging
    
    log.info("Repository root dir: %s", root_dir)
    
    log.info("Loading config")
    loaded_config = load_yaml(options.config)
    loaded_config = loaded_config.get('fission', {})

    log.debug("Loaded config: %s", loaded_config)

    config = default_config.copy()
    config.update(loaded_config)

    log.debug("Config with defaults: %s", config)

    # it is important to note here that if config options are absolute path
    # then pathlib will negate the rootdir for us
    nodes_dir = str(root_dir / config['nodes_dir'])
    jobs_dir = str(root_dir / config['jobs_dir'])
    repo = YamlFS(nodes_dir, jobs_dir)

    nodes = repo.nodes
    jobs = repo.jobs
    
    log.info("Found %d node(s)", len(nodes))
    log.info("Found %d job(s)", len(jobs))
    
    from .tags import tagstring_to_tags, match_tags
    log.info("Applying tag selection to job and nodes")
    tags = tagstring_to_tags(options.tags)
    
    nodes = [node for node in nodes.values() if match_tags(tags, node.tags)]
    jobs = [job for job in jobs.values() if match_tags(tags, job.tags)]

    log.info("Found %d node(s) post tag selection", len(nodes))
    log.info("Found %d job(s) post tag selection", len(jobs))

    print("====== Nodes ======")
    for node in nodes:
        print(" * {node.hostname} ({node.fqdn})".format(node=node))
    print()
    print("====== Jobs =======")
    for job in jobs:
        print(" * {job.hostname} on {job.node}".format(job=job))

if __name__ == "__main__":
    sys.exit(main())
