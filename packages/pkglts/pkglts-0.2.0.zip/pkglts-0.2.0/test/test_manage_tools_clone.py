from nose.tools import with_setup
from os import listdir
from os.path import exists, getsize
from os.path import join as pj

from pkglts.manage_tools import clone_base_option

from .small_tools import ensure_created, rmdir


tmp_dir = "takapouet_clone"
pkg_cfg = dict(base={'pkgname': 'toto', 'namespace': None})
init_file = pj(tmp_dir, "src", "toto", "__init__.py").replace("\\", "/")


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


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_clone_does_not_complain_if_option_not_defined():
    clone_base_option('toto', {}, {}, tmp_dir, {})
    assert len(listdir(tmp_dir)) == 0


@with_setup(setup, teardown)
def test_clone_copy_files_from_pkg_data():
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    assert len(listdir(tmp_dir)) > 0
    assert exists(init_file)


@with_setup(setup, teardown)
def test_clone_copy_binary_files_from_pkg_data():
    clone_base_option('for_testing_purpose', pkg_cfg, {}, tmp_dir, {})
    assert len(listdir(tmp_dir)) > 0
    assert exists(init_file)
    assert exists(pj(tmp_dir, "src", "toto", "ext_data.png"))


@with_setup(setup, teardown)
def test_clone_do_overwrite_existing_files_by_default():
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    bin_file = pj(tmp_dir, "src", "toto", "ext_data.png")
    with open(bin_file, 'w') as f:
        f.write("")

    addendum()
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    clone_base_option('for_testing_purpose', pkg_cfg, {}, tmp_dir, {})
    with open(init_file, 'r') as f:
        txt = f.read()
        assert "addendum" not in txt

    assert getsize(bin_file) > 0


@with_setup(setup, teardown)
def test_clone_can_force_no_overwrite_of_existing_files():
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    addendum()
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {init_file: False})
    with open(init_file, 'r') as f:
        txt = f.read()
        assert "addendum" in txt


@with_setup(setup, teardown)
def test_clone_overwrite_only_pkglts_divs():
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    with open(init_file, 'a') as f:
        f.write("addendum")

    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    with open(init_file, 'r') as f:
        txt = f.read()
        assert "addendum" in txt


@with_setup(setup, teardown)
def test_clone_returns_list_of_files_with_missing_pkglts_divs():
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    with open(init_file, 'w') as f:
        f.write("modified")

    error_files = clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    assert len(error_files) > 0
    assert error_files[0] == init_file


@with_setup(setup, teardown)
def test_clone_handles_namespace():
    pkg_cfg = dict(base={'pkgname': 'toto', 'namespace': 'oa'})
    clone_base_option('base', pkg_cfg, {}, tmp_dir, {})
    assert not exists(init_file)

    assert exists(pj(tmp_dir, 'src', 'oa', 'toto', '__init__.py'))
    assert exists(pj(tmp_dir, 'src', 'oa', '__init__.py'))
