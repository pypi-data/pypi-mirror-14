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
from subprocess import call
from multiprocessing import Process, Pool
import types, copy_reg

# This allows multiprocessing to pickle class methods
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

# Set up the logger
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

wdir=os.path.abspath(os.path.dirname(__file__))


class Tracker(object):

    def __init__(self, username, password, login_url, main_url, cookies_file, tools_server=None):
        self.username = username
        self.password = password
        self.login_url = login_url
        self.main_url = main_url
        self.tools_server = tools_server
        self.cookies_file = cookies_file
        self.br = mechanize.Browser()
        self.logged_in = False

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

        if os.path.isfile(os.path.join(wdir, self.cookies_file)) and not invalidate_cookies:
            logger.debug("Found %s" % self.cookies_file)
            cj.load(os.path.join(wdir, self.cookies_file), ignore_discard=True, ignore_expires=True)
            torrent_index = self.main_url
            logger.debug("Opening url...%s" % torrent_index)
            resp = br.open(torrent_index)
            if "login.php" in resp.geturl():
                logger.debug("Bad url.  Invalidating cookies...")
                self.login(invalidate_cookies=True)
        else:
            # Check if existing cookies work
            resp = br.open(self.login_url)

            br.select_form(nr=0) # select second form in page (0 indexed)
            br['username'] = self.username
            br['password'] = self.password
            response = br.submit()

            logger.debug("Saving cookies after login form")
            cj.save(os.path.join(wdir, self.cookies_file), ignore_discard=True, ignore_expires=True)
            logger.debug("Logged in to %s" % response.geturl())

        self.logged_in = True
        return self.logged_in

    def query_isbn(self, isbn, tools_server=None):
        if not tools_server:
            tools_server = self.tools_server
        logger.info("+++++++++++++++++++++++++++++++")
        logger.info("querying %s -- Start" % isbn)
        url='http://%s/search.php?keyword=%s' % (tools_server, isbn)
        r = requests.get(url)
        json_data = json.loads(r.text)
        logger.info("querying %s -- Done!" % isbn)
        return json_data

    def get_epub(self, url):
        logger.info(url)
        if not self.logged_in:
            logger.debug("Not logged in.")
            return False

        resp = self.br.open(url)
        write_text_to_file("torrent_page.html", resp.read())

    def _get_torrent_info(self, url):
        logger.info(url)
        if not self.logged_in:
            logger.debug("Not logged in.")
            return False

        resp = self.br.open(url)
        doc = lh.document_fromstring(resp.read())

        return parse_torrent_page(doc=doc)

    def download_torrent_from_url(self, url):
        torrent_info = self._get_torrent_info(url)
        download_url = torrent_info['download_url']
        logger.debug("download_url is %s" % download_url)
        logger.info("Downloading torrent...")
        torrent_resp = self.br.open(download_url)
        with open(os.path.join(wdir, torrent_info['slug']),'w') as f:
            f.write(torrent_resp.read())
            logger.info("Wrote to file %s" % torrent_info['slug'])

    def add_ebook_format(self, url, isbn, torrent_file, format='MOBI', debug_write_to_file=False):
        if not self.logged_in:
            logger.debug("Not logged in.")
            return False

        logger.info("Opening %s...", url)
        resp = self.br.open(url)

        # Get the right form
        for form in self.br.forms():
            if form.attrs.get('id') == 'upload_table':
                self.br.form = form
                break

        if not self.br.form:
            logger.info("Missing form on %s" % url)
            return False

        # fill out the form
        logger.debug(self.br.form)
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
        logger.debug(self.br.form)

        req = self.br.submit()
        logger.debug(req.geturl())

        if debug_write_to_file:
            html = resp.read()
            filename = "add_ebook_format.html"
            logger.info("Writing url to file %s" % filename)
            write_text_to_file(filename, html)

    def transmission_add_torrent_from_url(self, url):
        torrent_info = self._get_torrent_info(url)
        download_url = torrent_info['download_url']
        logger.info('adding to transmission: %s' % download_url)
        call(["transmission-remote", "-a", download_url])
        logger.debug('Done! adding to transmission: %s' % download_url)
