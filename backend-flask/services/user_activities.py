from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder


class UserActivities:
    def run(user_handle):
        try:
            with xray_recorder.capture('user_activity_time') as subsegment_1:
                model = {
                    'errors': None,
                    'data': None
                }

                now = datetime.now(timezone.utc).astimezone()

                dict = {
                    "now": now.isoformat(),
                    "user_handle": user_handle,
                }

                # Add metadata or annotation to sub segment-1 if necessary
                subsegment_1.put_metadata(
                    'user_metadata_key', dict, 'namespace')
                subsegment_1.put_annotation('time_now', now.isoformat())

                if user_handle == None or len(user_handle) < 1:
                    model['errors'] = ['blank_user_handle']
                else:
                    now = datetime.now()
                    results = [{
                        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
                        'handle':  'Andrew Brown',
                        'message': 'Cloud is fun!',
                        'created_at': (now - timedelta(days=1)).isoformat(),
                        'expires_at': (now + timedelta(days=31)).isoformat()
                    }]
                    model['data'] = results

            # Add metadata or annotation to subsegment 2 if necessary
            sub_segment = xray_recorder.begin_subsegment(
                "user_data.subsegment")
            sub_segment.put_annotation('user.result.length', len(results))

        finally:
            xray_recorder.end_subsegment()
        return model