import datetime as dt
from event_lib.event import Event
from event_lib.recurrence import Recurrence
from event_lib.reminder import Reminder
from calendar import Calender
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from typing import List


@dataclass
class google_calendar(Calender):

    def __init__(self,token_path,credentials_path) -> None:
        self.google_init(token_path,credentials_path)
        
    def google_init(self,token_path,credentials_path):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.creds=None
        if os.path.exists(token_path):
            self.creds= Credentials.from_authorized_user_file(token_path)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file(credentials_path,self.SCOPES)
                self.creds= flow.run_local_server(port=0)
            with open(token_path,'w') as token:
                token.write(self.creds.to_json())
        
        try:
            self.service = build("calendar", "v3", credentials=self.creds)
            calendar_list = self.service.calendarList().list().execute()
            more_5_years=dt.datetime.now()+dt.timedelta(days=2000)
            back_5_years=dt.datetime.now()-dt.timedelta(days=2000)

            for calendar_entry in calendar_list['items']:#all google calendars
                start=back_5_years.isoformat()+"Z" #more then 5 years
                google_calendar_id=calendar_entry['id']
                google_calender_Name=calendar_entry['summary']

                event_result=self.service.events().list(calendarId=google_calendar_id,timeMin=(start),timeMax=(more_5_years.isoformat()+"Z")).execute()
                events=event_result.get("items",[])

                if not events:
                    print(f'no upcoming events found in {google_calender_Name} id: {google_calendar_id}')
                else:
                    for e in events:
                        new_event=self.googleEvent_to_Event(e,google_calendar_id)
                        self.events.append(new_event)
            
            print(f'events amount: {len(self.events)}')
        except HttpError as error:
            print('An error occured: ',error)

    # POST/create funcrions
    def post_single_event(self,event:Event):
        try:
            self.service.events().insert(calendarId='primary',body=self.event_to_google_data(event)).execute()
            self.events.append(event)
        except HttpError as error:
            print('An error occured: ',error)
    def post_multiple_events(self,events:List[Event]):
        self.events.extend(events)
        try:
            for e in events:
                self.service.events().insert(calendarId='primary',body=self.event_to_google_data(e)).execute()
                self.events.append(e)
        except HttpError as error:
            print('An error occured: ',error)

    # GET/read functions    
    def get_all_events(self)->List[Event]:
        return self.events
    def get_events_by_dates(self,start:dt,end:dt)->List[Event]:
        return [e for e in self.events if e.start_time>=start and e.end_time<=end]
    def get_event_by_id(self,id)->Event:
        for e in self.events:
            if e.id==id:
                return e
        return None

    # PUT/update functions
    def put_event(self,old_event:Event,new_event:Event):
        try:
            self.delete_event(old_event)
            self.post_single_event(new_event)
            print(f"Event {old_event.id} updated successfully.")
        except HttpError as error:
            print(f"An error occurred: {error}")
    def put_event(self,old_event_id:str,new_event:Event):
        try:
            index = next((i for i, event in enumerate(self.events) if event.id == old_event_id), None)
            if index is not None:
                self.delete_event(self.events[index])
                self.post_single_event(new_event)
            else:
                raise ValueError(f'Event with id {old_event_id} not found.')
        except HttpError as error:
            print(f"An error occurred: {error}")

    # DELETE functions
    def delete_event_by_id(self,id):
        for e in self.events:
            if e.id == id:
                self.delete_event(e)
                self.events.remove(e)
    def delete_event(self,event:Event):
        try:
            self.service.events().delete(calendarId=event.google_calendar_id, eventId=event.id).execute()
            self.events.remove(event)
            print(f"Event {event.id} deleted successfully.")
        except HttpError as error:
            print(f"An error occurred: {error}")

    #google helping functions
    def googleEvent_to_Event(self,event,google_calendar_id) -> Event:
        title=event['summary']
        if event['start'].get('date')!=None:
            start=dt.datetime.strptime(event['start'].get('date'),'%Y-%m-%d')
        else:
            start=dt.datetime.strptime(event['start'].get('dateTime'),'%Y-%m-%dT%H:%M:%S%z')
        if event['end'].get('date')!=None:
            end=dt.datetime.strptime(event['start'].get('date'),'%Y-%m-%d')
        else:
            end=dt.datetime.strptime(event['start'].get('dateTime'),'%Y-%m-%dT%H:%M:%S%z')
        start=start.replace(tzinfo=dt.timezone.utc)
        end=end.replace(tzinfo=dt.timezone.utc)
        location=''
        if 'location'in event:
            location=event['location']
        description=''
        if 'description' in event:
            description=event['description']
        is_recurrence=False
        recurrence=None
        if 'recurrence' in event:
            recurrence=self.create_recurrance_from_google(event['recurrence'][0])
            is_recurrence=True
        reminders=[]
        if 'reminders' in event:
            reminders=self.create_reminders_from_google(event['reminders'])
        ids=''
        if 'id' in event:
            ids=event['id']

        new_event=Event(title=title,start_time=start,end_time=end,location=location,description=description,is_recurring=is_recurrence,recurrance_pattern=recurrence,reminders=reminders,tag=None,ID=ids,google_calendar_id=google_calendar_id)

        return new_event         
    def event_to_google_data(self,event):
        e={
            'summary':event.title,
            'location':event.location,
            'description':event.description,
            'colorId':event.tag.colorId,
            'backgroundColor':event.tag.background_color,
            'start':{
                'dateTime':event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone':event.time_zone
            },
            'end':{
                'dateTime':event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone':event.time_zone
            },
            'recurrence':[f'RRULE:FREQ={event.recurrence_pattern.frequency};COUNT={event.recurrence_pattern.count};INTERVAL={event.recurrence_pattern.interval}'],
            'attendees':[
                {'email':'totalynotexist@gmail.com'}
                ]
                ,
            'reminders':{
                'useDefault':False,
                'overrides':self.get_reminders_for_google(event)
            }
        }
        return e
    def create_recurrance_from_google(self,RRULE_str):
        rrule_dict = {}
        RRULE_str=RRULE_str[6:]
        parts = RRULE_str.split(';')
        for part in parts:
            key, value = part.split('=')
            rrule_dict[key] = value

        freq=''
        interval=None
        count=None
        until=None
        if 'FREQ' in rrule_dict:
            freq=rrule_dict['FREQ']
        if 'INTERVAL' in rrule_dict:
            interval=rrule_dict['INTERVAL']
        if 'COUNT' in rrule_dict:
            count=rrule_dict['COUNT']
        if 'UNTIL' in rrule_dict:
            until=rrule_dict['UNTIL']
        recur=Recurrence(frequency=freq,interval=interval,count=count,until=until)

        return recur   
    def create_reminders_from_google(self,reminders):

        reminders=[]
        if reminders['useDefault']==False and 'overrides' in reminders:
            for remind in reminders['overrides']:
                new_remind=Reminder(method=remind['method'],minutes=int(remind['minutes']))
        else:
            new_remind=Reminder()
        reminders.append(new_remind)
        return reminders
    def get_reminders_for_google(self,event):
        arr=[]
        for r in event.reminders:
            arr.append(r.to_dict())
        return arr

 
