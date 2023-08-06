#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import quote # pylint: disable=F0401
from six import text_type as unicode
import base64

from gcloud._helpers import _datetime_from_microseconds
from gcloud.exceptions import NotFound
from gcloud.iterator import Iterator


class Task(object):
    """A wrapper around Cloud Task Queue's concept of an ``Task``.

    :type id: string
    :param id: The name of the task.  This corresponds to the
                 unique path of the object in the taskqueue.

    :type taskqueue: :class:`gcloud.taskqueue.taskqueue.Taskqueue`
    :param taskqueue: The taskqueue to which this task belongs.

    """

    def __init__(self, id, taskqueue):

        self.id = id
        self.taskqueue = taskqueue
        self._description = None
        self._properties = {}

    def __repr__(self):
        if self.taskqueue:
            taskqueue_name = self.taskqueue.id
        else:
            taskqueue_name = None
        return '<Task: {}, {}>'.format(taskqueue_name, self.id)

    def _set_properties(self, value):
        """Set the properties for the current object.

        :type value: dict or :class:`gcloud.storage.batch._FutureDict`
        :param value: The properties to be set.
        """
        self._properties = value

    @staticmethod
    def path_helper(taskqueue_path, id):
        """Relative URL path for a task.

        :type taskqueue_path: string
        :param taskqueue_path: The URL path for a taskqueue.

        :type id: string
        :param id: The name of the task.

        :rtype: string
        :returns: The relative URL path for ``task_name``.
        """
        return taskqueue_path + '/tasks/' + quote(id, safe='')

    @property
    def path(self):
        """Getter property for the URL path to this Task.

        :rtype: string
        :returns: The URL path to this task.
        """
        if not self.id:
            raise ValueError('Cannot determine path without a task id.')

        return self.path_helper(self.taskqueue.path, self.id)

    @property
    def client(self):
        """The client bound to this task."""
        return self.taskqueue.client

    def delete(self, client=None):
        """Deletes a task from Task Queue.

        :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the task's taskqueue.

        :rtype: :class:`Task`
        :returns: The task that was just deleted.
        :raises: :class:`gcloud.exceptions.NotFound`
                 (propagated from
                 :meth:`gcloud.taskqueue.taskqueue.Taskqueue.delete_task`).
        """
        return self.taskqueue.delete_task(self.id, client=client)

    def update(self, new_lease_time, client=None):
        """Update the duration of a task lease

        :type new_lease_time: int
        :param new_lease_time: the new lease time in seconds.

        :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the task's taskqueue.

        :rtype: :class:`Task`
        :returns: The task that was just updated.
        :raises: :class:`gcloud.exceptions.NotFound`
                 (propagated from
                 :meth:`gcloud.taskqueue.taskqueue.Taskqueue.update_task`).
        """
        return self.taskqueue.update_task(self.id, new_lease_time=new_lease_time, client=client)

    @property
    def retry_count(self):
        """The number of leases applied to this task.

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: integer
        :returns: The number of leases applied to this task.
        """
        return int(self._properties.get('retry_count'))

    @property
    def queue_name(self):
        """Name of the queue that the task is in. Note that this name contains the
        real project name,

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: string
        :returns: Name of the queue that the task is in.
        """
        return self._properties.get('queueName')

    @property
    def tag(self):
        """The tag for this task.

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: string
        :returns: The tag for this task.
        """
        return self._properties.get('tag')


    @property
    def description(self):
        """The description for this task.

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: string
        :returns: The description for this task.
        """
        if self._description is None:
            if 'payloadBase64' not in self._properties:
                self._properties = self.taskqueue.get_task(id=self.id)._properties
            self._description = base64.b64decode(self._properties.get('payloadBase64', b'')).decode("ascii")
        return self._description

    @property
    def time_enqueued(self):
        """Retrieve the timestamp at which the task was enqueued.

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from microsecond timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get('enqueueTimestamp')
        if value is not None:
            return _datetime_from_microseconds(int(value))

    @property
    def leaseTimestamp(self):
        """Retrieve the timestamp at which the task lease will expire. If this task has never been leased,
        it will be None. If this this task has been previously leased
        and the lease has expired, this value will be < Now().

        See: https://cloud.google.com/appengine/docs/python/taskqueue/rest/tasks

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from microsecond timestamp, or
                  ``None`` if the property is not set locally. If the task has
                  not been leased, this will never be set.
        """
        value = self._properties.get('leaseTimestamp')
        if value is not None:
            return _datetime_from_microseconds(int(value))