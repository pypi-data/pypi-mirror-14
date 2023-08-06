hatena-haiker: Python 3 Wrapper for Hatena Haiku API
====================================================

hatena-haiker is a simple library handling `Hatena Haiku <http://h.hatena.ne.jp/>`_ API.

.. code-block:: python

    >>> import haiker
    >>> auth = haiker.OAuth(
    ...    'MyConsumerKey', 'MyConsumerSecret',
    ...     'MyAccessToken', 'MyAccessTokenSecret'
    ... )
    >>> api = haiker.Haiku(auth)
    >>> api.public_timeline(count=3)
    [{'created_at': '...',
      'favorited': '...',
      'id': '...',
      'in_reply_to_status_id': '',
      'in_reply_to_user_id': '',
      'keyword': '...',
      'link': '...',
      'replies': [...],
      'source': '...',
      'target': {...},
      'text': '....',
      'user': {'followers_count': '...',
               'id': '...',
               'name': '...',
               'profile_image_url': '...',
               'screen_name': '...',
               'url': 'http://h.hatena.ne.jp/...'}},
     {...},
     {...}]

