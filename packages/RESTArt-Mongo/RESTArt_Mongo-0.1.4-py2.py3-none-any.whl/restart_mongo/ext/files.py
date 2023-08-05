from __future__ import absolute_import

import os
import uuid
from datetime import datetime

from restart.exceptions import BadRequest, MethodNotAllowed
from restart.ext.mongo.collection import Collection
from restart.ext.mongo.utils import ensure_dir


class Files(Collection):
    """The resource class for managing uploaded files.

    Storage scheme:
        1. The file content will be stored to server's file system.
        2. The file meta-data and the (extra) form data will be saved
           into the database.

        The document schema:
            {
                initial_name (The initial file name)
                storage_path (The final storage path)
                date_uploaded (The date uploaded)
                ... (The form data from request)
            }
    """

    #: The folder for storing the uploaded files.
    #: Must be a string.
    upload_folder = None

    #: The file extensions allowed to upload.
    #: Must be a tuple of strings.
    allowed_extensions = None

    #: The string format of the archive name.
    #: An archive is a folder that includes files, which are
    #: uploaded in the same time period.
    #:
    #: For example:
    #:
    #:     '%Y%m': in the same month
    #:     '%Y%m%d': on the same day (the default value)
    #:     '%Y%m%d%H': within the same hour
    archive_name_format = '%Y%m%d'

    def allowed_file(self, filename):
        assert isinstance(self.allowed_extensions, tuple), \
            'The `allowed_extensions` attribute must be a tuple object'
        return ('.' in filename and
                filename.rsplit('.', 1)[1] in self.allowed_extensions)

    def get_storage_path(self, filename, date_uploaded):
        uid = uuid.uuid4()
        _, ext = os.path.splitext(filename)
        filename = '%s%s' % (uid, ext)

        archive_name = date_uploaded.strftime(self.archive_name_format)
        storage_path = os.path.join(archive_name, filename)

        return storage_path

    def get_full_storage_path(self, storage_path):
        assert isinstance(self.upload_folder, basestring), \
            'The `upload_folder` attribute must be a string'
        return os.path.join(self.upload_folder, storage_path)

    def save_file(self, fileobj, storage_path):
        full_storage_path = self.get_full_storage_path(storage_path)
        ensure_dir(os.path.dirname(full_storage_path))

        with open(full_storage_path, 'wb') as f:
            f.write(fileobj.read())

    def remove_file(self, storage_path):
        full_storage_path = self.get_full_storage_path(storage_path)
        if os.path.isfile(full_storage_path):
            os.remove(full_storage_path)

    def get_fileobj(self, files):
        if len(files) != 1:
            raise BadRequest('One and only one file is allowed')

        fileobj = files.values()[0]
        if not self.allowed_file(fileobj.filename):
            raise BadRequest('Only file extensions (%s) are allowed' %
                             ', '.join(self.allowed_extensions))

        return fileobj

    def get_file_metadata(self, fileobj):
        """Get the file meta-data from the file object."""
        date_uploaded = datetime.now()
        storage_path = self.get_storage_path(fileobj.filename, date_uploaded)

        return dict(
            initial_name=fileobj.filename,
            storage_path=storage_path,
            date_uploaded=date_uploaded
        )

    def update_request(self, request, file_metadata):
        """Update the request object.

        Now only merge the file meta-data into the request data.
        Override to implement your own strategy.
        """
        request.data.update(file_metadata)
        return request

    def create(self, request):
        """Create a new file."""
        fileobj = self.get_fileobj(request.files)

        # Store the file content to the file system
        file_metadata = self.get_file_metadata(fileobj)
        self.save_file(fileobj, file_metadata['storage_path'])

        # Save the file meta-data and the form data into the database
        request = self.update_request(request, file_metadata)
        return super(Files, self).create(request)

    def replace(self, request, pk):
        """Replace the old file with a new one.

        You can set the `X-Keep-Storage-Path` headr as follows:

            X-Keep-Storage-Path: true

        to replace the file while still using the old storage path.
        """
        fileobj = self.get_fileobj(request.files)
        doc = self.get_doc(pk)

        # Remove the old file
        self.remove_file(doc['storage_path'])

        # Use the old storage path if `X-Keep-Storage-Path` headr is set
        file_metadata = self.get_file_metadata(fileobj)
        if request.headers.get('X-Keep-Storage-Path'):
            file_metadata['storage_path'] = doc['storage_path']

        # Store the new file content to the file system
        self.save_file(fileobj, file_metadata['storage_path'])

        # Save the new file meta-data and the form data into the database
        request = self.update_request(request, file_metadata)
        return super(Files, self).replace(request, pk)

    def update(self, request, pk):
        raise MethodNotAllowed()

    def delete(self, request, pk):
        """Delete the file."""
        doc = self.get_doc(pk)
        self.remove_file(doc['storage_path'])
        return super(Files, self).delete(request, pk)
