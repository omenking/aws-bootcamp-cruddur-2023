from psycopg_pool import ConnectionPool
import os
import re
from flask import current_app as app

class Db:
  def __init__(self):
    self.init_pool()
    
  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)
  
  def print_sql(self,title,sql):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print("\n")
    print(f'{cyan}SQL Statament [{title}]-----{no_color}')
    print(sql+"\n")

  # commit /insert update
  def query_commit(self,sql,*kwargs):
   self.print_sql("query commit with returning",sql);

   pattern= r"\bRETURNING\b"
   is_returning_id =re.search(pattern,sql)
   
   conn = None
   cur = None 
   try:
        conn = self.pool.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        cur.execute(sql,kwargs)
        if is_returning_id:
          returning_id= cur.fetchone();
          
        conn.commit() 

        if is_returning_id:
          return returning_id
   except (Exception) as error:
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

  def template(self,name):
    template_path=os.path.join(app.root_path,"db","sql",name+'.sql')
    with open(template_path,'r') as f:
        template_content=f.read()
    return  template_content


db= Db()