from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    project = env['readthedocs']['project']
    project = project.replace(".", "")

    url = "%s.readthedocs.org/en/latest/?badge=latest" % project
    img = "readthedocs.org/projects/%s/badge/?version=latest" % project
    return fmt_badge(img, url, "Documentation status")


mapping = {'readthedocs.badge': badge}
