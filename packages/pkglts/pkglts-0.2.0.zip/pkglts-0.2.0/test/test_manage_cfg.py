from base64 import b64encode
from nose.tools import with_setup
from hashlib import sha512
from os import listdir
from os.path import join as pj

from pkglts.manage import (get_pkg_config, get_pkg_hash,
                           init_pkg,
                           write_pkg_config)

from .small_tools import ensure_created, rmdir


tmp_dir = 'toto_manage_cfg'


def setup():
    ensure_created(tmp_dir)
    init_pkg(tmp_dir)


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_manage_init_create_pkg_config():
    # init_pkg(tmp_dir)
    cfg = get_pkg_config(tmp_dir)
    assert cfg is not None
    assert "_pkglts" in cfg


@with_setup(setup, teardown)
def test_manage_init_create_pkg_hash():
    init_pkg(tmp_dir)
    hm = get_pkg_hash(tmp_dir)
    assert hm is not None


@with_setup(setup, teardown)
def test_manage_init_protect_pkglts_dir_from_modif():
    assert "regenerate.no" in listdir(pj(tmp_dir, ".pkglts"))
    assert "clean.no" in listdir(pj(tmp_dir, ".pkglts"))


@with_setup(setup, teardown)
def test_manage_pkg_config():
    cfg = dict(toto={'toto': 1})
    write_pkg_config(cfg, tmp_dir)
    new_cfg = get_pkg_config(tmp_dir)
    assert new_cfg == cfg


@with_setup(setup, teardown)
def test_manage_pkg_config_fmt_templates():
    cfg = dict(base={'pkg': 'custom'},
               toto={'base': 10, 'toto': "{{key, base.pkg}}"})
    write_pkg_config(cfg, tmp_dir)

    cfg = get_pkg_config(tmp_dir)['toto']
    assert 'base' in cfg
    assert 'toto' in cfg
    assert cfg['toto'] == "custom"


@with_setup(setup, teardown)
def test_manage_cfg_store_any_item():
    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))

    cfg = dict(simple=1,
               txt="lorem ipsum\n" * 4,
               hash=b64encode(algo.digest()).decode('utf-8'))

    write_pkg_config(dict(toto=cfg), tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)['toto']
    assert new_cfg == cfg

    algo = sha512()
    algo.update(("lorem ipsum\n" * 10).encode("latin1"))
    sha = b64encode(algo.digest()).decode('utf-8')
    assert sha == new_cfg['hash']


@with_setup(setup, teardown)
def test_manage_cfg_do_store_private_item():
    cfg = {'toto': {}, '_toto': {}}
    write_pkg_config(cfg, tmp_dir)

    new_cfg = get_pkg_config(tmp_dir)
    assert '_toto' in new_cfg


@with_setup(setup, teardown)
def test_manage_cfg_restore_templates_on_writing():
    cfg = dict(base={'pkg': 'custom'},
               toto={'base': 10, 'toto': "{{key, base.pkg}}"})
    write_pkg_config(cfg, tmp_dir)

    pkg_cfg = get_pkg_config(tmp_dir)
    assert pkg_cfg['toto']['toto'] == "custom"

    pkg_cfg['base']['pkg'] = "another"
    write_pkg_config(pkg_cfg, tmp_dir)

    pkg_cfg = get_pkg_config(tmp_dir)
    assert pkg_cfg['toto']['toto'] == "another"
