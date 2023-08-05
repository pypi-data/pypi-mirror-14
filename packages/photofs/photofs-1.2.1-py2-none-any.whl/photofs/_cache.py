# coding: utf-8
# photofs
# Copyright (C) 2012-2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import errno
import os
import sqlite3
import threading


class CachedFile(object):
    def __init__(self, path, size, condition):
        """A readable file-like object with blocking reading.

        :param str path: The path of the file.

        :param int size: The size of the file. This may be greater than the
            actual size of the file. Reading beyond this position will return no
            data.

        :param threading.Condition condition: A condition that will be waited
            upon when reading past the actual end of the file is requested. The
            process writing data to the file is responsible for signalling this
            when more data becomes available.
        """
        super(CachedFile, self).__()
        self._file = open(path, 'rb')
        self._size = size
        self._condition = condition



class Cache(object):
    """A cache of file resources.
    """
    def __init__(self, base, name):
        """Creates a cache.

        :param str base: The base directory for caching. This directory is
            expected to exist

        :param str name: The name of the cache.

        :raises OSError: if the cache directory does not exist and cannot be
            created
        """
        self._path = os.path.join(base, name)
        self._name = name

        # Make sure the directory exists
        try:
            os.mkdir(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self._db_lock = threading.RLock()
        self._db_cursors = []
        self._db = sqlite3.connect(
            os.path.join(os.path.join(base, name + '.db')),
            check_same_thread = False)
        self._upgrade_tables()

        self._files_lock = threading.RLock()
        self._files = {}

    @property
    def path(self):
        """The path to the cache directory."""
        return self._path

    @property
    def name(self):
        """The name of this cache."""
        return self._name

    def get(self, image_id, *args, **kwargs):
        """Retrieves a file object associated with an image ID.

        :param str image_id: The unique ID of the image.

        :param args: Positional arguments passed on to :meth:`open` if the image
            is not fully cached.

        :param kwargs: Keyword arguments passed on to :meth:`open` if the image
            is not fullkypy cached.

        :return: an object supporting the *FUSE* read protocol
        """
        with self._files_lock:
            try:
                return self._files[image_id]
            except KeyError:
                self._files[image_id] = self.open(image_id, *args, **kwargs)
                return self._files[image_id]

    def open(self, *args, **kwargs):
        """Actually opens a file.

        The object returned supports the *FUSE* read protocol, and has the
        attributes ``size``, which is the total size, and ``timestamp``, which
        is the timestamp of the image.

        :return: a file object
        """
        raise NotImplementedError()

    def __enter__(self):
        self._db_lock.acquire()
        self._db_cursors.append(self._db.cursor())
        return self._db_cursors[-1]

    def __exit__(self, exc_type, exc_value, tb):
        try:
            self._db_cursors.pop().close()
        finally:
            self._db_lock.release()

    def _commit(self):
        """Commits the current transaction.

        This method calls :meth:`sqlite.
        """
        self._db.commit()

    @property
    def _db_version(self):
        """The current database version."""
        with self as cursor:
            try:
                cursor.execute('''
                    SELECT MAX(number) FROM Version''')
                number, = cursor.fetchone()
                return number
            except sqlite3.OperationalError:
                return 0

    def _upgrade_tables(self):
        """Upgrades the database to the current version.
        """
        while True:
            # Get the current version and see if we have a next version
            version = self._db_version
            try:
                create_tables = getattr(self,
                    '_create_tables_%d' % (version + 1))
            except AttributeError:
                # We have moved past the latest version
                break

            # Upgrade the database to the next version
            with self as cursor:
                create_tables(cursor)
                cursor.execute('''
                    INSERT INTO Version (number)
                        VALUES (?)''',
                    (version + 1,))
                self._commit()

    def _create_tables_1(self, cursor):
        """Creates the ``Version`` table.

        :param sqlite.Cursor: The database cursor to use.
        """
        cursor.execute('''
            CREATE TABLE Version (
                number INT,
                date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP)''')

    def _create_tables_2(self, cursor):
        """Creates the ``Image`` table.

        :param sqlite.Cursor: The database cursor to use.
        """
        cursor.execute('''
            CREATE TABLE Image (
                id TEXT
                    NOT NULL,
                size INT
                    NOT NULL,
                timestamp TEXT
                    NOT NULL,
                CONSTRAINT UNIQUE_Image_id
                    UNIQUE (id))''')
        cursor.execute('''
            CREATE INDEX Image_id
                ON Image(id)''')

    def _image_get(self, image_id):
        """Reads a row from the ``Image`` table.

        :param str image_id: The ID of the image.

        :return: the tuple ``(size, timestamp)``

        :raises KeyError: if ``image_id`` is not a known ID
        """
        with self as cursor:
            cursor.execute('''
                SELECT size, datetime(timestamp) FROM Image
                    WHERE id = ?''',
                (image_id,))
            result = cursor.fetchone()
            if result is None:
                raise KeyError(image_id)
            else:
                return result

    def _image_add(self, image_id, size, timestamp):
        """Adds a row to the ``Image`` table.

        :param str image_id: The ID of the image.

        :param int size: The size of the image.

        :param timestamp: The timestamp of the image.
        """
        with self as cursor:
            cursor.execute('''
                INSERT INTO Image (id, size, timestamp)
                    VALUES (?, ?, ?)''',
                (image_id, size, timestamp))
            self._commit()

    def _image_del(self, image_id):
        """Deletes a row from the ``Image`` table.

        :param str image_id: The ID of the image.

        :raises KeyError: if ``image_id`` is not a known ID
        """
        with self as cursor:
            cursor.execute('''
                DELETE FROM Image
                    WHERE id = ?''',
                (image_id,))
            if cursor.rowcount < 1:
                raise KeyError(image_id)
            self._commit()

    def _image_path(self, image_id):
        """Returns the full path for an image.

        :param str image_id: The ID of the image.

        :return: the full path of the image

        :rtype: str
        """
        return os.path.join(self.path, image_id)

    def _open(self, image_id, *args, **kwargs):
        """Opens a file.

        If a cache of the file exists, and its size is as is stored in the
        database, the actual cached file will be opened and a normal ``file``
        object will be returned.

        If the file does not exist in the database or on disk, or the size on
        disk is less that the size in the database, :meth:`open` will be called
        with all parameters passed to this method.

        :param str image_id: The unique ID of the image.

        :param args: Positional arguments passed on to :meth:`open`.

        :param kwargs: Keyword arguments passed on to :meth:`open`.
        """
        # Read the expected size from the database
        try:
            size, timestamp = self._image_get(image_id)
        except KeyError:
            # The image does not exist in the database; add it and then open an
            # actual file
            image = self.open(image_id, *args, **kwargs)
            self._image_add(image_id, image.size, image.timestamp)
            return image

        # Check the size of the file cache
        path = self._image_path(image_id)
        st = os.stat(path)
        if st.st_size == size:
            # The cached file is complete; simply return it
            return open(path, 'rb')

        return self.open(image_id, *args, **kwargs)
