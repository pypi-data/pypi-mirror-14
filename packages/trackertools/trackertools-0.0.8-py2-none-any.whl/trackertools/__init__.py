#!/usr/bin/env python
from __future__ import print_function
import mechanize
import cookielib
import os
import json
import requests
import pprint
import logging
import sys
import lxml.html as lh
import subprocess
import re
import string
import helpers

class Tracker(object):

    def __init__(self, username, password, root_url, login_url, main_url, cookies_file, tools_server=None, debug=False):
        self.username = username
        self.password = password
        self.root_url = root_url
        self.login_url = login_url
        self.main_url = main_url
        self.tools_server = tools_server
        self.cookies_file = cookies_file
        self.br = mechanize.Browser()
        self.logged_in = False
        self.debug = debug

        # Set up output dir
        self.wdir=os.path.abspath(os.path.dirname(__file__))

        # Set up the logger
        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('tcpserver')

        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def login(self, invalidate_cookies=False):
        br = self.br
        br.set_handle_robots(False)
        # user agent updated 2016-03-11
        br.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]

        # Cookie Jar
        policy = mechanize.DefaultCookiePolicy(rfc2965=True)
        cj = mechanize.LWPCookieJar(policy=policy)
        br.set_cookiejar(cj)

        if os.path.isfile(os.path.join(self.wdir, self.cookies_file)) and not invalidate_cookies:
            self.logger.debug("Found %s" % self.cookies_file)
            cj.load(os.path.join(self.wdir, self.cookies_file), ignore_discard=True, ignore_expires=True)
            torrent_index = self.main_url
            self.logger.debug("Opening url...%s" % torrent_index)
            resp = br.open(torrent_index)
            if "login.php" in resp.geturl():
                self.logger.debug("Bad url.  Invalidating cookies...")
                self.login(invalidate_cookies=True)
        else:
            # Check if existing cookies work
            resp = br.open(self.login_url)

            br.select_form(nr=0) # select second form in page (0 indexed)
            br['username'] = self.username
            br['password'] = self.password
            response = br.submit()

            self.logger.debug("Saving cookies after login form")
            cj.save(os.path.join(self.wdir, self.cookies_file), ignore_discard=True, ignore_expires=True)
            self.logger.debug("Logged in to %s" % response.geturl())

        self.logged_in = True
        return self.logged_in

    def query_isbn(self, isbn, tools_server=None):
        if not tools_server:
            tools_server = self.tools_server
        self.logger.info("+++++++++++++++++++++++++++++++")
        self.logger.info("querying %s -- Start" % isbn)
        url='http://%s/search.php?keyword=%s' % (tools_server, isbn)
        r = requests.get(url)
        json_data = json.loads(r.text)
        self.logger.info("querying %s -- Done!" % isbn)
        return json_data

    def get_epub(self, url):
        self.logger.info(url)
        if not self.logged_in:
            self.logger.debug("Not logged in.")
            return False

        resp = self.br.open(url)
        helpers.write_text_to_file("torrent_page.html", resp.read())

    def _get_torrent_info(self, url):
        self.logger.info(url)
        if not self.logged_in:
            self.logger.debug("Not logged in.")
            return False

        resp = self.br.open(url)
        doc = lh.document_fromstring(resp.read())

        return parse_torrent_page(doc=doc)

    def download_torrent_from_url(self, url):
        torrent_info = self._get_torrent_info(url)
        download_url = torrent_info['download_url']
        self.logger.debug("download_url is %s" % download_url)
        self.logger.info("Downloading torrent...")
        torrent_resp = self.br.open(download_url)
        with open(os.path.join(self.wdir, torrent_info['slug']),'w') as f:
            f.write(torrent_resp.read())
            self.logger.debug("Wrote to file %s" % torrent_info['slug'])

    def add_ebook_format(self, url, isbn, torrent_file, format='MOBI', debug_write_to_file=False):
        if not self.logged_in:
            self.logger.debug("Not logged in.")
            return False

        self.logger.info("Opening %s...", url)
        resp = self.br.open(url)

        # Get the right form
        for form in self.br.forms():
            if form.attrs.get('id') == 'upload_table':
                self.br.form = form
                break

        if not self.br.form:
            self.logger.info("Missing form on %s" % url)
            return False

        # fill out the form
        self.logger.debug(self.br.form)
        self.br.form['book_isbn'] = isbn.replace('-','')
        self.br.form['book_format'] = [format.upper(),]
        self.br.form.add_file(open(torrent_file), 'text/plain', torrent_file)
        self.br.form.set_all_readonly(False)
        #self.br.form['file_input'] = torrent_file

        query = self.query_isbn(isbn)
        self.br.form['book_author'] = query['Items'][0]['Author']
        self.br.form['book_publisher'] = query['Items'][0]['Publisher']
        book_year = query['Items'][0]['ReleaseDate'].split('-')[0]
        if not book_year:
            book_year = query['Items'][0]['PublicationDate'].split('-')[0]

        self.br.form['book_year'] = book_year
        self.logger.debug(self.br.form)

        req = self.br.submit()
        final_url = req.geturl()
        self.logger.debug("Redirected to %s" % final_url)

        if "groupid" in final_url:
            html = resp.read()
            filename = "add_ebook_format_%s.html" % isbn
            self.logger.debug("Writing url to file %s" % filename)
            helpers.write_text_to_file(filename, html)

        return final_url

    def parse_search_page(self, filename=None, doc=None, url=None):
        doc = self._get_doc_from_general(filename=filename, doc=doc, url=url)

        mydict = {}

        # Prepare top level keys
        mydict['title'] = doc.xpath('//title')[0].text_content()
        mydict['torrents'] = []

        # Fill out torrent key with 'page_url' list
        view_torrent_urls = doc.xpath('//a[@title="View Torrent"]/@href')
        for vtu in view_torrent_urls:
            mydict['torrents'].append({'page_url': '/'.join([self.root_url, vtu])})

        # Get the torrent list titles
        view_torrent_titles = doc.xpath('//a[@title="View Torrent"]/text()')
        for i, vtt in enumerate(view_torrent_titles):
            mydict['torrents'][i]['title'] = vtt

        # Get the author, year, format
        view_torrent_td = doc.xpath('//a[@title="View Torrent"]/parent::td')
        regex = re.compile('\[DL \| RP \] *(.*)-.*\(([0-9]{4})\).*\[([a-zA-Z]*)\]')
        for i, vta in enumerate(view_torrent_td):
            # Get the author, format, year
            raw_td = vta.text_content().replace('\n','')
            m = regex.search(raw_td)
            cleaned_author = m.group(1).strip()
            cleaned_year = m.group(2).strip()
            cleaned_format = m.group(3).strip()
            if i%30 == 0:
                self.logger.debug("cleaned_author is %s" % cleaned_author)
                self.logger.debug("cleaned_format is %s" % cleaned_format)
            mydict['torrents'][i]['author'] = cleaned_author
            mydict['torrents'][i]['year'] = cleaned_year
            mydict['torrents'][i]['format'] = cleaned_format

        # Get the download_url
        view_torrent_td = doc.xpath('//a[@title="Download"]/@href')
        for i, vtt in enumerate(view_torrent_td):
            cleaned_url = '/'.join([self.root_url, vtt])
            if i%15 == 0:
                self.logger.debug('vtt is %s' % cleaned_url)
            mydict['torrents'][i]['download_url'] = cleaned_url

        # Get the tags
        view_torrent_tags = doc.xpath('//div[@class="tags"]')
        for i, vtt in enumerate(view_torrent_tags):
            cleaned_tags = vtt.text_content()
            if i%15 == 0:
                self.logger.debug("cleaned tags is %s" % cleaned_tags)
            mydict['torrents'][i]['tags'] = cleaned_tags

        # Get the filesize
        view_torrent_filesize = doc.xpath('//tr[@class="torrent  "]/td[5]')
        for i, vtt in enumerate(view_torrent_filesize):
            cleaned_filesize = vtt.text_content()
            if i%15 == 0:
                self.logger.debug("cleaned filesize is %s" % cleaned_filesize)
            mydict['torrents'][i]['filesize'] = cleaned_filesize

        return mydict

    def _get_doc_from_general(self, filename=None, doc=None, url=None):
        # One or the other
        if doc is None and filename:
            with open(filename, 'r') as f:
                doc = lh.document_fromstring(f.read())
                return doc
        elif doc is not None and not filename:
            pass
        elif url:
            self.logger.debug("Parsing %s" % url)
            if not self.logged_in:
                self.logger.debug("Not logged in.")
                return False

            resp = self.br.open(url)
            html = resp.read()
            doc = lh.document_fromstring(html)
            return doc

        self.logger.debug("No valid doc or filename")
        return False

    def parse_torrent_page(self, filename=None, doc=None, url=None):
        doc = self._get_doc_from_general(filename=filename, doc=doc, url=url)

        mydict = {}
        mydict['title'] = doc.xpath('//title')[0].text_content()
        mydict['slug'] = '.'.join([mydict['title'][0:50].translate(None, '-: ,?!'), 'torrent'])
        mydict['torrent_table'] = doc.xpath('//table[@class="torrent_table"]')

        # get the ISBN
        bbcode = doc.xpath('//div/span[@class="bbcode"]')[0].text_content().split("\n")
        for line in bbcode:
            self.logger.debug(line)
            if "ISBN" in line:
                isbn = line.split(":")[1].strip()
                mydict['isbn'] = isbn
                self.logger.debug("Using ISBN: %s" % isbn)
                break
            elif "ASIN" in line:
                asin = line.split(":")[1].strip()
                mydict['isbn'] = asin
                self.logger.debug("ISBN not found, using ASIN: %s" % asin)
                break
        else:
            mydict['isbn'] = None

        # get the torrent info
        mydict['group_id'] = doc.xpath('//input[@name="groupid"]')[0].value
        # Add torrent_ids and raw_download_urls
        mydict['raw_download_urls'] = []
        mydict['torrent_ids'] = []
        # regex for torrent_id
        tid_regex = re.compile('.*id=([^&]*)')
        for dl_url in doc.xpath('//tr[@class="group_torrent "]//a[@title="Download"]/@href'):
            raw_download_url = '/'.join([self.root_url, dl_url])
            # raw_download_urls
            mydict['raw_download_urls'].append(raw_download_url)
            self.logger.debug("raw_download_url is: %s" % raw_download_url)

            # torrent_ids
            m = tid_regex.match(dl_url)
            torrent_id = m.group(1)
            mydict['torrent_ids'].append(torrent_id)

        mydict['format_titles'] = []
        mydict['formats'] = []

        #for link, tid in zip(doc.xpath('//tr[@class="group_torrent "]/a/@onclick'), mydict['torrent_ids']):
        for link in doc.xpath('//tr[@class="group_torrent "]//a'):
            # Make sure that the order is right for torrent_id and the title. onclick contains the torrent_id

            # Strip unicode
            title = link.text_content()
            printable = set(string.printable)
            title = filter(lambda x: x in printable, title).strip()

            # Add formats
            if 'MOBI' in title:
                mydict['formats'].append('MOBI')
            elif 'EPUB' in title:
                mydict['formats'].append('EPUB')
            else:
                continue

            self.logger.debug("Link is %s and content is %s" % (link, title))
            mydict['format_titles'].append(title)

        # Hook up the formats and raw_download_urls into a dict
        mydict['download_urls'] = dict(zip(mydict['formats'], mydict['raw_download_urls']))

        self.logger.debug(pprint.pprint(mydict))
        return mydict

    def _get_doc_from_general(self, filename=None, doc=None, url=None):
        # One or the other
        if doc is None and filename:
            with open(filename, 'r') as f:
                doc = lh.document_fromstring(f.read())
                return doc
        elif doc is not None and not filename:
            pass
        elif url:
            self.logger.debug("Parsing %s" % url)
            if not self.logged_in:
                self.logger.debug("Not logged in.")
                return False

            resp = self.br.open(url)
            html = resp.read()
            doc = lh.document_fromstring(html)
            return doc

        self.logger.debug("No valid doc or filename")
        return False

    def get_stats(self, filename=None, doc=None, url=None):

        doc = self._get_doc_from_general(filename=filename, doc=doc, url=url)
        if not doc:
            self.logger.debug('get_stats doc is None')
            return None

        stats = {}
        li_stats = doc.xpath('//ul[@class="stats nobullet"]/li')
        for stat in li_stats:
            stat_list = stat.text_content().strip().split(':')
            if len(stat_list) != 2:
                continue
            try:
                cs = self._clean_stat_list(stat_list)
                stats[cs[0]] = cs[1]
            except IndexError:
                continue

        self.logger.debug(stats)

        if ' for ' in stats['requests_filled_gb']:
            num_and_gb = stats['requests_filled_gb'].split(' for ')
            stats['requests_filled_num'] = num_and_gb[0]
            stats['requests_filled_gb'] = num_and_gb[1]

        return stats

    def _clean_stat_list(self, stat_list):
        #self.logger.debug("Dirty stat is %s" % stat_list)

        cleaned = stat_list

        # Append _num to non GB
        if 'TB' in stat_list[1]:
            # convert into GB
            cleaned[1] = cleaned[1].replace('TB','').strip()
            cleaned[1] = str(int(float(cleaned[1])*1000))
            cleaned[0] = cleaned[0] + "_gb"
        elif 'GB' in stat_list[1]:
            cleaned[0] = cleaned[0] + "_gb"
            cleaned[1] = cleaned[1].replace('GB','').strip()
        elif 'View' in stat_list[1]:
            cleaned[0] = cleaned[0] + "_num"

        cleaned[0] = cleaned[0].strip().replace(' ','_').strip().lower()
        cleaned[1] = cleaned[1].strip().replace(' View','').strip().lower()

        #self.logger.debug("Cleaned stat is %s" % cleaned)
        return cleaned

