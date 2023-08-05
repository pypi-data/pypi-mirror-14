#!/usr/bin/env python

import os
import os.path
import stat
import re
import pkg_resources
from jinja2 import Environment, FileSystemLoader

def init_template(template, pkgname, description=None):
    # test if directory exists

    #name = "only letters up and lower case, no - and _"
    name = pkgname.lower()

    path = os.path.join('template', template)
    templatepath = pkg_resources.resource_filename(__name__, path)
    if not os.path.isdir(templatepath):
        print 'The template, %s, does not exist' % template
        print '(Directory does not exist %s)' % templatepath
        print 'Try any of the following: %s' % ", ".join(_templates())
        return 1

    env = Environment()
    templatevars = {
        'pkgname' : pkgname,
        'name' : name,
        'description' : '%s description' % pkgname
    }
    if description:
        templatevars['description'] = description

    topdir = name
    os.mkdir(topdir)

    for (dirpath, dirnames, filenames) in os.walk(templatepath, topdown=True):
        relpath = dirpath[len(templatepath):]
        if relpath.startswith('/'):
            relpath = relpath[1:]

        for templatedir in dirnames:
            outdir = os.path.join(topdir, relpath, templatedir)
            outdir = outdir.replace('__name__', name)
            os.mkdir(outdir)

        loader = FileSystemLoader(dirpath)
        for templatename in filenames:
            template = loader.load(env, templatename)
            outfile = template.render(**templatevars)
            outpath = os.path.join(topdir, relpath, templatename)
            outpath = outpath.replace('__name__', name)
            suffix = ".jinja"
            if outpath.endswith(suffix):
                outpath = outpath[:-len(suffix)]

            with open(outpath, 'w') as f:
                f.write(outfile)

            # make build script executable
            if templatename == "build.sh":
                st = os.stat(outpath)
                os.chmod(outpath, st.st_mode | stat.S_IEXEC)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Canary User modules')
    parser.add_argument('-t', '--template',
        choices=_templates(),
        default='tcp',
        help='User module template')
    parser.add_argument('-d', '--description',
        help='Description of module'
    )
    parser.add_argument('name', help='User module name (eg. DHCPExample)')
    args = parser.parse_args()

    if not re.match('[a-zA-Z0-9]{1,10}', args.name):
        print "Name should consist of only digits and characters"
        return 1

    init_template(args.template, args.name, args.description)

def _templates():
    return pkg_resources.resource_listdir(__name__, 'template')
