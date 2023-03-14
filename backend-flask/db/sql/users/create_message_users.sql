SELECT 
  users.uuid,
  users.display_name,
  users.handle
FROM users
WHERE
  users.handle IN(
    %(user_sender_handle)s,
    %(user_receiver_handle)s,
    )