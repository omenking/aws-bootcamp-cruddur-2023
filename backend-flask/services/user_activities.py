from datetime import datetime, timedelta, timezone
from opentelemetry import trace

tracer = trace.get_tracer("user-activities")
class UserActivities:
  def run(user_handle):
    with tracer.start_as_current_span("user-data"):
      span = trace.get_current_span()
      model = {
        'errors': None,
        'data': None
      }

      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("user.now", now.isoformat())
      
      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['blank_user_handle']
      else:
        now = datetime.now()
        span.set_attribute("user.now", now.isoformat())
        span.set_attribute("UserID", user_handle)
        results = [{
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Andrew Brown',
          'message': 'Cloud is fun!',
          'created_at': (now - timedelta(days=1)).isoformat(),
          'expires_at': (now + timedelta(days=31)).isoformat()
        }]
        model['data'] = results

      subsegment = xray_recorder.begin_subsegment('mock-data')
      # xray ---
      dict = {
        "now": now.isoformat(),
        "results-size": len(model['data'])
      }
      subsegment.put_metadata('key', dict, 'namespace')
      xray_recorder.end_subsegment()
    finally:  
     # Close the segment
      xray_recorder.end_subsegment()
    return model
