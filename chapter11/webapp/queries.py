SQL_SESSIONS = """
    select distinct ts from times
"""


SQL_SWIMMERS_BY_SESSION = """
    select distinct swimmers.name, swimmers.age  
    from times, swimmers 
    where date(times.ts) = ? and     
    times.swimmer_id = swimmers.id 
    order by name
"""


SQL_SWIMMERS_EVENTS_BY_SESSION = """  
    select distinct events.distance, events.stroke
    from swimmers, events, times
    where times.swimmer_id = swimmers.id and
    times.event_id = events.id and
    (swimmers.name = ? and swimmers.age = ?) and
    date(times.ts) = ?
"""


SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION = """
    select times.time
    from swimmers, events, times
    where (swimmers.name = ? and swimmers.age = ?) and
    (events.distance = ? and events.stroke = ?) and 
    swimmers.id = times.swimmer_id and
    events.id = times.event_id and
    date(times.ts) = ?
"""
