from datetime import datetime, timedelta, timezone
# X-Ray
# from aws_xray_sdk.core import xray_recorder
from lib.db import db

class UserActivities:
  def run(user_handle):
    # segment = xray_recorder.begin_segment('user_activities')
      
    model = {
      'errors': None,
      'data': None
    }
    now = datetime.now(timezone.utc).astimezone()
    dict= {
      "now": now.isoformat()
    }
    print(user_handle)
    # segment.put_metadata('key',dict,'namespace')
    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      sql = db.template("users/show")
      results = db.query_object_json(sql,{'handle': user_handle})
      model['data'] = results
    # subsegment = xray_recorder.begin_subsegment('mock-data')
    # subsegment.put_metadata('key',dict,'namespace')

    # dict= {
    #   "now": now.isoformat(),
    #   "result-size": len(model['data'])
    # }
    # xray_recorder.end_subsegment();
    print(results)
    return model