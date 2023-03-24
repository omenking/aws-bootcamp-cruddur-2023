select 
    users.uuid
from public.user_s
WHERE
    users.cognito_user_id=%(cognito_user_id)s
LIMIT 1