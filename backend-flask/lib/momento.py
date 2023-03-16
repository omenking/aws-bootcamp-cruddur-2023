from momento import simple_cache_client as scc

momento_auth_token  = os.getenv('MOMENTO_AUTH_TOKEN')
momento_ttl_seconds = os.getenv('MOMENTO_TTL_SECONDS')
cache_name  = os.getenv('MOMENTO_CACHE_NAME')

class MomentoCounter:
  def get(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as cache_client:

  #increment
  def incr(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as cache_client:
      get_resp = cache_client.get(cache_name, key)
      if get_resp.status() == 'hit':
        json_data = get_resp.value()
      elif get_resp.status() == 'miss':
        json_data = get_free_courses()
        cache_client.set(cache_name, key, json_data)

  # reset to zero
  def reset(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as cache_client:
      get_resp = cache_client.get(cache_name, key)
      if get_resp.status() == 'hit':
        json_data = get_resp.value()
      elif get_resp.status() == 'miss':
        json_data = get_free_courses()
        cache_client.set(cache_name, key, json_data)