select 
    users.uuid
from public.users
WHERE
    users.cognito_user_id=%(cognito_user_id)s
LIMIT 1