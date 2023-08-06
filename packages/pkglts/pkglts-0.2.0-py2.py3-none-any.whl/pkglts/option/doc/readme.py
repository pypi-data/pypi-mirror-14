# def fmt_badge(badge, url, txt):
#     lines = [".. image:: https://%s" % badge,
#              "    :alt: %s" % txt,
#              "    :target: https://%s" % url]
#     return "\n".join(lines)
#
#
# def badges(txt, env):  # TODO: maybe not the right place for badge knowledge
#     """ Produce relevant image links to include web services badges
#     """
#     if 'github' not in env:
#         return txt
#
#     owner = env['base']['owner']
#     pkgname = env['base']['pkgname']
#     project = env['github']['project']
#
#     items = []
#     if 'readthedocs' in env:
#         badge = "readthedocs.org/projects/%s/badge/?version=latest" % project
#         url = "%s.readthedocs.org/en/latest/?badge=latest" % project
#         items.append(fmt_badge(badge, url, "Documentation status"))
#
#     if 'travis' in env:
#         url = "travis-ci.org/%s/%s" % (owner, project)
#         badge = url + ".svg?branch=master"
#         items.append(fmt_badge(badge, url, "Travis build status"))
#
#     if 'coveralls' in env:
#         badge = ("coveralls.io/repos/%s/%s/" % (owner, project) +
#                  "badge.svg?branch=master&service=github")
#         url = "coveralls.io/github/%s/%s?branch=master" % (owner, project)
#         items.append(fmt_badge(badge, url, "Coverage report status"))
#
#     if 'landscape' in env:
#         url = "landscape.io/github/%s/%s/master" % (owner, project)
#         badge = url + "/landscape.svg?style=flat"
#         items.append(fmt_badge(badge, url, "Code health status"))
#
#     if 'pypi' in env:
#         url = "badge.fury.io/py/%s" % pkgname
#         badge = url + ".svg"
#         items.append(fmt_badge(badge, url, "PyPI version"))
#
#     if len(items) == 0:
#         return txt
#     else:
#         return "\n\n" + "\n\n".join(items) + "\n"
