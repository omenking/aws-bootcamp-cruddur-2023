from datetime import timedelta
from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet, CreateCache

import os

class MomentoCounter:
  def client():
    print("MomentoCounter.client")
    momento_auth_token = CredentialProvider.from_environment_variable('MOMENTO_AUTH_TOKEN')
    momento_ttl_seconds = os.getenv('MOMENTO_TTL_SECONDS')
    ttl  = timedelta(seconds=int(momento_ttl_seconds))

    print("<><><><><><>")
    print(os.getenv('MOMENTO_AUTH_TOKEN'))

    config = {
      'configuration': Configurations.Laptop.v1(),
      'credential_provider': momento_auth_token,
      'default_ttl':  ttl
    }
    print(config)
    return CacheClient(**config)
  # get value if not present then reset
  def get(key):
    cache_name = os.getenv('MOMENTO_CACHE_NAME')
    with MomentoCounter.client() as client:
      resp = client.get(cache_name, key)
      if isinstance(resp, CacheGet.Hit):
        return int(resp.value_string) 
      elif isinstance(resp, CacheGet.Miss):
        raise "missed"
      elif isinstance(resp, CacheGet.Error):
        raise resp.inner_exception
  #increment
  def incr(key):
    cache_name = os.getenv('MOMENTO_CACHE_NAME')
    with MomentoCounter.client() as client:
      print("MomentoCounter.incr ==")
      resp = client.increment(cache_name,key,amount=1)
      print(resp)

  # reset to zero
  def reset(key):
    cache_name = os.getenv('MOMENTO_CACHE_NAME')
    with MomentoCounter.client() as client:
      resp = client.set(cache_name, key, 0)
      if isinstance(resp, CacheSet.Error):
          raise resp.inner_exception