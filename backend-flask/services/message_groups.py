from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb

class MessageGroups:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }

    ddb = Ddb.client()
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'data = :my_user_uuid',
      'ExpressionAttributeValues': {
        ':my_user_uuid': {'S': brown_user_uuid}
      }
    }



    now = datetime.now(timezone.utc).astimezone()
    results = [
      {
        'uuid': '24b95582-9e7b-4e0a-9ad1-639773ab7552',
        'display_name': 'Andrew Brown',
        'handle':  'andrewbrown',
        'created_at': now.isoformat()
      },
      {
        'uuid': '417c360e-c4e6-4fce-873b-d2d71469b4ac',
        'display_name': 'Worf',
        'handle':  'worf',
        'created_at': now.isoformat()
    }]
    model['data'] = results
    return model