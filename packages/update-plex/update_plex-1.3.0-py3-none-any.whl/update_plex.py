import configparser
import os
import sys
import xml.etree.cElementTree as etree

import click
import requests


@click.command()
@click.option('--host')
@click.version_option()
def run(host):
    if not host:
        path = '~/.config/update_plex'
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(path))
        try:
            host = config['DEFAULT']['host']
        except KeyError:
            msg = 'Don\'t know where plex is. Have you created the config file in "{}"?'
            click.echo(msg.format(path), err=True)
            sys.exit(1)

        try:
            token = config['DEFAULT']['token']
        except KeyError:
            msg = 'Can\'t authenticate without a token. Have you created the config file in "{}"?'
            click.echo(msg.format(path), err=True)
            sys.exit(1)

    url = 'http://{}/library/sections'.format(host)

    s = requests.Session()
    s.headers = {'X-Plex-Token': token}
    r = s.get(url)
    r.raise_for_status()

    path = './/Directory[@type="show"]'
    for section in etree.fromstring(r.content).findall(path):
        url = '{}/{}/refresh'.format(url, section.attrib['key'])
        r = s.get(url)
        r.raise_for_status()


if __name__ == '__main__':
    run()
