import operator as op
import re
import subprocess
import argparse
import os

from tornado import template
from yaml import CLoader
from yaml import load


def parse(args):
    parser = argparse.ArgumentParser('help')
    parser.add_argument('-c', default="Rumblerfile.yml", dest='conf')
    parser.add_argument('cmd', help="command to run")
    parser.add_argument('rest', nargs='*')
    namespace = parser.parse_args(args)
    return namespace

def main(args=None):
    ns = parse(args)
    src = get_src(ns.conf)
    rumble = Rumbler(src)
    cmd = rumble.cmd(ns.cmd, ' '.join(ns.rest))
    return subprocess.call(cmd, shell=True)


def get_src(fname):
    with open(os.path.join(os.getcwd(), fname)) as f:
        return '\n'.join(list(f))
    

class Rumbler(object):

    def __init__(self, src):
        self.src = src

    def cmd(self, command, rest=None):
        data = load(interpolate(self.src))
        node = data[command]
        joiner = data.get('__config', {}).get('joiner', {})
        args = filter(op.truth, [
            node['cmd'],
            build_arg('short', node, joiner),
            build_arg('long', node, joiner),
            build_args(node),
            rest
        ])
        return ' '.join(args)

def interpolate(src):
    meta = load(src).get('__meta', {})
    meta = { key: shell(value) for (key, value) in meta.items() }
    t = template.Template(src)
    return t.generate(**meta)

def shell(arg):
    cmd = get_shell_cmd(arg)
    if cmd:
        return sh(cmd)
    return arg

def sh(arg):
    out =  subprocess.check_output(arg, shell=True)
    return out.strip()

def get_shell_cmd(arg):
    cmd = False
    matched = re.search(r"^\$\((.+)\)$", str(arg))
    if matched:
        cmd =  matched.group(1)
    return cmd

    
prefixes = {
    'short': '-',
    'long': '--'
}

def build_args(node):
    args = node.get('args', [])
    return ' '.join(args)
    

def build_arg(prefix_name, node, joiner):
    opt = node.get(prefix_name, None)
    flag_prefix = prefixes.get(prefix_name)
    if not opt:
        return None

    joinsep = ' '
    flags = sorted(map(compact, opt.items()))
    args = [flag_prefix + joinby(pair, joiner) for pair in flags]
    return ' '.join(args)

def joinby(items, joiner):
    type = items[0]
    sep = joiner.get(type, ' ')
    node_stringer = lambda item: stringer(item, sep)
    return ' '.join(map(node_stringer, items))

def stringer(item, sep):
    if type(item) is dict:
        pairs = sorted(["{1}{0}{2}".format(sep, *pair) for pair in item.items()])
        return ' '.join(pairs)
    return str(item)

def compact(items):
    return filter(op.truth, items)


if __name__ == '__main__':
    main()
