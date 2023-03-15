from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb

class Messages:
  def run(message_group_uuid):
    model = {
      'errors': None,
      'data': None
    }

    ddb = Ddb.client()
    data = Ddb.list_messages(ddb, message_group_uuid)
    print("list_messages")
    print(data)

    model['data'] = data
    return model