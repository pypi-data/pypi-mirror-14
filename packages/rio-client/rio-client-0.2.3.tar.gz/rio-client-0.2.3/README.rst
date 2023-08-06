rio-client
==========

Example::

    In [1]: from rio_client import *

    In [2]: client = Client('http://mysender:replace-token@rio.intra.yourcorp.com/1/myproject')

    In [3]: client.emit('post-comment-published', {'content':'Spam','content_id':1})
    Out[3]:
    {'event_uuid': u'966812c3-6f2f-4155-a733-5054f75265f1',
     'is_success': True,
      'message': u'ok',
       'task_id': u'81ca44c4-cbf6-43eb-ab39-c26159d7379f'}
