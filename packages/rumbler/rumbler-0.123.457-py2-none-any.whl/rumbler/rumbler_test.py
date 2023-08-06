import os

from yaml import load
from yaml import CLoader
from pytest import mark

from rumbler import Rumbler
import rumbler


def test_cmd():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_cmd')
    assert cmd == 'docker run'


def test_cmd_with_short_options():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_short')
    assert cmd == 'docker run -i -t'

def test_cmd_with_short_options_and_x():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_short_x')
    assert cmd == 'docker run -x abc'

def test_cmd_with_short_options_and_x_and_y():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_short_x_y')
    assert cmd == 'docker run -x abc -y'

def test_cmd_with_long_options():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_long')
    assert cmd == 'docker run --rm'

def test_cmd_with_long_options_and_foo():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_long_foo')
    assert cmd == 'docker run --foo abc --rm'

def test_cmd_with_mix_options():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_mix')
    assert cmd == 'docker run -a -b bee -c --bar xyz --foo abc --rm'

def test_cmd_volume():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_volume')
    assert cmd == 'docker run --volume foo:/bar two:/too'

def test_cmd_with_joiner():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_joiner')
    assert cmd == 'docker run -v three:3 --number one-:-1 two-:-2'

def test_cmd_interpolation():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_interpolation')
    assert cmd == 'docker run --version v0.123@tip'

def test_shell_meta():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_shell_meta')
    assert cmd == 'docker run --path helloworld'


def test_get_shell_cmd():
    assert rumbler.get_shell_cmd("$(echo 1 2 3)") == 'echo 1 2 3'
    assert rumbler.get_shell_cmd("$($bar)") == '$bar'
    assert rumbler.get_shell_cmd("$()") == False
    assert rumbler.get_shell_cmd(" $()") == False
    assert rumbler.get_shell_cmd("$() ") == False
    assert rumbler.get_shell_cmd(123) == False

def test_args():
    src = get_sample_src()
    rum = Rumbler(src)
    cmd = rum.cmd('test_args')
    assert cmd == 'docker run duck/rumbler sh'


def test_parse():
    args = "runx hello there".split()
    ret = rumbler.parse(args)
    assert ret.conf == "Rumblerfile.yml"
    assert ret.cmd == "runx"
    assert ret.rest == ["hello", "there"]


def test_get_src_relative_dir(tmpdir):
    fname = 'Rumblerfile.yml'
    with tmpdir.as_cwd():
        f = tmpdir.join(fname)
        f.write('hello')
        src = rumbler.get_src(fname)
        assert src == 'hello'


def test_main(tmpdir):
    cmd = 'runx foo bar'.split()
    lines = get_sample_src('Rumblerfile.runx.yml')
    target = 'src/Rumblerfile.runx.yml'
    with tmpdir.as_cwd():
        f = tmpdir.join('Rumblerfile.yml')
        f.write(lines)
        ret = rumbler.main(cmd)
        assert ret == 0

def test_sample():
    with open(os.path.join(os.path.dirname(__file__), 'sample.yml')) as f:
        src = '\n'.join(list(f))
        data = load(src)
        assert data['__meta']['version'] == 'v0.123'


def get_sample_src(fname=None):
    if not fname:
        fname = 'sample.yml'
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        src = '\n'.join(list(f))
        return src
