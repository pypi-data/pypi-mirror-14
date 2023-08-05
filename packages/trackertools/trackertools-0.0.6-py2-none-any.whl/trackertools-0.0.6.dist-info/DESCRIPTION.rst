Manage your Gazelle tracker account
===================================

.. code-block:: python

        from trackers import Tracker
        from collections import namedtuple

        Login = namedtuple('Login', ['username', 'password',
                                     'url',
                                     'main_url',
                                     'tools_server'])

        gazelles = {'mytracker': Login('john', 'password',
                                       'http://mytracker.com/login.php',
                                       'http://mytracker.com/torrents.php',
                                       'tools.mytracker.com'),

        mytracker = gazelles['mytracker']
        mytracker = Tracker(username=mytracker[0], password=mytracker[1],
                            login_url=mytracker[2],
                            main_url=mytracker[3],
                            tools_server=mytracker[4],
                            cookies_file="mytracker.cookie")
        mytracker.login()


