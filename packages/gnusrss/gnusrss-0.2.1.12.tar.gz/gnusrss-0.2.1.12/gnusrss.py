#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import urllib.parse
import pycurl
import os.path
import sqlite3
import feedparser
import argparse
import sys
import hashlib
from os import listdir
from sys import argv
from xml.dom import minidom
from io import BytesIO
from html.parser import HTMLParser
from re import findall


class Database:
    """Manage the database."""
    def __init__(self, database='gnusrss.db'):
        """
        Connect to the database.

        database -- string containig the filepath of the db
            (default: gnusrss.db)
        """

        self.connection = sqlite3.connect(database)

    def create_tables(self):
        """Create table and columns."""

        current = self.connection.cursor()
        current.execute('DROP TABLE IF EXISTS items')
        current.execute('CREATE TABLE items(id INTEGER PRIMARY KEY,'
                        'feed TEXT, post TEXT, posted INTEGER, url '
                        'TEXT, lastbuild TIMESTAMP, guid TEXT)')

    def insert_data(self, param):
        """
        Insert all the article's information to the table.

        Keyword arguments:
        param -- list containing all the values
        """
        self.connection.execute('INSERT INTO items(feed, post, posted'
                                ', url, lastbuild, guid) VALUES(?, ?,'
                                '?, ?, ?, ?)', (param))
        self.connection.commit()

    def select(self, param):
        """
        Return a select.

        Keyword arguments:
        param -- string containing a sql select
        """

        current = self.connection.cursor()
        current.execute(param)
        rows = current.fetchall()

        return rows

    def close(self):
        """Close the database."""
        self.connection.close()


class myParser(HTMLParser):
    """Just a HTML parser."""
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.data = []

    def handle_data(self, data):
        self.data.append(data)

    def return_value(self):
        return ''.join(self.data)


def rss(feed, post_format):
    """
    Request the feed, parse it and return requested values on a list
    of lists.

    Keyword arguments:
    feed -- string containing the url or the filepath of the feed
    post_format -- string containing RSS keywords surrounded by {}
    """

    foo = []
    xml = feedparser.parse(feed)
    keys = list(xml.entries[0].keys())

    try:
        lastbuild = xml.entries[0].updated
    except:
        lastbuild = xml.entries[0].published_parsed

    rss_link = xml.feed.link

    for item in xml['items']:
        values = {}
        for i in keys:
            if i in post_format:
                values[i] = item[i]
        post = post_format.format(**values)

        # Stupid HTML code adding to make it complete to parse it
        post = '<html>' + post + '</html>'
        parser = myParser()
        parser.feed(post)
        post = parser.return_value()

        try:
            guid = item['guid']
        except:
            # Since the feed doesn't have a guid, I'll create it
            guid = hashlib.sha1(post.encode()).hexdigest()

        foo.append([rss_link, post, item['link'], lastbuild,
                    guid])
    return foo


def post(article, gs_node, username, password):
    """
    Post the articles to GNU Social.

    Keyword arguments:
    article -- list containing a most of what is necessary on the
        insert
    gs_node -- string containing the url of the GNU Social node
    username -- string containing the user of GNU Social
    password -- string containing the password of GNU Social
    """

    msg = article[1].split()
    api = (gs_node + '/api/statuses/update.xml')

    # Check for twitter images and call post_image if required
    for word in msg:
        if 'pic.twitter.com/' in word:
            image = post_image(word, gs_node, username, password)
            if image is not None:
                index = msg.index(word)
                msg[index] = image
            else:
                pass
    msg = ' '.join(msg)

    buffer = BytesIO()
    post_data = {'status': msg, 'source': 'gnusrss'}
    postfields = urllib.parse.urlencode(post_data)

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, api)
    curl.setopt(pycurl.USERPWD, username + ':' + password)
    curl.setopt(pycurl.VERBOSE, False)
    curl.setopt(curl.POSTFIELDS, postfields)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()
    curl.close

    response = curl.getinfo(curl.RESPONSE_CODE)

    return response


