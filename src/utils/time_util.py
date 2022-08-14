import datetime


def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)

    # If we are past the execution, it will take place tomorrow
    if (future_exec - now).days < 0:
        future_exec = datetime.datetime.combine(
            now + datetime.timedelta(days=1), given_time
        )

    return (future_exec - now).total_seconds()
