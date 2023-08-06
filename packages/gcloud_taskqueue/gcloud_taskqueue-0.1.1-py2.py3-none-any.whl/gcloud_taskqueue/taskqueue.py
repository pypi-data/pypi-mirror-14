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
import base64
import os

from gcloud.exceptions import NotFound
from gcloud.iterator import Iterator

from gcloud_taskqueue.task import Task


class _TaskIterator(Iterator):
    """An iterator listing tasks in a taskqueue

    You shouldn't have to use this directly, but instead should use the
    :class:`gcloud.taskqueue.taskqueue.Taskqueue.list_tasks` method.

    :type taskqueue: :class:`gcloud.taskqueue.taskqueue.Taskqueue`
    :param taskqueue: The taskqueue from which to list tasks.

    :type extra_path: string
    :param extra_path: path to list tasks from

    :type client: :class:`gcloud.storage.client.Client`
    :param client: Optional. The client to use for making connections.
                   Defaults to the taskqueue's client.
    """

    def __init__(self, taskqueue, extra_path="/tasks", client=None):
        if client is None:
            client = taskqueue.client
        self.taskqueue = taskqueue
        super(_TaskIterator, self).__init__(client=client, path=taskqueue.path + extra_path)

    def get_items_from_response(self, response):
        """Yield :class:`.taskqueue.task.Task` items from response.

        :type response: dict
        :param response: The JSON API response for a page of tasks.
        """
        for item in response.get('items', []):
            id = item.get('id')
            task = Task(id, taskqueue=self.taskqueue)
            task._set_properties(item)
            yield task


class Taskqueue(object):
    """A class representing a TaskQueue on Cloud Task Queue.

    :type client: :class:`gcloud.taskqueue.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the taskqueue (which requires a project).

    :type id: string
    :param id: The name of the taskqueue.
    """

    _iterator_class = _TaskIterator

    def __init__(self, client, id):
        self._client = client
        self._full_name = None
        self.id = id
        assert self.exists()  # necessary to update path with prefixed project name

    def __repr__(self):
        return '<Taskqueue: {}>'.format(self.id)

    @property
    def client(self):
        """The client bound to this taskqueue."""
        return self._client

    @property
    def project(self):
        """Project bound to the topic."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in taskqueues / tasks APIs"""
        if self._full_name is None:
            self._full_name = 'projects/{project}/taskqueues/{taskqueue}'.format(project=self.project,
                                                                                 taskqueue=self.id)
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        self._full_name = full_name

    @property
    def path(self):
        """URL path for the taskqueue's APIs"""

        return '/{full_name}'.format(full_name=self.full_name)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`taskqueue.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current topic.

        :rtype: :class:`taskqueue.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def exists(self, client=None):
        """API call:  test for the existence of the taskqueue via a GET request

        See
        https://cloud.google.com/appengine/docs/python/taskqueue/rest/taskqueues/get

        :type client: :class:`taskqueue.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current taskqueue.
        """
        client = self._require_client(client)
        try:
            response = client.connection.api_request(method='GET', path=self.path)
        except NotFound:
            return False
        else:
            # projectname gets prefixed, this retrieves correct path with prefixed project name
            # see https://code.google.com/p/googleappengine/issues/detail?id=10199
            if os.path.split(response.get("id"))[-1] == self.id:
                self.full_name = response.get("id")
                return True
            else:
                return False


def delete_task(self, id, client=None):
    """Deletes a task from the current task queue.

    If the task isn't found (backend 404), raises a
    :class:`gcloud.exceptions.NotFound`.

    :type id: string
    :param id: A task name to delete.

    :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
    :param client: Optional. The client to use.  If not passed, falls back
                   to the ``client`` stored on the current taskqueue.

    :raises: :class:`gcloud.exceptions.NotFound`
    """
    client = self._require_client(client)
    task = Task(taskqueue=self, id=id)

    # We intentionally pass `_target_object=None` since a DELETE
    # request has no response value (whether in a standard request or
    # in a batch request).
    client.connection.api_request(method='DELETE', path=task.path, _target_object=None)


