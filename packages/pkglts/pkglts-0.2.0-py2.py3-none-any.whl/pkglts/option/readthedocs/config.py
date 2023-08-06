parameters = [
    ("project", "{{key, github.project}}")
]


def check(pkg_cfg):
    """Check the validity of parameters in package configuration.

    args:
     - pkg_cfg (dict of str, dict of str, any)): package configuration

    return:
     - (list of str): list of faulty parameters
    """
    invalids = []
    project = pkg_cfg['readthedocs']['project']

    if len(project) == 0:
        invalids.append("project")

    return invalids
