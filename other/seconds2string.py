def seconds_to_string(seconds: int = 0, outstr: str = "%wweeks, %ddays %h:%m.%s"):
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    if seconds >= 604800:
        while seconds >= 604800:
            seconds = seconds - 604800
            weeks = weeks + 1
    if seconds >= 86400:
        while seconds >= 86400:
            seconds = seconds - 86400
            days = days + 1
    if seconds >= 3600:
        while seconds >= 3600:
            seconds = seconds - 3600
            hours = hours + 1
    if seconds >= 60:
        while seconds >= 60:
            seconds = seconds - 60
            minutes = minutes + 1
    result = outstr.replace("%w",str(weeks)).replace("%d",str(days)).replace("%h",str(hours)).replace("%m",str(minutes)).replace("%s",str(seconds))
    return result
    
# EXAMPLE
print(seconds_to_string(1000000))
