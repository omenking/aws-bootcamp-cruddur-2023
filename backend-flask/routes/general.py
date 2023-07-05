from flask import request, g

def load(app):
  @app.route('/api/health-check')
  def health_check():
    return {'success': True, 'ver': 1}, 200

  @app.route('/rollbar/test')
  def rollbar_test():
    g.rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"