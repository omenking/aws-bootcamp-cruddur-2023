SELECT
  users.uuid
FROM public.users
WHERE
  users.handle = %(handle)s