from momento import simple_cache_client as scc

momento_auth_token  = os.getenv('MOMENTO_AUTH_TOKEN')
momento_ttl_seconds = os.getenv('MOMENTO_TTL_SECONDS')
cache_name  = os.getenv('MOMENTO_CACHE_NAME')

class MomentoCounter:
  # get value if not present then reset
  def get(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as client:
      resp = client.get(cache_name, key)
      if resp.status() == 'hit':
        return resp.value()
      elif resp.status() == 'miss':
        client.set(cache_name, key, 0)

  #increment
  def incr(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as client:
      resp = client.get(cache_name, key)
      if resp.status() == 'hit':
        count = resp.value()
      elif resp.status() == 'miss':
        count = 0
      client.set(cache_name, key, count+1)

  # reset to zero
  def reset(key):
    with scc.SimpleCacheClient(momento_auth_token, momento_ttl_seconds) as client:
      client.set(cache_name, key, 0)