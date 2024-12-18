from calendar_lib.calendar import Calendar
from event_lib.event import Event
import datetime

def test_post_and_get_in_calendar():
    new_calendar=Calendar()
    #post checks:
    event1=Event(title='first event',start_time=datetime.datetime.now()+datetime.timedelta(days=2),end_time=datetime.datetime.now()+datetime.timedelta(days=3),time_zone='UTC/JERUSALEM',id='123')
    new_calendar.post_single_event(event1)
    event1_3=[]
    for n in range(3):
        e=Event(title=f'{n} event',start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),time_zone='UTC/JERUSALEM',id=f'123-{n}')
        event1_3.append(e)
    new_calendar.post_multiple_events(event1_3)

    assert len(new_calendar.get_all_events())==4 and new_calendar.get_event_by_id('123')==event1 and len(new_calendar.get_events_by_dates(datetime.datetime.now()-datetime.timedelta(days=1),datetime.datetime.now()))==3

def test_delete_in_calendar():
    new_calendar=Calendar()
    #post checks:
    event1=Event(title='first event',start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),time_zone='UTC/JERUSALEM',id='123')
    new_calendar.post_single_event(event1)
    new_calendar.delete_event_by_id('123')
    assert len(new_calendar.get_all_events())==0

def test_put_in_calendar():
    new_calendar=Calendar()
    #post checks:
    event1=Event(title='first event',start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),time_zone='UTC/JERUSALEM',id='123')
    event2=Event(title='first event',start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),time_zone='UTC/JERUSALEM',id='1234')
    new_calendar.post_single_event(event1)
    new_calendar.put_event('123',event2)

    assert new_calendar.get_event_by_id('1234')==event2