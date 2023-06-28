from data.interfaces import RowTable


tasklist = RowTable(
    'tasklist',
    ('taskid', 'userid', 'content', 'rewarded', 'created_at', 'completed_at', 'deleted_at', 'last_updated_at','channelid','deadline'),
    'taskid'
)

members = RowTable(
    'members',
    ('guildid', 'userid',
     'tracked_time', 'coins',
     'workout_count', 'last_workout_start',
     'revision_mute_count',
     'last_study_badgeid',
     'video_warned',
     'display_name',
     '_timestamp'
     ),
    ('guildid', 'userid'),
)