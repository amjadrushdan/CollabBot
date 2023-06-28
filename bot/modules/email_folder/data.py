from cachetools import TTLCache
from data.interfaces import RowTable


email_data = RowTable(
    'user_config',
    ('userid', 'timezone', 'topgg_vote_reminder', 'avatar_hash', 'gems','useremail'),
    'userid',
    cache=TTLCache(5000, ttl=60*5)
)