def post_image(picture, gs_node, username, password):
    """
    Upload a picture to GNU Social hosting and return a string with the
    new url.

    Keyword arguments:
    picture -- string containing the twitter url of a picture
    gs_node -- string containing the url of the GNU Social node
    username -- string containing the user of GNU Social
    password -- string containing the password of GNU Social
    """

    html = urllib.request.urlopen('https://' + picture).read().decode(
        'utf-8').splitlines()
    api = gs_node + '/api/statusnet/media/upload'
    pic = ""
    found = False

    # Search the hardcoded tag name of the picture
    for part in html:
        if picture in part:
            found == True
        if 'data-image-url' in part and found:
            pic = part.split('"')[1]
            break

    # If there's a video instead of a picture, just exit
    if not pic:
        return None
    buffer = BytesIO()

    # Pick the image and put it in the buffer
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, pic)
    curl.setopt(pycurl.VERBOSE, False)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()

    pic = buffer.getvalue()
    buffer = BytesIO()

    # Upload the buffer's image
    curl.setopt(pycurl.URL, api)
    curl.setopt(pycurl.USERPWD, username + ':' + password)
    curl.setopt(curl.HTTPPOST,
                [('media', (curl.FORM_BUFFER, 'useless.jpg',
                            curl.FORM_BUFFERPTR, pic))])
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()
    curl.close()

    buffer = buffer.getvalue().decode()
    xmldoc = minidom.parseString(buffer)
    item = xmldoc.getElementsByTagName('rsp')
    url = item.item(0).getElementsByTagName(
        'mediaurl')[0].firstChild.data

    return url


def shortener(post):
    """
    Return a shortened url.

    Keyword argument:
    post -- string containing a url to be shortened
    """

    api = ('http://qttr.at/yourls-api.php?format=xml&action=shorturl'
           '&signature=b6afeec983&url=' + post)
    buffer = BytesIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, api)
    curl.setopt(pycurl.VERBOSE, False)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()

    buffer = buffer.getvalue().decode('utf-8')

    xmldoc = minidom.parseString(buffer)
    item = xmldoc.getElementsByTagName('result')
    url = item.item(0).getElementsByTagName('shorturl')[0].\
      firstChild.data

    return url


def compare(feeds):
    """
    Compare the picked feed to the saved on the database and return
    list of lists if new.

    Keyword argument:
    feeds -- list of lists containing all actual feeds on the RSS file
    """

    db = Database()
    old = db.select('select guid from items;')
    new_feed = []
    posted = []

    # make the list accesible
    for x in old:
        posted.append(x[0])

    for feed in feeds:
        if feed[4] not in posted:
            new_feed.append(feed)

    return new_feed


def shorten_all(post):
    """
    Short all the urls from a notice.

    Keyword arguments:
    post - list containing all the data related to the post to GS
    """
    # Regex taken from stackoverflow, thanks guys
    # It doesn't identify pic.twitter.com url, which is good
    urls = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                       '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post[1])

    separate = post[1].split(' ')

    # Clean unicode carriage return
    tmp = ''
    for i in separate:
        i = i.replace(u'\xa0', u'') + ' '
        tmp += i
    separate = tmp.split(' ')

    for i in urls:
        shortened = shortener(i)
        position = separate.index(i)
        separate[position] = shortened

    post[1] = ' '.join(separate)

    return post


def get_config(name, option):
    """
    Parse config file and return it on a list.

    Keyword arguments:
    name -- string containing the config's name
    option -- string containin the section of the config to be parsed
    """

    config = []
    parser = configparser.SafeConfigParser()
    parser.read(name)

    for name, value in parser.items(option):
        config.append(value)

    return config


def create_config(config_name):
    """
    Create config file.

    Keyword argument:
    config_name -- string containing the config's name to be created
    """

    print('Hi! Now we\'ll create de config file!')
    feed = input('Please introduce the feed\'s url: ')
    username = input('Please introduce your username '
                     '(user@server.com): ')
    password = input('Please introduce your password: ')
    shorten = input('Do you need to shorten the urls that you '
                    'post? Please take in account \nthat you '
                    'should only use it if your node only has 140'
                    ' characters. \nAnswer with "yes" or just press '
                    'enter if you don\'t want to use it: ')
    fallback_feed = input('Please introduce your feed\'s fallback'
                          'url. If you don\'t want or have one,\n'
                          'just press enter: ')
    print('Now we\'re gona fetch the feed. Please wait...')
    feed_file = feedparser.parse(feed)
    keys = list(feed_file.entries[0].keys())
    print('Done! The tags are: ')
    for tag in keys:
        print('\t' + tag)
    post_format = input('The XML has been parsed. Choose wich '
                        'format you want:\nPlease put the tags '
                        'inside the square brackets\nEx: {title}'
                        ' - {link} by @{author}: ')

    config = configparser.ConfigParser()
    config['feeds'] = {}
    config['feeds']['feed'] = feed
    config['feeds']['user'] = username
    config['feeds']['password'] = password
    config['feeds']['shorten'] = shorten
    config['feeds']['fallback_feed'] = fallback_feed
    config['feeds']['format'] = post_format

    with open(config_name + '.ini', 'w') as configfile:
        config.write(configfile)


