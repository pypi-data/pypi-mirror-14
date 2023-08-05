#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass
try:
    from ConfigParser import (SafeConfigParser as ConfigParser,
                              Error as parseError)
except ImportError:
    from configparser import ConfigParser, Error as parseError

import json
import logging
from collections import defaultdict
from datetime import datetime
from os import listdir
from os.path import basename, splitext, dirname, join as pjoin
from re import compile, DOTALL, MULTILINE, findall, M as REM

import dns.message
import dns.rdatatype
import dns.resolver
import dns.tsig
import dns.tsigkeyring
from dns import query, name as dns_name
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from pyparsing import (Literal, White, Word, alphanums, CharsNotIn,
                       Optional, Forward, Group, ZeroOrMore, OneOrMore,
                       QuotedString, restOfLine)
from requests import Session, get as rget
from requests.exceptions import SSLError


__all__ = ['Distributor', 'create_html']


class NginxParser(object):
    def __init__(self):
        left_bracket = Literal("{").suppress()
        right_bracket = Literal("}").suppress()
        semicolon = Literal(";").suppress()
        space = White().suppress()
        key = Word(alphanums + "+.-_/")
        value = ZeroOrMore(
            CharsNotIn('{};#"\'') | space |
            QuotedString("'", escChar='\\', multiline=True) |
            QuotedString('"', escChar='\\', multiline=True))
        # modifier for location uri [ = | ~ | ~* | ^~ ]
        modifier = Literal("=") | Literal("~*") | Literal("~") | Literal("^~")

        comment = Literal('#').suppress() + Optional(restOfLine)

        # rules
        assignment = Group(
            (key | value) + value + semicolon +
            Optional(space + comment))
        block = Forward()

        block << Group(
            Group(key + Optional(space + modifier) + Optional(space) +
                  Optional(value) + Optional(space + value)) +
            left_bracket +
            Group(ZeroOrMore(assignment | block | comment.suppress())) +
            right_bracket)

        def comment_handler(t):
            result = []

            if "promo" in t[0]:
                result.append("promo")
            if "author: " in t[0]:
                try:
                    email = t[0].split("author: ")[1].strip()
                    result.append(email)
                except Exception:
                    result.append(t[0])
            return result

        comment.setParseAction(comment_handler)

        self.script = OneOrMore(assignment | block | comment.suppress())

    def parse(self, s):
        def to_dict(o):
            d = defaultdict(list)
            for i in o:
                try:
                    d[i[0].strip() if isinstance(i[0], (str, int))
                      else " ".join(i[0]).strip()].append(
                        i[1].strip() if isinstance(i[1], (str, int))
                        else to_dict(i[1]))
                except:
                    continue
                if 'promo' in i:
                    d['promo'] = True
                if '@' in i[-1] and "@go" not in i[-1]:
                    d['author'] = i[-1]
            return d

        servers = {'http': [], 'stream': [], 'log_format': {}}
        for t in self.script.parseString(s).asList():
            if len(t) and t[0] in [['http'], ['stream']]:
                for tt in t[1]:
                    if tt[0] == ["server"]:
                        servers[t[0][0]].append(to_dict(tt[1]))
                    if tt[0] == 'log_format':
                        servers[tt[0]][tt[1].strip()] = tt[2].strip()

        return servers


def check_dns(domain, ns):
    ns_s = list(filter(len, map(lambda _s: _s.strip(),
                                ns.replace('"', '').split(';'))))
    if len(ns_s) < 1:
        return {}
    mess = dns.message.make_query(dns_name.from_text(domain),
                                  dns.rdatatype.SOA)
    result = {}
    for ns in ns_s:
        try:
            name_s = dns_name.from_text(ns.split()[0]).to_text()
            answer = query.tcp(mess, name_s, timeout=2)
            if len(answer.authority):
                result[ns] = True
            else:
                rr = answer.answer[0][0]
                if rr.rdtype == dns.rdatatype.SOA:
                    result[ns] = True
                else:
                    result[ns] = False
        except:
            result[ns] = False
    return result


