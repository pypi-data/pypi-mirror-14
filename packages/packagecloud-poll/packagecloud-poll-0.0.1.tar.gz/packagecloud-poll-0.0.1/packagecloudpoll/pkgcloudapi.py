import logging
import time
from datetime import datetime

from requests import Session, Request, HTTPError, ConnectionError, Timeout
from requests.exceptions import RequestException

import utils

# logger
logger = logging.getLogger(__package__)


def pkgcloud_api_call(url, method, **kwargs):
    """
    Generic method to make HTTP requests to packagecloud
    """
    resp = None
    attempt = 0
    req = Request(method.upper(), url, **kwargs)

    while True:
        try:
            attempt += 1
            resp = Session().send(
                Session().prepare_request(req), verify=True)
            resp.raise_for_status()
            break
        except (HTTPError, ConnectionError, Timeout) as ex:
            if attempt >= 5:
                utils.abort(ex.message)
            else:
                time.sleep(3)
                continue
        except RequestException as ex:
            utils.abort(ex.message)

    try:
        if "error" in resp.json():
            raise Exception('{}'.format(resp.json()['error']))
        return resp
    except ValueError as ex:
        utils.abort("Unexpected response from packagecloud API. "
                    "Expected json, got something else: {}".format(ex.message))
    except Exception as ex:
        utils.abort("Error making packagecloud API call: {}".format(ex.message))


def look_for_package(env, args):
    """
    Iterates though package versions, looking for --filename.
    """

    # set up request
    request_page_size = 50
    initial_url = "{}/repos/{}/{}/package/{}/{}/{}/{}/{}/versions.json?per_page={}".format(
        env['url_base'],
        args['--user'],
        args['--repo'],
        args['--type'],
        args['--distro'],
        args['--distro_version'],
        args['--pkg_name'],
        args['--arch'],
        request_page_size
    )

    start_time = datetime.now()
    logger.info("Starting to poll Packagecloud. Timeout is {}s.".format(args['--timeout']))

    # poll until we see the filename we want, or timeout exceeds
    while (datetime.now() - start_time).seconds <= args['--timeout']:
        # fetch the first page of the collection
        resp = pkgcloud_api_call(initial_url, 'get')
        total_items = resp.headers['total']
        logger.debug('  Packagecloud API reports {} total items.'.format(total_items))

        # examine the response and paginate through rest of collection if there are more pages
        while True:
            if any(pkg['filename'] == args['--filename'] for pkg in resp.json()):
                return True

            try:
                if resp.links['next']:
                    fetchurl = resp.links['next']['url'].replace(
                            'packagecloud.io/', "{}:@packagecloud.io/".format(env['token']))
                    logger.debug('  fetching next page')
                    resp = pkgcloud_api_call(fetchurl, 'get')
                    time.sleep(1)
            except KeyError:
                logger.debug('  no more pages')
                break

        # didn't find what we want, so sleep for poll_interval seconds and then try again.
        logger.debug("  sleeping")
        time.sleep(args['--poll_interval'])
        logger.info("  been searching for {} seconds".format((datetime.now() - start_time).seconds))
    else:
        logger.error("Poll timeout has exceeded.")
    return False

