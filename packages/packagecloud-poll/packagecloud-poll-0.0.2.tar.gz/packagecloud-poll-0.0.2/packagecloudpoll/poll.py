"""packagecloud-poll

Packagecloud-poll repeatedly polls the packagecloud API, looking for a specific package filename to appear. It is
intended to be used in continuous integration/continuous deployment scenarios where we want to block until we are sure
a package has been indexed and is avaiable before continuing.

All arguments are mandatory except for --timeout, --poll_interval, --page_interval and --log-level.

Increased productivity gains high favour from the machine god.

Usage:
    packagecloud-poll --user user --repo repo_name --type type --distro distro --distro_version distro_version --arch arch --pkg_name pkg_name --filename filename [--timeout timeout] [--poll_interval interval] [--page_interval interval] [--log-level log_level]
    packagecloud-poll --help
    packagecloud-poll --version

Options:
    --user <user>                      Packagecloud user.
    --repo <repo_name>                 Packagecloud repository.
    --type <type>                      Package type. (i.e. rpm or deb)
    --distro <distro>                  Package distro. (i.e. ubuntu)
    --distro_version <distro_version>  Package distro version. (i.e. precise)
    --arch <arch>                      Package arch. (i.e. amd64 or x86_64)
    --pkg_name <pkg_name>              Name of the package to poll for.
    --filename <filename>              File name of the package to poll for. (i.e mystuff_v5.3_precise_amd64.deb)
    --timeout <timeout>                Time in seconds to poll for [default: 600].
    --poll_interval <interval>         Polling interval in seconds [default: 30].
    --page_interval <interval>         API pagination interval. Adjust if you are worried about hitting the packagecloud API too fast. [default: 1].
    --log-level <log_level>            Set output log level. One of DEBUG, INFO, WARN, ERROR or CRITICAL [default: INFO].
    --help                             Show this screen.
    --version                          Show version.

"""

import logging
import sys
from datetime import datetime

from docopt import docopt, DocoptExit

import config
import pkgcloudapi
import utils
from ._version import __version__


def main():
    # Load args
    try:
        args = docopt(__doc__, version=__version__)
    except DocoptExit as ex:
        # Sadly, docopt doesn't return exactly which argument was invalid.
        sys.stderr.write('[{}] ERROR: Invalid argument.\n\n{}'.format(datetime.now(), ex))
        sys.exit(1)

    # Set up logger
    logger = logging.getLogger(__package__)
    log_level = getattr(logging, args['--log-level'].upper(), None)

    # if log_level is DEBUG, set it for everything so Requests will log what
    # it's doing too. Else just configure logger the normal way.
    if log_level == logging.DEBUG:
        logging.basicConfig(
            level=log_level,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        try:
            logger.setLevel(log_level)
        except TypeError:
            sys.stderr.write('[{}] ERROR: Invalid log level specified: {}'.format(datetime.now(), args['--log-level']))
            sys.exit(1)

    try:
        # validate command line args and check environment variables
        args = config.validate_args(args)
        env = config.load_env()

        # engage
        logger.info("ENGAGE")
        logger.debug("Using arguments: \n{}".format(args))

        if pkgcloudapi.look_for_package(env, args):
            logger.info("Success. Found filename {}.".format(args['--filename']))
        else:
            utils.abort("Filename {} was not found during polling period.".format(args['--filename']))
    except KeyboardInterrupt:
        logger.info("\nOkay, bye.\n")
        sys.exit(130)

    # Done
    sys.exit(0)
