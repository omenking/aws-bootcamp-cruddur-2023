from psycopg_pool import ConnectionPool
import os
import sys
import re
from flask import current_app as app

class Db:
  def __init__(self):
    self.init_pool()
    
  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)
  
  def print_sql(self,title,sql,params={}):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print("\n")
    print(f'{cyan}SQL Statament [{title}]-----{no_color}')
    print(sql+"\n")
    self.print_params(params)

  # commit /insert update
  def query_commit(self,sql,params={}):
   self.print_sql("query commit with returning",sql,params);
   
   pattern= r"\bRETURNING\b"
   is_returning_id =re.search(pattern,sql)
   
   conn = None
   cur = None 
   try:
      with self.pool.connection() as conn:
        cur =  conn.cursor()
        cur.execute(sql,params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
          print(returning_id)
        conn.commit() 
        if is_returning_id:
          return returning_id
   except Exception as err:
      self.print_sql_err(err)
    
  # select and return json array
  def query_array_json(self,sql,params={}):
    self.print_sql("query_array_json",sql,params);

    wrapped_sql=self.query_wrap_array(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json=cur.fetchone()
        return json[0]

  # select and return json object
  def query_object_json(self,sql,params={}):
    self.print_sql("query_object_json",sql);
    self.print_params(params)
    wrapped_sql=self.query_wrap_object(sql)
    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json=cur.fetchone()
        if json == None:
          "{}"
        else:
          return json[0]
  def query_value(self,sql,params={}):
    self.print_sql('value',sql,params)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
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

  def print_template_path(self,title,templatePath):
    green = '\033[92m'
    no_color = '\033[0m'
    print("\n")
    print(f'{green}SQL Statament [{title}]-----{no_color}')
    print(templatePath+"\n")
  def print_params(self,params):
    blue = '\033[94m'
    no_color = '\033[0m'
    print(f'{blue} SQL Params:{no_color}')
    for key, value in params.items():
      print(key, ":", value)
  def template(self,*args):
    pathing= list((app.root_path,'db','sql',)+args)
    pathing[-1] = pathing[-1]+".sql"
    template_path=os.path.join(*pathing)
    self.print_sql("template",template_path);

    with open(template_path,'r') as f:
        template_content=f.read()
    return  template_content
  def print_sql_err(self,err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    #print ("pgerror:", err.pgerror)
    # print ("pgcode:", err.pgcode, "\n")

db= Db()