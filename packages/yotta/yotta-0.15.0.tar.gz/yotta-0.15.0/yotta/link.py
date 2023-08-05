# Copyright 2014-2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

def addOptions(parser):
    parser.add_argument('component', default=None, nargs='?',
        help='Link a globally installed (or globally linked) module into '+
             'the current module\'s dependencies. If ommited, globally '+
             'link the current module.'
    )

def execCommand(args, following_args):
    # standard library modules, , ,
    import logging
    import os

    # colorama, BSD 3-Clause license, color terminal output, pip install colorama
    import colorama

    # validate, , validate things, internal
    from yotta.lib import validate
    # folders, , get places to install things, internal
    from yotta.lib import folders
    # fsutils, , misc filesystem utils, internal
    from yotta.lib import fsutils

    c = validate.currentDirectoryModule()
    if not c:
        return 1
    if args.component:
        err = validate.componentNameValidationError(args.component)
        if err:
            logging.error(err)
            return 1
        fsutils.mkDirP(os.path.join(os.getcwd(), 'yotta_modules'))
        src = os.path.join(folders.globalInstallDirectory(), args.component)
        dst = os.path.join(os.getcwd(), 'yotta_modules', args.component)
        # if the component is already installed, rm it
        fsutils.rmRf(dst)
    else:
        fsutils.mkDirP(folders.globalInstallDirectory())

        src = os.getcwd()
        dst = os.path.join(folders.globalInstallDirectory(), c.getName())

    broken_link = False
    if args.component:
        realsrc = fsutils.realpath(src)
        if src == realsrc:
            broken_link = True
            logging.warning(
              ('%s -> %s -> ' % (dst, src)) + colorama.Fore.RED + 'BROKEN' + colorama.Fore.RESET #pylint: disable=no-member
            )
        else:
            logging.info('%s -> %s -> %s' % (dst, src, realsrc))
        # check if the thing we linked is actually a dependency, if it isn't
        # warn about that. To do this we may have to get the current target
        # description. This might fail, in which case we warn that we couldn't
        # complete the check:
        target = c.getTarget(args.target, args.config)
        if target:
            if not c.hasDependencyRecursively(args.component, target=target, test_dependencies=True):
                logging.warning(
                    '"%s" is not installed as a dependency, so will not '+
                    ' be built. Perhaps you meant to "yotta install %s" '+
                    'first?',
                    args.component,
                    args.component
                )
        else:
            logging.warning(
                'Could not check if linked module "%s" is installed as a '+
                'dependency, because target "%s" is not available. Run '
                '"yotta ls" to check.',
                args.component,
                args.target
            )
    else:
        logging.info('%s -> %s' % (dst, src))

    try:
        fsutils.symlink(src, dst)
    except Exception as e:
        if broken_link:
            logging.error('failed to create link (create the first half of the link first)')
        else:
            logging.error('failed to create link: %s', e)