def check_txt(domain, status):
    spf, dmarc = 1, 1
    if u"Не делегирован" in status:
        return spf, dmarc
    try:
        mess = dns.resolver.query(
            dns_name.from_text(domain),
            dns.rdatatype.TXT)
    except:
        spf = 1
    else:
        txts = [txt for rdata in mess for txt in rdata.strings]
        spfs = filter(lambda i: "v=spf1" in i, txts)
        if not spfs:
            spf = 1
        else:
            if "+all" in " ".join(spfs):
                spf = 2
            else:
                spf = 0
    try:
        mess = dns.resolver.query(
            dns_name.from_text("_dmarc." + domain),
            dns.rdatatype.TXT)
    except:
        return spf, dmarc
    else:
        txts = [txt for rdata in mess for txt in rdata.strings]

        dmarc = 0 if filter(lambda i: "v=DMARC1" in i, txts) else 1
        return spf, dmarc


class Distributor(object):
    def __init__(self, configs_dir, settings):
        self.services = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(set)))
        self._api = dict()
        self.changed = []
        self.authors = defaultdict(set)
        self.re_haproxy = compile(
            r'^listen\s+?([\w\d\.:\-_]+)\s+?'
            '(?:(?:\s+?bind\s+?)?'
            '((?:\d{1,3}\.){3}\d{1,3}:\d+)\s+?)+',
            DOTALL | MULTILINE)

        self.tpl = Environment(loader=PackageLoader("distributor"))
        self.configs = configs_dir
        try:
            self.settings = ConfigParser()
            if settings not in self.settings.read(settings):
                logging.error("No such file %s or it is empty" % settings)
                exit(1)
        except parseError as e:
            logging.error("Bad config file: %s" % e)
            exit(1)
        try:
            self.same_hosts = compile(self.settings.get("git", "same_host"))
        except parseError:
            # regexp for unavailable hostname (to be search() == None)
            self.same_hosts = compile("\*")

    def index(self):
        last_sync = datetime.now().strftime("%d %B %H:%M %A")
        try:
            zones = self.settings.get("dns", "domains").split(",")
        except:
            zones = []
        return self.tpl.get_template("index.html").render(
            last_sync=last_sync,
            categories=self.get_cats(),
            bind_zones=zones
        )

    def get_cats(self):
        return sorted(self.services.keys())

    def api(self):
        authors = defaultdict(list)
        for url, authors_list in self.authors.items():
            for a in authors_list:
                authors[a].append(url)
        self._api['web']['authors'] = authors
        return json.dumps(self._api)

    def generate(self):
        for conf in listdir(self.configs):
            conf_file = pjoin(self.configs, conf)
            if "dns" in conf:
                self.parse_dns(conf_file)
            elif "nic" in conf:
                self.parse_nic(conf_file)
            elif "nginx" in conf:
                self.parse_nginx(conf_file)
            elif "haproxy" in conf:
                self.parse_haproxy(conf_file)
            else:
                logging.warning("Parser for %s is not implemented" % conf)

    def parse_dns(self, conf):
        servers = [i.split(" ", 1) for i in open(conf).readlines()]
        cat = "DNS_" + basename(conf).replace("dns.", "").replace(".", "_")
        for server in servers:
            if "_domainkey" in server[0]:
                continue
            (priority, class_path,
             list_type, destination) = server[1].split(" ", 3)

            self.services[cat][server[0]] = {
                "   Priority": [priority],  # For sorting labels
                "  Class": [class_path],
                " Type": [list_type],
                "Dest": [destination.rstrip()]
            }

    def parse_nic(self, conf):
        domains = json.load(open(conf))
        for domain in domains:
            self.services["NIC"][domain['domain']] = {
                "    Status": [domain['status']],
                "   TXT": domain['txt'],
                "  NS": domain['ns'].items(),
                " Till": [domain['till']],
                "Auto-renew": [domain['sost']],
            }

    def parse_nginx(self, conf):
        servers = NginxParser().parse(open(conf).read())
        server_name = basename(conf).replace(".all", "").replace("nginx.", "")
        try:
            server_name = self.same_hosts.search(server_name).group(1)
        except (AttributeError, IndexError):
            pass

        if 'web' not in self._api:
            self._api['web'] = {'servers': {}, 'log_format': {}}

        self._api['web']['log_format'].update(servers['log_format'])

        # Parse http section
        for server in servers["http"]:
            cat = "promo" if "promo" in server and server['promo'] else "web"
            if "author" in server and server['author']:
                author = server['author']
            else:
                author = ""
            try:
                log = server['access_log'][0].split()
            except (IndexError, ValueError, TypeError):
                log = ["", ""]
            if len(log) > 1:
                log_path, log_format = map(lambda i: i.strip(), log[:2])
            else:
                log_path, log_format = log[0], ""
            listeners = server['listen']
            ports = list(filter(
                lambda p: (p != '80') and len(p),
                map(lambda l: l.split()[0].split(':')[1]
                    if len(l.split()[0].split(':')) > 1 else '',
                    listeners)))
            if server['server_name'] and '_' not in server['server_name'][0]:
                urls = map(
                    lambda l: l + ':' + ",".join(ports) if len(ports) else l,
                    server['server_name'][0].split())
            else:
                continue

            def std_ports(ip_addr):
                ip_addr = ip_addr.split()[0]
                if ":80" == ip_addr[-3:]:
                    return ip_addr[:-3]
                return ip_addr

            listeners = set(map(std_ports, listeners))

            for url in urls:
                url = url.lower().encode("utf8").decode("idna")
                self.authors[url].add(author)
                self.services[cat][url][server_name].update(listeners)

                self._api['web']['servers'][url] = {
                    'author': author,
                    'log': log_path,
                    'log_format': log_format
                }

        # Parse Stream section
        for server in servers["stream"]:
            cat = "stream"
            if "author" in server and server['author']:
                author = server['author']
            else:
                author = ""
            listeners = set(map(lambda l: l.split()[0], server['listen']))
            url = server['proxy_pass'][0]
            self.authors[url].add(author)
            self.services[cat][url][server_name].update(listeners)

    def parse_haproxy(self, conf):
        listeners = [(i[0].replace("cluster.", ""), i[1])
                     for i in self.re_haproxy.findall(open(conf).read())]

        server_name = basename(conf).replace("haproxy.",
                                             "").replace(".all", "")
        try:
            server_name = self.same_hosts.search(server_name).group(1)
        except (AttributeError, IndexError):
            pass

        for listener in listeners:
            if listener[0] == "stat":
                continue

            fl = True
            cat = "other"
            for pattern in [":8080", ":443", ":80"]:
                if pattern in listener[1]:
                    cat = "http"
                    fl = False
                    break

            if fl:
                for pattern in [":1433"]:
                    if pattern in listener[1]:
                        cat = "sql"
                        fl = False
                        break

            if fl:
                for pattern in [":25", ":143", ":110"]:
                    if pattern in listener[1]:
                        cat = "mail"
                        fl = False
                        break

            if fl:
                for pattern in ["ssh", "sql", "rdp", "mail",
                                "http", "ldap", "sms"]:
                    if pattern in listener[0]:
                        cat = pattern
                        # fl = False
                        break

            self.services[cat][listener[0]][server_name].add(listener[1])

    def write(self, cat):
        servers = set()
        for service in self.services[cat].keys():
            for server_name in self.services[cat][service].keys():
                try:
                    server_name = self.same_hosts.search(server_name).group(1)
                except (AttributeError, IndexError):
                    pass
                servers.add(server_name)
        servers = sorted(servers)
        columns = servers + ["author"]
        services1 = {0: [], 1: []}
        for service in self.services[cat].keys():
            c = (0 if len(self.services[cat][service].keys()) > 1 and
                 "DNS" not in cat and "NIC" not in cat else 1)
            services1[c].append(
                (service, None if c < 1
                 else servers.index(
                    next(iter(self.services[cat][service].keys()))
                 ))
            )

        def skip_www(cs):
            # Use for sorting
            s = cs[0]
            if len(s) > 4 and "www." in s[:4]:
                return s[4:] + " "
            else:
                return s

        services = (
            sorted(services1[0], key=skip_www) +
            sorted(services1[1], key=skip_www)
        )
        result_services = []
        for (service, zone) in services:
            errors = False
            result_service = {'zone': zone}

            clear_service = service
            dotted = False
            if clear_service[0] == ".":
                clear_service = clear_service[1:]
                dotted = True
            if ":443" in clear_service:
                clear_service = "https://" + clear_service.replace(":443", "")
            result_service['service'] = clear_service
            result_service['dotted'] = dotted
            skipped_cat = False
            try:
                for candidate in self.settings.get("git",
                                                   "skipped").split(","):
                    if candidate in self.services[cat][service].keys():
                        skipped_cat = True
                        break
            except parseError:
                pass
            if (cat == "web" or cat == "promo") and not skipped_cat:
                history = 0
                if "https://" in clear_service:
                    url = clear_service
                else:
                    url = "http://" + clear_service
                url = url.split(",")[0]
                try:
                    if cat == "promo":
                        r = rget("%s/favicon.ico" % url, timeout=5)
                        if r.status_code != 200:
                            result_service['no_fav'] = True
                        elif "image/x-icon" not in r.headers['content-type']:
                            result_service['bad_fav'] = True
                        history += len(r.history)
                        r = rget("%s/robots.txt" % url, timeout=5)
                        if r.status_code != 200:
                            result_service['no_robots'] = True
                        elif "text/plain" not in r.headers['content-type']:
                            result_service['bad_robots'] = True
                        history += len(r.history)
                        r = rget("%s/sitemap.xml" % url, timeout=5)
                        if r.status_code != 200:
                            result_service['no_sitemap'] = True
                        elif "text/xml" not in r.headers['content-type']:
                            result_service['bad_sitemap'] = True
                        r = rget(url, timeout=5)
                        history += len(r.history)
                        if len(r.history):
                            result_service['redirect'] = True
                        if r.headers.get('x-powered-by'):
                            result_service['x_powered_by'] = True
                        for head_name, header in r.headers.items():
                            if "set-cookie" in head_name:
                                continue
                            h = list(
                                map(lambda s: s.strip(), header.split(","))
                            )
                            if len(h) > len(set(h)):
                                result_service['double_header_same'] = True
                                break

                        if "<h1" not in r.text:
                            result_service['no_h1'] = True
                        if "<title" not in r.text:
                            result_service['no_title'] = True
                        if 'name="description"' not in r.text:
                            result_service['no_description'] = True

                    else:
                        r = rget(url, timeout=5)
                        history += len(r.history)
                        if len(r.history):
                            result_service['redirect'] = True
                        if r.headers.get('x-powered-by'):
                            result_service['x_powered_by'] = True
                        for head_name, header in r.headers.items():
                            if "set-cookie" in head_name:
                                continue
                            h = list(
                                map(lambda s: s.strip(), header.split(","))
                            )
                            if len(h) > len(set(h)):
                                result_service['double_header_same'] = True
                                break

                except SSLError:
                    result_service['insecure'] = True
                except Exception as e:
                    result_service['no_url'] = e

            result_service['servers'] = []
            for server in servers:
                if server not in self.services[cat][service].keys():
                    if "NIC" in cat and "NS" in server:
                        errors |= True
                    result_service['servers'].append(None)
                    continue

                if "NIC" in cat and "NS" in server:
                    temp_result = []
                    for ip, stat in sorted(
                            self.services[cat][service][server]):
                        temp_result.append({'ip': ip, 'stat': stat})
                        if not stat:
                            errors |= True
                    result_service['servers'].append(temp_result)

                elif "TXT" not in server:
                    result_service['servers'].append(
                        [{'ip': ip}
                         for ip in sorted(self.services[cat][service][server])]
                    )
                if "NIC" in cat and "TXT" in server:
                    if u"Не делегирован" not in u"".join(
                            self.services[cat][service]["    Status"]):
                        spf, dmarc = self.services[cat][service][server]
                        result_service['servers'].append(
                            [{'ip': 'spf ', 'spf': spf},
                             {'ip': 'dmarc ', 'dmarc': dmarc}]
                        )
                        if spf or dmarc:
                            errors |= True

            if cat == "web" or cat == "promo" or cat == "stream":
                result_service['author'] = " ".join(
                    filter(len, self.authors.get(service, {}))
                )
            result_service['errors'] = errors

            result_services.append(result_service)

        try:
            template = self.tpl.get_template(cat + ".html")
        except TemplateNotFound:
            template = self.tpl.get_template("_table.html")

        return template.render(services=result_services,
                               columns=columns,
                               servers=servers,
                               cat=cat)

    def fetch(self):
        # GitLab
        if self.settings.has_section('git'):
            self.fetch_git()

        # DNS
        if self.settings.has_section('dns'):
            self.fetch_dns()
        # NIC.ru
        if self.settings.has_section('nic'):
            self.fetch_nic()

    def fetch_nic(self):
        try:
            s = Session()
            login = s.post(
                "https://www.nic.ru/login/manager/",
                data={
                    'login': self.settings.get("nic", "login"),
                    'client_type': 'NIC-D',
                    'password': self.settings.get("nic", "password"),
                    'password_type': 'adm'
                }
            )
            if login.status_code == 200:
                csv = s.get("https://www.nic.ru/manager/my_domains.cgi"
                            "?step=srv.my_domains&view.format=csv",
                            verify=False)
                if csv.status_code == 200:
                    csv = csv.text
                    csv = list(map(
                        lambda info: {'domain': info[0],
                                      'ns': check_dns(info[1], info[2]),
                                      'txt': check_txt(info[1], info[5]),
                                      'status': info[5],
                                      'sost': info[6],
                                      'till': info[7]},
                        map(lambda l: l.split(","),
                            filter(len, csv.split("\n")[2:]))
                    ))
                    json.dump(csv, open(pjoin(self.configs, "nic"), "w"))
        except:
            logging.error("can't fetch from NIC.ru by login: %s" %
                          self.settings.get('nic', 'login'))

    def fetch_dns(self):
        try:
            name_server = self.settings.get("dns", "server")
            keyring = dns.tsigkeyring.from_text(
                    {self.settings.get("dns", "tsig_name"):
                     self.settings.get("dns", "tsig_key")}
            )
            for domain in self.settings.get("dns", "domains").split(","):
                try:
                    responses = query.xfr(
                            name_server,
                            dns_name.from_text(domain),
                            keyring=keyring,
                            keyname=self.settings.get("dns", "tsig_name"),
                            keyalgorithm=dns.tsig.HMAC_SHA512
                    )
                    with open(pjoin(self.configs, "dns." + domain),
                              "w") as config:
                        for response in responses:
                            for line in response.answer:
                                config.write(line.to_text() + u"\n")
                except:
                    pass
        except:
            logging.error("can't fetch from DNS: %s" %
                          self.settings.get('dns', 'server'))

    def fetch_git(self):
        try:
            servers = self.settings.get("git", "servers").split(",")
            auth = {'PRIVATE-TOKEN': self.settings.get("git", "token")}
            url = ("https://%s/api/v3/projects" %
                   self.settings.get("git", "host"))
            for server in servers:
                try:
                    id_proj = rget(
                        "%s/%s%%2F%s" %
                        (url, self.settings.get("git", "group"), server),
                        headers=auth
                    ).json()[u'id']
                except:
                    logging.warning("Repository %s does not exists" % server)
                else:
                    sha = rget(
                        "%s/%s/repository/commits" % (url, id_proj),
                        headers=auth).json()[0][u'id']
                    for filepath in ['usr/local/etc/nginx/nginx.conf',
                                     'usr/local/etc/haproxy/haproxy.cfg',
                                     'etc/nginx/nginx.conf',
                                     'etc/haproxy/haproxy.cfg',
                                     'nginx.conf']:
                        try:
                            params = {'filepath': filepath}
                            main_file = rget(
                                "%s/%s/repository/blobs/%s" %
                                (url, id_proj, sha),
                                params=params, headers=auth)
                            if main_file.status_code != 200:
                                continue
                            with open(
                                pjoin(
                                    self.configs,
                                    "%s.%s.all" %
                                    (splitext(basename(filepath))[0], server)
                                ), "w"
                            ) as config:
                                main_file = main_file.text

                                for incl in findall(
                                    r"(?:^i|^[ \t]+i)nclude (.+?);$",
                                    main_file, REM
                                ):
                                    try:
                                        params = {
                                            'filepath':
                                            pjoin(dirname(filepath), incl)
                                        }
                                        include_file = rget(
                                            "%s/%s/repository/blobs/%s"
                                            % (url, id_proj, sha),
                                            params=params, headers=auth)
                                        if include_file.status_code == 200:
                                            main_file = main_file.replace(
                                                "include " + incl + ";",
                                                include_file.text)
                                    except:
                                        pass
                                config.write(main_file)
                        except:
                            pass
        except:
            logging.error("can't fetch from GitLab: %s" %
                          self.settings.get('git', 'host'))
