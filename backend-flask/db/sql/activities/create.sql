INSERT INTO public.activities (
  user_uuid,
  message,
  expires_at
)
VALUES (
  (SELECT uuid 
    FROM public.users 
    WHERE users.cognito_user_id = %(cognito_user_id)s
    LIMIT 1
  ),
  %(message)s,
  %(expires_at)s
) RETURNING uuid;