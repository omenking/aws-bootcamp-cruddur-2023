# Week 5 — DynamoDB

## Timezones

- What format is postgres database is being store for datetimes?
- How does psycopg3 do to datetimes when inputing or outputing?
- What format is DynamoDB table is being stored for datetimes?
- Does the system machine timezone matter?
- What does flask set as the timezone?
- Do we need to translate the datetime for python before serving?
- What does python do the datetimes converted to string for the api calls?
- What format do we need to serve the datetime to the endpoint?
- What does luxon library expect for datetime format with timezones?

## Postgres


- timestamp format: `2023-04-05 12:30:45`
- timestampz format: `2023-04-05 12:30:45+00`

The following format currently stored in postgres:
- `2023-04-15 13:15:19.922515O`

> '2023-04-15 13:15:19.922515O' represents a timestamp of April 15th, 2023 at 1:15:19.922515 PM with the microseconds (.922515) and is stored as UTC time since there is no timezone included.

What postgres says about timezones:

[Postgres Datetimes](https://www.postgresql.org/docs/current/datatype-datetime.html#:~:text=PostgreSQL%20assumes%20your%20local%20time,being%20displayed%20to%20the%20client.)

> we recommend using date/time types that contain both date and time when using time zones. We do not recommend using the type time with time zone (though it is supported by PostgreSQL for legacy applications and for compliance with the SQL standard). PostgreSQL assumes your local time zone for any type containing only date or time.

> All timezone-aware dates and times are stored internally in UTC. They are converted to local time in the zone specified by the TimeZone configuration parameter before being displayed to the client.

We can see what timezone postgres is using by running:

```
show timezone;
```

This will output:

```
-[ RECORD 1 ]-
TimeZone | UTC
```

[psycopg3 datetime adaption](https://www.psycopg.org/psycopg3/docs/basic/adapt.html#date-time-types-adaptation)

> Python datetime objects are converted to PostgreSQL timestamp (if they don’t have a tzinfo set) or timestamptz (if they do).

> PostgreSQL timestamptz values are returned with a timezone set to the connection TimeZone setting, which is available as a Python ZoneInfo object in the Connection.info.timezone attribute:

```py
conn.info.timezone
# zoneinfo.ZoneInfo(key='Europe/London')

conn.execute("select '2048-07-08 12:00'::timestamptz").fetchone()[0]
# datetime.datetime(2048, 7, 8, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/London'))
```

We don't plan to use timestamptz based on postgres recommendation and we are not so we probably don't have to worry about checking the timezone for hte connection. The underlying connection might matter.

https://docs.python.org/3/library/datetime.html