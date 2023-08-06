Google Taskqueue client
=======================

Support for Python client for `Task Queue Rest API`_ using `gcloud`_

.. _Task Queue Rest API: https://cloud.google.com/appengine/docs/python/taskqueue/rest/
.. _gcloud: https://googlecloudplatform.github.io/gcloud-python/


Required Dependencies
---------------------

The following third-party Python modules are required:
- gcloud

The easiest way to install the dependencies is to run::

    $ pip install -r requirements.txt

Why an interface to the Task Queue API?
---------------------------------------
The Google Cloud Client Library for Python (`gcloud`_) is great, but it's missing
an interface to the Task Queue Rest API. This is understandable, because the API
is experimental and still in alpha, and not fully accesble from outside the App Egine.
And gcloud does support Pubsub.

However, Task Queues offer a few functions that aren't available in Pubsub. And
although Push Queues are restricted to use within App Engine, Pull Queues can be
used outside the App Engine enviroment.

With Pull Queues a worker can lease tasks for a certain period. During this period,
the tasks aren't available to other workers. This prevents processing a single task
multiple times by different workers. This makes Task Queues very useful for background
processing, for example in combination with object change notifications, to process
objects in a Storage Bucket the moment they are changed or created.

.. https://cloud.google.com/compute/docs/tutorials/batch-processing-with-autoscaler
.. https://cloud.google.com/appengine/docs/python/taskqueue/rest


Example
-------

Example::

    >>> from gcloud_taskqueue import Taskqueue, Client

For object change notifications, you need to create a service account. To pull tasks
created with this account, you need to use it's credentials::

    >>> json_credentials_path = "/path/to/my-service-credential.json"
    >>> client = Client.from_service_account_json(json_credentials_path, project="my-project")


Get taskqueue::

    >>> tq = Taskqueue(client=client, id="my-taskqueue")


Get tasks in taskqueue::

    >>> for task in tq.list_tasks(client=client):
    >>>     print("{}\t{}\t{}".format(task.id, task.leaseTimestamp, task.retry_count))


Lease 10 tasks for 60 seconds::

    >>> for task in tq.lease(lease_time=60, num_tasks=10, client=client):
    >>>     print("{}\t{}\t{}".format(task.id, task.leaseTimestamp, task.retry_count))


Lease 10 tasks with specific tag for 60 seconds::

    >>> for task in tq.lease(lease_time=60, num_tasks=10, tag='my-tag', client=client):
    >>>     print("{}\t{}\t{}".format(task.id, task.leaseTimestamp, task.retry_count))

