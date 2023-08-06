import mock
from nose.tools import with_setup
from os import remove
from os.path import exists
from os.path import join as pj

from pkglts.manage import (add_option, default_cfg, get_pkg_config, init_pkg,
                           regenerate, write_pkg_config)

from .small_tools import ensure_created, rmdir


tmp_dir = 'toto_mg_rg'
init_file = pj(tmp_dir, "src", "toto", "__init__.py")
pkg_cfg = dict(default_cfg)
pkg_cfg = add_option("base", pkg_cfg)


def addendum():
    """ modify init_file in first pkglts div
    """
    with open(init_file, 'r') as f:
        lines = f.read().splitlines()

    lines.insert(1, "addendum")

    with open(init_file, 'w') as f:
        f.write("\n".join(lines))


def setup():
    ensure_created(tmp_dir)
    init_pkg(tmp_dir)
    pkg_cfg['base']['pkgname'] = 'toto'
    regenerate(pkg_cfg, tmp_dir)


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_pass():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    assert exists(init_file)


@with_setup(setup, teardown)
def test_regenerate_check_pkg_cfg_validity():
    pkg_cfg['base']['pkgname'] = '1toto'
    assert not regenerate(pkg_cfg, tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_keep():
    with open(init_file, 'w') as f:
        f.write("modified")

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=False):
        regenerate(pkg_cfg, tmp_dir)

    with open(init_file, 'r') as f:
        assert f.read() == "modified"


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_overwrite():
    addendum()

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=True):
        regenerate(pkg_cfg, tmp_dir)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_handle_global_overwrite():
    addendum()

    regenerate(pkg_cfg, tmp_dir, overwrite=True)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_new_files_do_not_generate_conflicts():
    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate(pkg_cfg, tmp_dir)

    assert exists(new_pth)
    with open(new_pth, 'r') as f:
        txt = f.read()
        assert txt == "txt = 'addendum'"


@with_setup(setup, teardown)
def test_regenerate_remove_user_files_do_not_generate_conflicts():
    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate(pkg_cfg, tmp_dir)

    remove(new_pth)

    regenerate(pkg_cfg, tmp_dir)
    assert not exists(new_pth)


@with_setup(setup, teardown)
def test_regenerate_fail_if_permanent_templated_section_has_been_modified():
    with open(init_file, 'r') as f:
        lines = f.readlines()

    # lines.insert(1, "a = 1")
    del lines[2:]

    with open(init_file, 'w') as f:
        f.write("\n".join(lines))

    assert not regenerate(pkg_cfg, tmp_dir, overwrite=True)


@with_setup(setup, teardown)
def test_regenerate_do_not_touch_pkglts_cfg_files():
    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("{{key, base.pkgname}}")

    cfg = get_pkg_config(tmp_dir)
    cfg['extra'] = dict(toto="{{key, base.pkgname}}")
    write_pkg_config(cfg, tmp_dir)

    regenerate(pkg_cfg, tmp_dir)
    with open(new_pth, 'r') as f:
        txt = f.read()
        assert txt == "toto"

    cfg = get_pkg_config(tmp_dir)
    assert cfg['extra']['toto'].template == "{{key, base.pkgname}}"
