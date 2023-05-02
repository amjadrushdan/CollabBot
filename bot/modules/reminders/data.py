from data.interfaces import RowTable


reminders = RowTable(
    'reminders',
    ('reminderid','groupid', 'userid', 'remind_at', 'content', 'message_link', 'interval', 'created_at', 'title', 'footer'),
    'reminderid'
)
