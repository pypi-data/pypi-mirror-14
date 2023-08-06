from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    owner = env['base']['owner']
    project = env['github']['project']

    url = "travis-ci.org/%s/%s" % (owner, project)
    img = url + ".svg?branch=master"
    return fmt_badge(img, url, "Travis build status")


def pyversions(txt, env):
    del txt  # unused
    intended_versions = env['pysetup']['intended_versions']
    items = ['   - "%s.%s"' % (ver[0], ver[1]) for ver in intended_versions]
    return "\n".join(items)


mapping = {'travis.badge': badge,
           'travis.pyversions': pyversions}
