from psycopg_pool import ConnectionPool
import os


class Db:
  def __init__(self):
    self.init_pool()
    
  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)
  
  # commit /insert update
  def query_commit(self):
   conn = None
   cur = None 
   try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit() 
   except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        #conn.rollback
   finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

  # select and return json array
  def query_array_json(self,sql):
    print("SQL: array")
    print(sql)
    wrapped_sql=self.query_wrap_array(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        json=cur.fetchone()
        return json[0]

  # select and return json object
  def query_object_json(self,sql):
    print("SQL: object")
    print(sql)
    wrapped_sql=self.query_wrap_object()
    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        json=cur.fetchone()
        return json[0]

  def query_wrap_object(self,template):
    sql = f'''
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    '''
    return sql

  def query_wrap_array(self,template):
    sql = f'''
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    '''
    return sql


db= Db()