#!/usr/bin/env python
# coding=utf-8
"""Watch Torrent RSS feeds and download new torrent files.
"""
from __future__ import print_function
import os
import sys
import click
import json
import hashlib
import requests
import feedparser
import time
import copy

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
__config__ = '~/.blacksap.cfg'
debug = False
http_header = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
               }


def read_cfg():
    """Load the config file

    :return: Dictionary
    """
    global debug, __config__
    if os.path.exists(os.path.expanduser(__config__)):
        with open(os.path.expanduser(__config__)) as f:
            cfg = json.load(f)
        return cfg
    else:
        return {'feeds': []}


def write_cfg(cfg):
    """Write config dictionary to config file

    :param cfg: Dictionary of items to write
    :return: True or Exception
    """
    global debug, __config__
    with open(os.path.expanduser(__config__), 'w') as f:
        json.dump(cfg, f, indent=4)
    return True


def ttl_expired(timestamp, ttl):
    """Is the current cache expired

    :param timestamp: Last time the feed was checked.
    :param ttl: Amount of time for cache to be considered valid (in seconds)
    """
    global debug
    if timestamp is None:
        return True
    now = int(time.time())
    if now - timestamp > ttl:
        return True
    else:
        return False


def get_torrent_file(url, destination, filename):
    """Attempt to download a torrent file to a destination

    :param url: URL of torrent file
    :param destination: POSX path to output location
    :param filename: Name of the output file
    :return: True or False
    """
    global debug, http_header
    if url.startswith('http') is False:
        return False, 'Not a url: ' + url
    if '?' in url:
        short_url = str(url.split('?')[0])
    else:
        short_url = url
    result = requests.get(short_url, headers=http_header)
    if result.status_code == 200:
        with open(destination + filename, 'wb') as torrentfile:
            torrentfile.write(result.content)
        return True, 'Downloaded: ' + filename
    else:
        if debug:
            return False, 'Unable to download: ' + filename + ' ' + str(result.status_code)
        else:
            return False, 'Unable to download: ' + filename + ' ' + str(result.status_code)


def download_rss_feed(url):
    """ Download a given RSS feed and return the resulting dictionary
    :param url: Url to RSS feed
    :return: rss_feed, rss_hash,
    """
    global debug, http_header
    if debug:
        click.echo('Attempting to download RSS Feed: ' + url)
    try:
        rss_feed_raw = requests.get(url, timeout=5, headers=http_header)
        if rss_feed_raw.url != url:  # A redirect occurred
            url = rss_feed_raw.url
            rss_feed_raw = requests.get(url, timeout=5, headers=http_header)
        rss_feed_raw = rss_feed_raw.text
    except requests.exceptions.Timeout:
        raise requests.HTTPError('Unable to download: ' + url)
    if debug:
        click.echo('RSS feed downloaded successfully')
    rss_feed = feedparser.parse(rss_feed_raw)
    rss_hash = hashlib.md5(rss_feed_raw.encode('utf-8')).hexdigest()
    return rss_feed, rss_hash


@click.group()
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
@click.version_option()
def cli(**opts):
    """Manage RSS Torrent feeds to feed Transmission
    """
    global debug
    debug = opts['debug']


@cli.command()
@click.argument('urls', nargs=-1)
def reset(urls):
    """Clear the hash, last, and ttl fields from one or all feeds
    """
    global debug
    cfg = read_cfg()
    if len(cfg['feeds']) == 0:
        click.secho('No feeds being tracked', fg='red', err=True)
    else:
        for feed in cfg['feeds']:
            if len(urls) > 0:
                if feed['url'] in urls:
                    feed['hash'] = None
                    feed['last'] = None
                    feed['ttl'] = None
                    click.secho('Cache cleared for: ' + feed['url'], fg='green')
            else:
                feed['hash'] = None
                feed['last'] = None
                feed['ttl'] = None
        write_cfg(cfg)
        if len(urls) == 0:
            click.secho('All caches cleared', fg='green')
    return 0


@cli.command()
@click.argument('urls', nargs=-1, required=True)
def track(urls):
    """Add RSS feed(s) to tracking
    """
    global debug
    cfg = read_cfg()
    cfg_urls = [x['url'] for x in cfg['feeds']]
    for url in urls:
        if url in cfg_urls:
            click.secho('RSS feed already exists!', fg='red', err=True)
            continue
        else:
            try:
                rss_feed, rss_hash = download_rss_feed(url)
            except requests.HTTPError:
                click.secho('Unable to download: ' + url, fg='red', err=True)
                continue
            feed = dict()
            feed['name'] = rss_feed['feed']['title']
            feed['url'] = url
            feed['hash'] = None
            feed['last'] = None
            feed['ttl'] = None
            feed['new'] = True
            cfg['feeds'].append(feed)
            write_cfg(cfg)
            click.secho('Added RSS feed: ' + feed['name'], fg='green')
    return 0


@cli.command()
@click.argument('urls', nargs=-1, required=True)
def untrack(urls):
    """Stop tracking RSS feed(s)
    """
    global debug
    cfg = read_cfg()
    cfg_urls = [x['url'] for x in cfg['feeds']]
    for url in urls:
        if url in cfg_urls:
            cfg['feeds'] = [x for x in cfg['feeds'] if x['url'] != url]
            click.secho('Untracked RSS feed: ' + url, fg='yellow')
        else:
            click.secho('RSS feed is not being tracked: ' + url, fg='red', err=True)
    write_cfg(cfg)
    click.echo('Finished untracking feed(s)')
    return 0