def get_task(self, id, client=None):
    """Gets a named task from taskqueue

    If the task isn't found (backend 404), raises a
    :class:`gcloud.exceptions.NotFound`.
    :type id: string
    :param id: A task name to get

    :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
    :param client: Optional. The client to use.  If not passed, falls back
                   to the ``client`` stored on the current taskqueue.

    :rtype: :class:`_Task`.
    :returns: a task
    :raises: :class:`gcloud.exceptions.NotFound`
    """
    client = self._require_client(client)
    task = Task(taskqueue=self, id=id)
    try:
        response = client.connection.api_request(method='GET', path=task.path, _target_object=task)
        task._set_properties(response)
        return task
    except NotFound:
        return None


def list_tasks(self, client=None):
    """Return an iterator used to find tasks in the taskqueue.

    :rtype: :class:`_TaskIterator`.
    :returns: An iterator of tasks.
    """
    return self._iterator_class(self, client=client)


def lease(self, lease_time, num_tasks, group_by_tag=False, tag=None, client=None):
    """ Acquires a lease on the topmost N unowned tasks in the specified queue.

    :type lease_time: int
    :param lease_time: How long to lease this task, in seconds.

    :type num_tasks: int
    :param num_tasks: The number of tasks to lease.

    :type group_by_tag: bool
    :param group_by_tag: Optional. When True, returns tasks of the same tag. Specify which tag by using the
    tag parameter. If tag is not specified, returns tasks of the same tag as the oldest task in the queue.

    :type tag: string
    :param tag: Optional. Only specify tag if groupByTag is true. If groupByTag is true and tag is not specified,
    the tag is assumed to be that of the oldest task by ETA. I.e., the first available tag.

    :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
    :param client: Optional. The client to use.  If not passed, falls back
                   to the ``client`` stored on the task's taskqueue.

    :rtype: :class:`_TaskIterator`.
    :returns: An iterator of tasks.
    """
    client = self._require_client(client)

    if group_by_tag:
        query_params = {"leaseSecs": lease_time, "numTasks": num_tasks, "groupByTag": group_by_tag, "tag": tag}
    else:
        query_params = {"leaseSecs": lease_time, "numTasks": num_tasks}
    response = client.connection.api_request(method='POST', path=self.path + "/tasks/lease",
                                             query_params=query_params)

    for item in response.get('items', []):
        id = item.get('id')
        task = Task(id, taskqueue=self)
        task._set_properties(item)
        yield task


def update_task(self, id, new_lease_time, client=None):
    """ Updates the duration of a task lease

    If the task isn't found (backend 404), raises a
    :class:`gcloud.exceptions.NotFound`.

    :type id: string
    :param id: A task name to update

    :type new_lease_time: int
    :param new_lease_time: New lease time, in seconds.

    :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
    :param client: Optional. The client to use.  If not passed, falls back
                   to the ``client`` stored on the task's taskqueue.

    :rtype: :class:`_Task`.
    :returns: a task
    :raises: :class:`gcloud.exceptions.NotFound`
    """
    client = self._require_client(client)
    task = Task(taskqueue=self, id=id)
    try:
        response = client.connection.api_request(method='POST', path=self.path + "/tasks/" + id,
                                                 query_params={"newLeaseSeconds": new_lease_time},
                                                 _target_object=task)
        task._set_properties(response)
        return task
    except NotFound:
        return None


def insert_task(self, description, tag=None, client=None):
    """ Insert task in task queue.

    If the task isn't found (backend 404), raises a
    :class:`gcloud.exceptions.NotFound`.

    :type description: string
    :param description: Description of task to perform

    :type tag: string
    :param tag: Optional. The tag for this task, allows leasing tasks with a specific tag

    :type client: :class:`gcloud.taskqueue.client.Client` or ``NoneType``
    :param client: Optional. The client to use.  If not passed, falls back
                   to the ``client`` stored on the task's taskqueue.

    :rtype: :class:`_Task`.
    :returns: a task
    :raises: :class:`gcloud.exceptions.NotFound`
    """
    client = self._require_client(client)

    new_task = {
        "queueName": self.full_name,
        "payloadBase64": base64.b64encode(description).decode('ascii'),
        "tag": tag
    }

    response = client.connection.api_request(method='POST', path=self.path + "/tasks/", data=new_task)
    task = Task(taskqueue=self, id=response.get('id'))
    task._set_properties(response)
    return task
