#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import a2x.a2s
import argparse
import urllib.error
import urllib.request


def cl():
    parse = argparse.ArgumentParser()

    group_comm = parse.add_argument_group('Common')
    group_comm.add_argument(
        '--incoming', help='Incoming data', metavar='url', type=str,
    )
    group_comm.add_argument(
        '--outgoing', help='Outgoing data', metavar='url', type=str,
    )
    group_comm.add_argument(
        '--domain', help='Domain name', metavar='name', type=str,
    )
    group_comm.add_argument(
        '--fields', help='Which fields for sending (default: all)',
        metavar='name,players,...', type=str,
    )

    group_oth = parse.add_argument_group('Other')
    group_oth.add_argument(
        '--verbose', help='Show message', action='store_true', default=False,
    )
    group_oth.add_argument(
        '--daemon', help='Daemon', action='store_true', default=False,
    )
    group_oth.add_argument(
        '--sleep', help='Sleeping time (default: 180s)', metavar='number',
        type=float, default=180
    )
    group_oth.add_argument(
        '--version', action='version', version='%(prog)s -- v0.0.6',
    )
    parse_keys = parse.parse_args()
    return parse, parse_keys


def request(url):
    """
    getting data (json):
    {
        <game_srv1>: {
            {'location': 'n4', 'port': 27015}
        },
        <game_srv1>: {
            {'location': 'n4', 'port': 27016}
        },
    }

    location: part of the domain -- n4 or full hostname -- n4.domain.net

    :param url:
    :type url: str
    :return: dict
    """
    try:
        rst = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print('Error: URL incorrect (page not found (404))')

        return {}

    return json.loads(rst.read().decode('utf-8'))


def response(url, data):
    json_data = json.dumps(data).encode(encoding='utf-8')
    req = urllib.request.Request(
        url=url,
        data=json_data)

    req.add_header('Content-Type', 'application/json')

    try:
        res = urllib.request.urlopen(url=req)
    except Exception as err:
        print('Error: report message -- failed: %s' % err)
        return False

    if res.code == 200:
        return True
    else:
        print('Report message -- failed')
        return False


def vl_srv_request(host, port, domain):
    """

    :param host: location game server
    :type host: str
    :param port:
    :type port: int
    :param domain: if getting part of domain then need domain use
    :type domain: str
    :return: dict
    """
    a2s_info = a2x.a2s.A2SInfo()

    if domain:
        host = '%s.%s' % (host, domain)

    a2s_info.get_info((host, port))
    return a2s_info.readable_data


def work(**kwargs):
    url_incoming = kwargs.get('in')
    url_outgoing = kwargs.get('out')
    domain = kwargs.get('domain')
    fields = kwargs.get('fields', [])
    verbose = kwargs.get('verbose')
    outgoing_data = {}

    if isinstance(fields, str):
        fields = fields.split(',')

    # Getting data
    hosts = request(url_incoming)

    for host in hosts:
        outgoing_data[host] = {}
        host_ = hosts[host]['location']
        port_ = hosts[host]['port']

        a2s_info = vl_srv_request(host_, port_, domain)

        if fields:
            for field in fields:
                outgoing_data[host][field] = a2s_info[field]
        else:
            for key, value in a2s_info.items():
                outgoing_data[host][key] = value

    if verbose:
        print(outgoing_data)

    if url_outgoing:
        response(url_outgoing, outgoing_data)


def daemon(**kwargs):
    is_daemon = kwargs.get('is_daemon')
    sleep_time = kwargs.get('sleep_time')

    while True:
        try:
            work(**kwargs)

            if is_daemon is False:
                break

            time.sleep(sleep_time)
        except Exception as err:
            print('Exception: %s' % (err,))


def main():
    parse, keys = cl()

    if keys.incoming:
        options = {
            'in': keys.incoming, 'out': keys.outgoing, 'domain': keys.domain,
            'fields': keys.fields, 'verbose': keys.verbose,
            'is_daemon': keys.daemon, 'sleep_time': keys.sleep
        }
        daemon(**options)
        exit()

    parse.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