@cli.command()
def tracking():
    """List tracked RSS feeds
    """
    global debug
    cfg = read_cfg()
    if len(cfg['feeds']) == 0:
        click.secho('Zero feeds tracked', fg='green')
        return 0
    else:
        click.secho(str(len(cfg['feeds'])) + ' feeds tracked', fg='green')
        for feed in cfg['feeds']:
            click.echo('-' * 20)
            click.echo('Name: ' + feed['name'])
            click.echo('URL: ' + feed['url'])
    return 0


@cli.command()
@click.option('--count', '-c', default=-1, help='Number of torrent files to download')
@click.option('--force', '-F', is_flag=True, help='Force a new download of the RSS feed')
@click.option('--ttl', '-T', default=600, help='TTL for cache in seconds')
@click.option('--reverse', '-R', is_flag=True, help='Read the feeds in reverse order (oldest to newest)')
@click.option('--output', '-o', type=click.Path(exists=True, file_okay=False, writable=True), required=True,
              help='Directory to download torrent files to')
@click.argument('urls', nargs=-1)
def run(**opts):
    """Check all tracked feeds for new content and download torrent files as needed

    DEFAULTS:

        count = -1 (all)
        ttk = 600
    """
    global debug
    cfg = read_cfg()

    if len(cfg['feeds']) == 0:
        click.secho('Zero feeds being tracked', fg='red', err=True)
        return 1

    if opts['output'].endswith('/') is False:
        opts['output'] += '/'

    if len(opts['urls']) > 0:
        feeds_use = list()
        cfg_before = copy.deepcopy(cfg)
        for url in opts['urls']:
            for feed in cfg['feeds']:
                if url == feed['url']:
                    feeds_use.append(feed)
                    break
            else:
                click.secho('Feed not being tracked: ' + url, fg='yellow')
        cfg['feeds'] = feeds_use

    time_start = time.time()
    for feed in cfg['feeds']:
        if ttl_expired(feed['ttl'], opts['ttl']) is False and opts['force'] is False:
            click.secho('TTL not expired for feed: ' + feed['url'], fg='yellow')
            continue

        try:
            rss_feed, rss_hash = download_rss_feed(feed['url'])
        except (requests.HTTPError, requests.exceptions.ConnectionError):
            click.secho('Unable to download: ' + feed['url'], fg='red', err=True)
            continue

        feed['ttl'] = int(time.time())  # Update the timestamp for the ttl

        if feed['hash'] == rss_hash and opts['force'] is False:
            if debug:
                click.echo('Feed has not changed: ' + feed['url'])
            if len(opts['urls']) > 0:
                # I perform a dictionary "update" this way because the update funciton kept overwriting the list
                for idx, feed_orig in enumerate(cfg_before['feeds']):
                    if feed['url'] == feed_orig['url']:
                        cfg_before['feeds'][idx] = feed
                        break
                write_cfg(cfg_before)
            else:
                write_cfg(cfg)
        else:
            rss_entries = rss_feed['entries']
            if debug:
                click.echo('Feed contains ' + str(len(rss_entries)) + ' entries')
            counter = 0
            # This is so we can keep track of what the "most recent torrent" downloaded was
            downloaded_torrents = list()
            if opts['reverse']:
                rss_entries = reversed(rss_entries)
            for torrent in rss_entries:
                torrent_name = torrent['torrent_filename']
                if feed['new']:
                    downloaded_torrents.append(torrent_name)
                    feed['new'] = False
                    if opts['force'] is False:
                        break
                if opts['count'] <= 0 and torrent_name == feed['last']:
                    if debug:
                        click.echo('No new items in: ' + feed['url'])
                    break
                torrent_url = [x['href'] for x in torrent['links'] if x['type'] == 'application/x-bittorrent']
                if torrent_name not in downloaded_torrents:
                    result = get_torrent_file(torrent_url.pop(), opts['output'], torrent_name)
                    if result[0]:
                        downloaded_torrents.append(torrent_name)
                    else:
                        click.secho(result[1], fg='red', err=True)
                    if opts['count'] >= 0:
                        counter += 1
                        if counter >= opts['count']:
                            break
            # Update the md5 hash for the feed cache
            feed['hash'] = rss_hash
            if len(downloaded_torrents) > 0:
                click.echo('Downloaded ' + str(len(downloaded_torrents)) + ' new torrent(s)')
                # Cache the most recent torrent downloaded
                if opts['reverse']:
                    feed['last'] = downloaded_torrents.pop()
                else:
                    feed['last'] = downloaded_torrents[0]
            if len(opts['urls']) > 0:
                # I perform a dictionary "update" this way because the update funciton kept overwriting the list
                for idx, feed_orig in enumerate(cfg_before['feeds']):
                    if feed['url'] == feed_orig['url']:
                        cfg_before['feeds'][idx] = feed
                        break
                write_cfg(cfg_before)
            else:
                write_cfg(cfg)
    time_end = time.time()
    time_delta = time_end - time_start
    time_delta = format(float(time_delta), '.4f')
    click.secho(str(len(cfg['feeds'])) + " RSS feeds checked in: " + time_delta + ' seconds', fg='green')
    return 0


if __name__ == '__main__':
    sys.exit(cli())
