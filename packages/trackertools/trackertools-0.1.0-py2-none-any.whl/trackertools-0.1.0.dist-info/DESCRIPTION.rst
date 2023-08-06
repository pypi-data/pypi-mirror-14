Manage your Gazelle tracker account
===================================

Supported:

- Gazelle trackers
- transmission-remote

.. code-block:: python

        from trackers import Tracker, Seedbox

        # Tracker
        mytracker = Tracker(username='john', password='password',
                            root_url='http://mytracker.com',
                            login_url='http://mytracker.com/login.php',
                            main_url='http://mytracker.com/torrents.php',
                            tools_server='tools.mytracker.com',
                            cookies_file="mytracker.cookie")
        mytracker.login()

        # Seedbox
        myseedbox = Seedbox(seed_dir="/home/myuser/Downloads/")
        myseedbox.add_torrent("http://mytracker.com/mytorrent.file.torrent")
        myseedbox.move_to_seed_dir("mytorrent.file")
        myseedbox.verify_last_transmission_id()


