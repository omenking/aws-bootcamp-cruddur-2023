import uuid
from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb
from json

class CreateMessage:
  def run(message, user_sender_handle, user_receiver_handle):
    model = {
      'errors': None,
      'data': None
    }
    if user_sender_handle == None or len(user_sender_handle) < 1:
      model['errors'] = ['user_sender_handle_blank']

    if user_receiver_handle == None or len(user_receiver_handle) < 1:
      model['errors'] = ['user_reciever_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      # return what we provided
      model['data'] = {
        'display_name': 'Andrew Brown',
        'handle':  user_sender_handle,
        'message': message
      }
    else:
      sql = db.template('users','create_message_users')
      json = db.query_array_json(sql)
      users = json.loads(json)

      my_user    = next((item for item in dicts if item["handle"] == user_sender_handle), None)
      other_user = next((item for item in dicts if item["handle"] == user_receiver_handle), None)

      ddb = Ddb.client()

      if message_group_uuid:
        data = Ddb.create_message(
          client=ddb,
          message_group_uuid=message_group_uuid,
          message=message,
          my_user_uuid=my_user['uuid'],
          my_user_display_name=my_user['display_name'],
          my_user_handle=my_user['handle']
        )
      else:
        data = Ddb.create_message_group(
          client=ddb,
          my_user_uuid=my_user['uuid'],
          my_user_display_name=my_user['display_name'],
          my_user_handle=my_user['handle'],
          other_user_uuid=other_user['uuid'],
          other_user_display_name=other_user['display_name'],
          other_user_handle=other_user['handle']
        )
      model['data'] = data
    return model