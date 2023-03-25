-- this file was manually created
INSERT INTO public.users (display_name, handle,email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown','cswkmab1@gmail.com' ,'MOCK'),
  ('Andrew Bayko', 'bayko','cswkmab7@gmail.com' ,'MOCK'),
  ('Marcus', 'cswkmab','cswkmab@gmail.com' ,'MOCK');  -- londo

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
);