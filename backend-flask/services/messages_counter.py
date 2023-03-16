from datetime import datetime, timedelta, timezone

from lib.db import db
from lib.momento import MomentoCounter

class MessageGroups:
  def run(cognito_user_id):
    sql = db.template('users','handle_from_cognito_user_id')
    user_handle = db.query_value(sql)

    print('MessageGroups.user_handle')
    print(user_handle)

    count = MomentoCounter.get(f"msgs/{user_handle}")

    print('MessageGroups.count')
    print(count)
    return count