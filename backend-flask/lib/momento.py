from datetime import timedelta
from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet, CreateCache

import os

class MomentoCounter:
  def client():
    momento_auth_token = CredentialProvider.from_environment_variable('MOMENTO_AUTH_TOKEN')
    ttl  = timedelta(int(os.getenv('MOMENTO_TTL_SECONDS')))
    config = {
      'configuration': Configurations.Laptop.v1(),
      'credential_provider': momento_auth_token,
      'default_ttl':  ttl
    }
    return CacheClient(**config)
  # get value if not present then reset
  def get(cache_name, key):
    cache_name = os.getenv('MOMENTO_CACHE_NAME')
    with MomentoCounter.client() as client:
      resp = client.get(cache_name, key)
      if isinstance(resp, CacheGet.Hit):
        return resp.value_string
      elif isinstance(resp, CacheGet.Miss):
        raise "missed"
      elif isinstance(resp, CacheGet.Error):
        raise resp.inner_exception
  #increment the value of a key
  def incr(cache_name, key, value = 1):
    with MomentoCounter.client() as client:
      resp = client.increment(cache_name,key,value)
      print(resp)

  # reset to zero
  def reset(cache_name, key):
    cache_name = os.getenv('MOMENTO_CACHE_NAME')
    with MomentoCounter.client() as client:
      resp = client.set(cache_name, key, 0)
      if isinstance(resp, CacheSet.Error):
          raise resp.inner_exception