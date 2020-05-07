from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
import os
from kivy.uix.checkbox import CheckBox
from kivy.utils import platform
if platform == "ios":
    from os.path import join, dirname
    import kivy.garden
    kivy.garden.garden_app_dir = join(dirname(__file__), "libs", "garden")
from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapMarkerPopup
from kivy.uix.bubble import Bubble
from kivy.garden.mapview import MapView, MapMarker

from datetime import datetime
from datetime import timedelta
from datetime import date
import pymysql
import pymysql.cursors
import time
from kivy.clock import Clock

host='cap-comp.cpwue0appyn7.us-west-2.rds.amazonaws.com'
port=3306
dbname= 'Companion'
user="admin234"
password="tf7A8sjX#!"

#hour = datetime.datetime.now().hour
#minutes = datetime.datetime.now().minute

conn = pymysql.connect(db=dbname,host=host, password=password, port=port, user=user)
cursor = conn.cursor()


#from kivy.garden.mapview.MapMarkerPopup import MapMarkerPopup 

class MainWindow(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'second'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class SecondWindow(Screen):
    
    tab_pos = 'top_mid'
    #test = SecondWindow()
    #test.update_events()
    event_update = StringProperty()
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        #this self.event_update having the value of 'new event' is for purposes of showing the utility of the
        #refresh button
        #lock.schedule_once(self.update_txt, 0.1)

    #def update_txt(self, *args):
       #count = 0
       # if (count==1):
       # #    pass
        #else:
         #   self.update_events()
        
    #self.event_update = str('new event')
    def set_marker_position(self):
       # marker = MapView.mar
        map = MapView(zoom=17, lon=-93.655, lat=41.605)
        mapview = MapView
        m1 = MapMarker(lon=-93.655, lat=41.605)
        map.add_marker(m1)
        

    def get_next_event(self):
        cursor.execute('SELECT Description, time from EVENTS order by time')
        next_event = cursor.fetchall()
        #next_event = str(next_event).strip('(')
        #next_event = str(next_event).strip('\'')
        #next_event = str(next_event).strip(',')

        '''
        dateNow = datetime.datetime.utcnow()
        dataNew = r['stream']['created_at']
        dateStart = datetime.datetime.strptime(dataNew, '%Y-%m-%dT%H:%M:%SZ')
        elapsedTime = dateNow - dateStart
        elapsedTimeHours = str(elapsedTime).split(':')
        elapsedTimeHours2 = elapsedTimeHours[0]
        elapsedTimeMinutes = elapsedTimeHours[1]
        '''

        return(next_event)
        #mapview.add_marker(MapMarkerPopup(lat=41.605,lon=-93.655, placeholder= Bubble()))
    def time_to_event(self):
        test = SecondWindow()

        events = test.get_next_event()
        dateNow = datetime.now().time()
        #print(dateNow)
        date1 = date(1, 1, 1)
        datetime1 = datetime.combine(date1, dateNow)
        #delta = timedelta(hours = 24)
        #t = dateNow
       # print(dateNow)
       # dateNow1 = datetime.combine(datetime.date(1,1,1),t) + delta.time()
       # print(dateNow1)
        #date= date.replace(2018)
        #timeNow = dateNow.time().strftime('%H:%M:%S')
        #timeNow = datetime.datetime.now().timed()
        '''
        minTime = dateNow - events[1][1]
        splitTime = str(minTime).split(' ')
        splitTime1 = splitTime[1]
        elapsedTimeHours = str(splitTime1).split(':')
        elapsedTimeHours2 = elapsedTimeHours[0]
        #elapsedTimeHours3 = elapsedTimeHours2.split(' ')
        elapsedTimeMinutes = elapsedTimeHours[1]
        #print(elapsedTimeHours2)

        minTime = int(f"{elapsedTimeHours2}{elapsedTimeMinutes}")
        '''
        testList = []
        testList1 = []
        count = 0 
        
        for i in events:
            #dataNew = i[1]
            
            #elapsedTime = dateNow - i[1]
            #hoursNow = str(dateNow).split(' ')
            
            #hoursNow1 = hoursNow[1].split(':')
            #hoursNow2 = hoursNow[1].split('.')
            #print(type(hoursNow2[0]))
            
            dateStart1 = datetime.strptime(str(i[1]), '%H:%M:%S')
            stop_time = datetime.time(dateStart1)
            #print(stop_time)
            datetime2 = datetime.combine(date1, stop_time)
            #print(dateStart)
            elapsedTime = datetime2 - datetime1

            #print(i[1])
            print(elapsedTime)
            elapsedTimeHours = str(elapsedTime).split(':')
            elapsedTimeHours2 = elapsedTimeHours[0]
            elapsedTimeHours3 = elapsedTimeHours2.split(' ')
            elapsedTimeMinutes = elapsedTimeHours[1]
            #print(hoursNow2[0])
            #print(elapsedTimeMinutes)
            #print(dateNow)
            #print(elapsedTime)
            if "day" in str(elapsedTime):
                                                                        
                test = str(elapsedTime).split('day, ')
                testList.append(str(test[1]))
                print(test)
            else:
            #elapsedTime = (int(f"{elapsedTimeHours3[1]}{elapsedTimeMinutes}"))
                testList.append(str(elapsedTime))
                #print(testList[count])
                #print(elapsedTime)
                testList1.append(i[0])
                count = count + 1

       # for i in testList:
          #  if "day" in i:
            #    i.split('')
        print(testList)
        l = sorted(enumerate(testList), key=lambda i: i[1])[:4]
        #m = sorted(range(len(testList)))[:4]
        #testList.sort(reverse=True)
        #testList1.sort(reverse=True)
        count=0
        print(l)
        #print(testList1)
        testList3 = []
        for i in testList:
            if "day" not in i:
                testList3.append(i)
            count = count + 1
        #print(testList3)
        #for i in testList3:
            #print(i)

            #print(testList.index(i))
        #print(testList1[m[0]])
        #print(testList1[5])
        #print(events[35][0])
        #print(m)
        #testList.sort()
        #print(testList)
        #print(testList)
        #print(l)
       # print(l)
        #print(testList)
        #print(events[20][0])
        return(events[l[0][0]][0], events[l[1][0]][0], events[l[2][0]][0])
        #testList.sort()
        #testList1.sort()
        #print(testList)
        #print(testList1)
            #elapsedTimeHours = str(elapsedTime).split(':')
            #elapsedTimeHours2 = elapsedTimeHours[0]
            #elapsedTimeMinutes = elapsedTimeHours[1]
           # print(elapsedTime)
            #print(i[1])
    def update_events(self,x):


        
        '''
        here we can have the number of events we want to display and dynamically change the events name
        when the app boots up, so it would also be useful to have a refresh button. The next goal for this would
        be to have the event name update by hooking up to the database, and not have to be entered manually
        via code
        '''
        test = SecondWindow()
        test.time_to_event()
        events = self.ids.event1
        events2 = self.ids.event2
        events3 = self.ids.event3
        
        '''
          Where to go from here:
      
          the code below will change to something like next_event = events.UpdateEvents() 
      
          and then next_event will do next_event.get_next_event(self)
      
          and then our labels that display the events can be changed, according to their ID's, by using
          events.text = next_event.get_next_event(self) where events in events.text is the ID of our label
      
          Looking at where the app builds (The TabbedPanelApp class), we can have the events update when 
          the application opens, and we can also utilize the refresh button in order for 
          users to obtain up-to-date information while remaining inside the application
      
        '''
        events.text = test.time_to_event()[0]
        events2.text = test.time_to_event()[1]
        events3.text = test.time_to_event()[2]
        #return(True)
    def reset_checkbox(self):
        for child in reversed(self.ids.two.children):
            if isinstance(child, CheckBox):
                child.active = False    
                
        
class DefaultWindow(Screen):
    pass
class CreateWindow(Screen):
    pass
class MapWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class PopUpWindow(Screen):
    def set_marker_position(self):
        
        x, y = mapview.get_window_xy_from(marker.lat, marker.lon, mapview.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)
        if isinstance(marker, MapMarkerPopup):
            marker.placeholder.x = marker.x - marker.width / 2
            marker.placeholder.y = marker.y + marker.height



kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv
    def get_application_config(self):
        if(not self.username):
            return super(MyMainApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(MyMainApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )


if __name__ == "__main__":
    MyMainApp().run()