class Seedbox(object):

    def __init__(self, seed_dir=None):
        self.seed_dir = seed_dir

        # Set up the logger
        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('tcpserver')
        self.logger.setLevel(logging.DEBUG)

    def add_torrent(self, url=None):
        if url:
            self.logger.debug("add_torrent: %s" % url)
        else:
            self.logger.error("add_torrent: Mising url")
            return False
        self.logger.debug('adding to transmission: %s' % url)
        subprocess.call(["transmission-remote", "-a", url])
        self.logger.debug('Done! adding to transmission: %s' % url)

    def _get_last_transmission_id(self):
        try:
            output = subprocess.check_output(["transmission-remote", "-l"])
        except subprocess.CalledProcessError, e:
            "stdout output:\n", e.output

        # Clean output
        last_item = output.split('\n')[-3]
        first_number = last_item.strip().split(' ')[0]
        return first_number

    def move_to_seed_dir(self, filename):
        if not self.seed_dir:
            logger.error("No seed_dir specified")
            return False

        return subprocess.call(["mv", "-v", filename, self.seed_dir])

    def _verify_transmission_id(self, transmission_id):
        if not self.seed_dir:
            logger.error("No seed_dir specified")
            return False

        subprocess.call(["transmission-remote", "-t", transmission_id, "--find", self.seed_dir])
        return subprocess.call(["transmission-remote", "-t", transmission_id, "-v"])

    def verify_last_transmission_id(self):
        last_tid = self._get_last_transmission_id()
        return self._verify_transmission_id(last_tid)
