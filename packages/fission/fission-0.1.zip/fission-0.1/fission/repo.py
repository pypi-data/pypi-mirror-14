#!/usr/bin/env python3
"""repo: funcions for building and maintaing an on disk fusion repo"""

# TODO:
# environ handling (insert them in the right place
# verify config files (dial in final format)
# work out if we want hosts entries

from yaml import safe_load as load_yaml, YAMLError
from collections import ChainMap, namedtuple
from pathlib import Path
import jinja2
import os

from . import log as _log

log = _log.getChild('repo')

Identifier = namedtuple("Identifier", "path, environ")
Job = namedtuple("Job", Identifier._fields + ('hostname', 'facts', 'hosts', 'node', 'tags'))
Node = namedtuple("Node", Identifier._fields + ('hostname', 'fqdn', 'facts', 'hosts', 'tags'))

DirSettings = namedtuple('DirSettings', 'hosts, environ, facts, tags')

class YamlFS:
    def __init__(self, node_dir, job_dir, hosts=[], environ={}, facts={}, tags=[],
                       environ_filename='environ.yml',
                       hosts_filename='hosts.yml',
                       facts_filename='facts.yml',
                       tags_filename='tags.yml'):
        """ 
        node_dir: Path to where the node data is stored
        job_dir: Path to where the job data is stored
        environ: Base enviroment that all nodes derive from
        facts: Used mainly for node selection and are not exported to the container
        *_filename: the on disk filename for facts/hosts/environs exported on a per der basis
        """
        self.node_dir = node_dir
        self.job_dir = job_dir
        self.nodes = {}
        self.jobs = {}

        # the 'or' is to ensure we dont share empty values between instances but recreate them
        self.hosts = hosts or []
        self.environ = environ or {}
        self.facts = facts or {}
        self.tags = tags or []

        self.environ_filename = environ_filename
        self.hosts_filename = hosts_filename
        self.facts_filename = facts_filename
        self.tags_filename = tags_filename

        self.load_nodes(node_dir, hosts, environ, facts, tags)
        self.load_jobs(job_dir, hosts, environ, facts, tags)


    def load_node(self, path, hosts, environ, facts, tags):
        conf, new_hosts, new_environ, new_facts, new_tags = self._load_conf(path, hosts, environ, facts, tags)

        if not conf_is_type(conf, 'node'):
            raise ValueError("Config file is not a node definition: " + path)

        results = []
        for key in ('hostname', 'address'):
            try:
                results.append(conf['node'][key])
            except KeyError as err:
                raise ValueError('key "{}" is missing in config'.format(key)) from err
        hostname, address = results

        new_tags.append('@{}'.format(hostname))
        new_tags.append('node')

        node = Node(path, new_environ, hostname, address, new_facts, new_hosts, new_tags)
        
        self.nodes[path] = node
        
        return node


    def load_nodes(self, path, hosts, environ, facts, tags):
        return self._load_confs(self.load_node, path, hosts, environ, facts, tags)


    def load_job(self, path, hosts, environ, facts, tags):
        log.info("Processing Job: " + path)
        conf, new_hosts, new_environ, new_facts, new_tags = self._load_conf(path, hosts, environ, facts, tags)

        if not conf_is_type(conf, 'job'):
            raise ValueError("Config file is not a job definition: " + path)

        results = []
        for key in ('hostname',):
            try:
                results.append(conf['job'][key])
            except KeyError as err:
                raise ValueError('key "{}" is missing in config'.format(key)) from err
        hostname, = results

        new_tags.append('@{}'.format(hostname))
        new_tags.append('job')

        file = Path(path)
        node_link = file.with_suffix('.node')
        if node_link.exists():
            node_conf = get_conf(node_link)

            if not conf_is_type(node_conf, 'node'):
                raise ValueError("Node link {} is not a link to a node manifest".format(node_link))

            try:
                node = node_conf['node']['hostname']
            except (KeyError, TypeError):
                raise ValueError("Node does not contain a valid config: " + str(node_link))
        else:
            node = None

        job = Job(path, new_environ, hostname, new_facts, new_hosts, node, new_tags)
        
        self.jobs[path] = job
        
        return job


    def load_jobs(self, path, hosts, environ, facts, tags):
        return self._load_confs(self.load_job, path, hosts, environ, facts, tags)
        

    def _load_conf(self, path, hosts, environ, facts, tags):
        """Loads a node from the specified path and merges its enviroment with the values supplied
        returns the loaded node
        
        path: the path to the yaml file to load
        hosts: the original hosts list to merge in
        environ: the original environ dict to merge in
        facts: the original facts dict to merge in
        """
        conf = get_conf(path) or {}
        extras = Path(path).with_suffix('.extras')
        if extras.exists():
            extras = get_conf(extras)
            log.info("Found extras file for %s at %s", path, extras)
        else:
            extras = {}

        if not isinstance(conf, dict):
            log.debug("file %s does not contain a dict", path)
            raise ValueError("Config file does not contain a dictonary: " + path)

        conf.update(extras)

        new_hosts = hosts.copy()
        new_hosts += conf.get('hosts', [])
        
        new_environ = environ.copy()
        new_environ.update(conf.get('environ', {}))
        keys = [key for key, val in new_environ.items() if val == "!"]
        for key in keys:
            del new_environ[keys]
        
        new_facts = facts.copy()
        new_facts.update(conf.get('facts', {}))
        
        new_tags = tags.copy()
        new_tags += conf.get('tags', [])

        return (conf, new_hosts, new_environ, new_facts, new_tags)


    def _load_confs(self, load_func, path, hosts=[], environ={}, facts={}, tags=[]):
        dir_settings = {}
        RootDirSettings = DirSettings(hosts, environ, facts, tags)
        
        for path, dirs, files in os.walk(path):
            log.info("Processing dir: %s", path)
            path = Path(path)
            
            # update host and environ and facts
            def conf_open(conf, key, *, default={}):
                filename = str(conf)
                if conf.exists():
                    log.info("Loading config: " + filename)
                    conf = get_conf(conf)
                    
                    if not isinstance(conf, dict):
                        raise ValueError("Config file is not a dictonary: " + filename)
                    
                    # multiple config files can be merged into one and are namespaced to
                    # avoid key conflicts, we need to remove this as 'hosts' is a list not
                    # a dict and the operations on lists are diffrent (think of case when default
                    # is returned, we cant do it outside this function as we would have to type
                    # check, easier to do it here and now)
                    if not conf_is_type(conf, key):
                        raise ValueError("Config file is not of type {}: {}".format(key, filename)) from err
                    conf = conf[key]
                else:
                    conf = default

                return conf
                
            # Welcome to the enrichment center
            parent = path.parent.parts
            parent_dir_settings = dir_settings.get(parent, RootDirSettings)
            
            dir_hosts = parent_dir_settings.hosts.copy()
            dir_hosts += conf_open(path / self.hosts_filename, 'hosts', default=[])
            dir_environ = parent_dir_settings.environ.copy()
            dir_environ.update(conf_open(path / self.environ_filename, 'environ'))
            dir_facts = parent_dir_settings.facts.copy()
            dir_facts.update(conf_open(path / self.facts_filename, 'facts'))
            dir_tags = parent_dir_settings.tags.copy()
            dir_tags += conf_open(path / self.tags_filename, 'tags', default=[])
            
            dir_settings[path.parts] = DirSettings(dir_hosts, dir_environ, dir_facts, dir_tags)
            
            for filename in files:
                # dont process special files
                if filename in {self.environ_filename, 
                                self.hosts_filename, 
                                self.facts_filename, 
                                self.tags_filename,
                                }:
                    continue
                    
                file = path / filename

                if file.suffix in ('.yaml', '.yml'):
                    log.info("Processing file: %s", file)
                    try:
                        load_func(str(file), dir_hosts, dir_environ, dir_facts, dir_tags)
                    except ValueError as err:
                        log.info("Encountered error while processing {}: {}".format(file, err))


def conf_is_type(conf, typ):
    """Check if the supplied config is of the type typ
    
    if typ is a list or tuple of types, then confirm that
    the supplied config provides all types
    """
    if isinstance(typ, str):
        if isinstance(conf, dict):
            return typ in conf
        else:
            return False
    else:
        all(conf_is_type(conf, typ) for x in typ)


def get_conf(path):
    with open(str(path)) as f:
        try:
            conf = load_yaml(f)
        except YAMLError as err:
            raise ValueError("Invalid yaml file: " + path) from err

    return conf


if __name__ == "__main__":
    # test YamlFS
    import sys
    import logging
    logging.basicConfig(level=logging.DEBUG)
    node_dir, job_dir = sys.argv[1:]    
    config = YamlFS(node_dir, job_dir)
    from pprint import pprint
    pprint(config.nodes)
    pprint(config.jobs)