def parse_options():
    """Parse command line options of this program."""

    parser = argparse.ArgumentParser(description='Post feeds to GNU '
                                     'Social', prog='gnusrss')
    parser.add_argument('-c', '--create-config', metavar='file_name',
                        dest='create_config', help='creates a config '
                        'file')
    parser.add_argument('-C', '--create-db', dest='create_database',
                        action='store_true', help='creates the database')
    parser.add_argument('-p', '--post', metavar='config_file',
                        dest='post', help='posts feeds')
    parser.add_argument('-P', '--post-all', dest='post_all',
                        action='store_true', help='posts all feeds')
    parser.add_argument('-k', '--populate-database', metavar='file_name',
                        dest='populate_database', help='fetch the RSS and'
                        ' save it in the database')
    args = parser.parse_args()

    if args.create_database:
        if os.path.exists('gnusrss.db'):
            overwrite = input('The database already exists. Are you '
                              'sure you want to overwrite it? (y/n)')
            if overwrite == 'y':
                db = Database()
                db.create_tables()
                db.close
                print('Database created!')
        else:
            db = Database()
            db.create_tables()
            db.close()
            print('Database created!')

    if args.create_config:
        db = Database()
        create_config(args.create_config)
        config = get_config(args.create_config + '.ini', 'feeds')
        feed = config[0]
        post_format = config[5]
        posts = rss(feed, post_format)

        for article in posts:
            if config[3] is 'yes':
                shortened = shortener(article[2])
                article[2] = shortened
            db.insert_data([article[0], article[1], 1, article[2],
                            article[3], article[4]])
        db.close

    elif args.post:
        config = get_config(args.post, 'feeds')
        feed = config[0]
        fallback_feed = config[4]
        gs_node = 'https://' + config[1].split('@')[1]
        username = config[1].split('@')[0]
        password = config[2]
        post_format = config[5]

        try:
            posts = rss(feed, post_format)
        except:
            posts = rss(fallback_feed, post_format)

        posts = list(reversed(posts))
        new = compare(posts)

        if new:
            # Post only the older item
            to_post = new[0]
            db = Database()
            if config[3] == 'yes':
                to_post = shorten_all(to_post)

            posted = post(to_post, gs_node, username, password)

            if int(posted) == int('200'):
                db.insert_data([to_post[0], to_post[1], 1, to_post[2],
                                to_post[3], to_post[4]])
                db.close()

    elif args.post_all:
        for config in listdir('.'):
            if config.endswith('.ini'):
                config = get_config(config, 'feeds')
                feed = config[0]
                fallback_feed = config[4]
                gs_node = 'https://' + config[1].split('@')[1]
                username = config[1].split('@')[0]
                password = config[2]
                post_format = config[5]

                try:
                    posts = rss(feed, post_format)
                except:
                    posts = rss(fallback_feed, post_format)

                posts = list(reversed(posts))
                new = compare(posts)

                if new:
                    # Post the first posted
                    to_post = new[0]
                    db = Database()
                    if config[3] == 'yes':
                        shortened = shorten_all(to_post)

                    posted = post(to_post, gs_node, username, password)

                    if int(posted) == int('200'):
                        db.insert_data([to_post[0], to_post[1], 1,
                                        to_post[2], to_post[3], to_post[4]])
                        db.close()

    elif args.populate_database:
        config = get_config(args.populate_database, 'feeds')
        feed = config[0]
        fallback_feed = config[4]
        post_format = config[5]

        try:
            posts = rss(feed, post_format)
        except:
            posts = rss(fallback_feed, post_format)

        new = compare(posts)

        if new:
            db = Database()
            for n in new:
                if config[3] == 'yes':
                    shortened = shortener(n[2])
                    temp = n[1].split()
                    try:
                        temp[temp.index(n[2])] = shortened
                    except:
                        print('There\'s not url in the message. Please'
                            ' fix the config.')
                        import sys
                        sys.exit()

                    n[1] = ' '.join(temp)
                    n[2] = shortened

                db.insert_data([n[0], n[1], 1, n[2], n[3], n[4]])
            db.close()

    if len(argv) == 1:
        parser.print_help()


if __name__ == "__main__":
    parse_options()
