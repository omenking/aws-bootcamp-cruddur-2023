-- this file was manually created
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  -- we can grab the cognito_user_id manually from the Congito Console
  ('Andrew Brown', 'andrewbrown' ,'7659c102-7ad4-44bd-bdc3-208f934d1f41'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )