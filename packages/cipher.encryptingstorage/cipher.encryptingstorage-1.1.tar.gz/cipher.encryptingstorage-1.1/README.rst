cipher.encryptingstorage
=========================

ZODB storage wrapper for encryption of database records.
Actually it is doing encryption and compression.


Installation manual with buildout
=================================

Follow https://pypi.python.org/pypi/keas.kmi to generate a kek.dat file::

    $ git clone https://github.com/zopefoundation/keas.kmi.git
    $ cd keas.kmi
    $ python2.7 bootstrap.py
    $ ./bin/buildout
    $ ./bin/runserver &

    $ wget https://localhost:8080/new -O kek.dat --ca-certificate sample.pem \
            --post-data=""

    $ wget https://localhost:8080/key --header 'Content-Type: text/plain' \
         --post-file kek.dat -O datakey.dat --ca-certificate sample.pem

Now copy `kek.dat` and the `keys` folder to your plone site::

    $ cp -pi kek.dat /home/yourname/Plone/training/var/kek.dat
    $ cp -pri keys /home/yourname/Plone/training/var/dek-storage


Then create a `encryption.conf` like this in your buildout directory::

    [encryptingstorage:encryption]
    enabled = true
    kek-path = /home/yourname/Plone/training/var/kek.dat
    dek-storage-path = /home/yourname/Plone/training/var/dek-storage/

Then edit buildout.cfg and add `cipher.encryptingstorage` to your eggs::

    eggs +=
        cipher.encryptingstorage

Now extend your `[instance]` ( `plone.recipe.zope2instance` )::

    zope-conf-imports =
        cipher.encryptingstorage
    zope-conf-additional =
        <zodb_db main>
          cache-size 30000
          <encryptingstorage>
            config encryption.conf
            # FileStorage database
            <filestorage>
              path ${buildout:buildout_dir}/var/filestorage/Data.fs
              blob-dir ${buildout:buildout_dir}/var/blobstorage
            </filestorage>
          </encryptingstorage>
          mount-point /
        </zodb_db>

Then run buildout::

    $ ./bin/buildout

Remove the generated <zodb_db main> entry in `parts/instance/etc/zope.conf`::

    <zodb_db main>
        # Main database
        cache-size 30000
        # Blob-enabled FileStorage database
        <blobstorage>
          blob-dir /home/yourname/Plone/training/var/blobstorage
          # FileStorage database
          <filestorage>
            path /home/yourname/Plone/training/var/filestorage/Data.fs
          </filestorage>
        </blobstorage>
        mount-point /
    </zodb_db>


Run the tests/develop
=====================

::

    $ virtualenv -p /usr/bin/python2.7 --no-site-packages .
    $ ./bin/pip install -r requirements.txt
    $ ./bin/buildout

    $ ./bin/test -v1
