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
from kivy.uix.button import Button
from kivy.uix.layout import Layout
#import kivy
from kivy.uix.label import Label
from  kivy.core.window import Window
import pymysql.cursors
import time
from kivy.clock import Clock
#import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import hashlib
import os
import hashlib, binascii, os
import base64

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
        test = MainWindow()
        checkUser = False
        cursor.execute('SELECT User, Pass from LOGIN321')
        logins = cursor.fetchall()
        salt = os.urandom(32)
        app.username = loginText
        app.password = passwordText
        #print(logins[0][1])

        for i in logins:
            if(test.verify_password(i[1], app.password)==True and i[0]==app.username):
                checkUser = True
                break
            #print(i[1])
        print(checkUser)
            #print('here' + str(test.verify_password(i[1], app.password)))
        global login123
        login123 =loginText
       # new_key = hashlib.pbkdf2_hmac(
         #   'sha256',
         #   app.password.encode('utf-8'), # Convert the password to bytes
         #   salt, 
         #   100000
         #   )
        #login123 = ''
        layout = GridLayout(cols = 1)
        #popupLabel = Label(text = "Incorrect Login Information") 
        closeButton = Button(text = "Close") 
  
        #layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)

        popup = Popup(title ='Incorrect Login Information', 
                      content = layout,
                      size_hint=(None, None), size=(500,200))   
        #popup.open()    
  
        # Attach close button press with popup.dismiss action 
        #closeButton.bind(on_press = popup.dismiss)
        #print(logins[0][1])
        
        count = 0
        '''
        for i in logins:
            print(i[1])
            if i[0] == app.username and i[1] == app.password:
                checkUser = True
                break
        '''

       # print(app.username)
        if checkUser == True:

            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'second'
        else:
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)

        app.config.read(app.get_application_config())
        app.config.write()
    def login_user(self):
        login123 = self.ids.login.text
        print(login123)
        return(login123)
    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000,
                                      dklen=45)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
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
        cursor.execute('SELECT Description, Time, EventID from EVENTS order by time')
        next_event = cursor.fetchall()
        #cursor.close()
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
            #print(elapsedTime)
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
                #print(test)
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
        #print(testList)
        testList6 = [None] * len(testList)
        count = 0
        for i in testList:
            testList5=i.split(":")
            testList6[count] =(int(f"{testList5[0]}{testList5[1]}"))
            count = count +1
        #print(testList6)
        l = sorted(enumerate(testList6), key=lambda i: i[1])
        #m = sorted(range(len(testList)))[:4]
        #testList.sort(reverse=True)

        #testList1.sort(reverse=True)
        count=0
        #testList.sort()
        #print(testList)
        #print(l)
        #print(testList1)
        testList3 = []
        for i in testList:
            if "day" not in i:
                testList3.append(i)
            count = count + 1
        #print(testList3)
        #for i in testList3:
            #print(i)
       # print(events[0][2])
        #print(l)
        #print(events[l[len(l)-1][0]][2])
        #print(events[l[len(l)-2][0]][2])
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
        #cursor.close()
        print(events[0][1])
        return(events[l[0][0]][0], events[l[1][0]][0], events[l[2][0]][0], events[l[len(l)-1][0]][2], events[l[len(l)-2][0]][2], events[l[len(l)-3][0]][2], events[l[0][0]][1],events[l[1][0]][1], events[l[2][0]][1])
        #testList.sort()
        #testList1.sort()
        #print(testList)
        #print(testList1)
            #elapsedTimeHours = str(elapsedTime).split(':')
            #elapsedTimeHours2 = elapsedTimeHours[0]
            #elapsedTimeMinutes = elapsedTimeHours[1]
           # print(elapsedTime)
            #print(i[1])
    def update_results(self,x):
        
        '''
        here we can have the number of events we want to display and dynamically change the events name
        when the app boots up, so it would also be useful to have a refresh button. The next goal for this would
        be to have the event name update by hooking up to the database, and not have to be entered manually
        via code
        '''
        test = SecondWindow()
        test.time_to_event()
        events = self.ids.result1
        events2 = self.ids.result2
        events3 = self.ids.result3
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(test.time_to_event()[3])
        cursor.execute(query)
        next_result = cursor.fetchall()
        #$resultID = test.time_to_event()[3]
        
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(test.time_to_event()[4])
        cursor.execute(query)
        next_result1 = cursor.fetchall()
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(test.time_to_event()[5])
        cursor.execute(query)
        next_result2 = cursor.fetchall()
        #print(next_result[0][0])
        #print("time to event: " + str(test.time_to_event()[3]))
        
        events.text = str(next_result[0][0]) + " Winner:  " + str(next_result[0][1]) + " " + str(next_result[0][2] + " of " + str(next_result[0][4]))
        events2.text = str(next_result1[0][0]) + " Winner:  " + str(next_result1[0][1]) + " " + str(next_result1[0][2] + " of " + str(next_result1[0][4]))
        events3.text = str(next_result2[0][0]) + " Winner:  " + str(next_result2[0][1]) + " " + str(next_result2[0][2] + " of " + str(next_result2[0][4]))

        #cursor.close()
        #events2.text = test.time_to_event()[4]
        #events3.text = test.time_to_event()[5]
        #events2.text = test.time_to_event()[4]
        #events3.text = test.time_to_event()[5]
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
        time = self.ids.time1
        time1 = self.ids.time2
        time2 = self.ids.time3
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
        time.text = str(test.time_to_event()[6])
        time1.text = str(test.time_to_event()[7])
        time2.text = str(test.time_to_event()[8])

        #return(True)
    def reset_checkbox(self):
        test = SecondWindow()
        test1 = MainWindow()
        #userName1 = test1.login_user()
        print(login123)
        layout = GridLayout(cols = 1)
        #popupLabel = Label(text = "Incorrect Login Information") 
        closeButton = Button(text = "Close") 
  
        #layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)

        popup = Popup(title ='Already Submitted Interest for this Event', 
                      content = layout,
                      size_hint=(None, None), size=(500,200)) 
        interest1 = False
        interest2 = False
        interest3 = False
       # print(login123)
        #app = App.get_running_app()
        #print(app.ids.login.text)
        sql = "SELECT User, Event FROM DUPLICATE"
        cursor.execute(sql)
        duplicate = cursor.fetchall()
        print(duplicate[0])
        for i in duplicate:
            if i[0] == login123 and i[1] == test.time_to_event()[0]:
                interest1=True 
            elif i[0] == login123 and i[1] == test.time_to_event()[1]:
                interest2=True
            elif i[0] == login123 and i[1] == test.time_to_event()[2]:
                interest3=True
        
        if interest1 == True:
            layout = GridLayout(cols = 1)
        #popupLabel = Label(text = "Incorrect Login Information") 
            closeButton = Button(text = "Close") 
      
            #layout.add_widget(popupLabel) 
            layout.add_widget(closeButton)

            popup = Popup(title ='Already Submitted Interest for this Event', 
                      content = layout,
                      pos_hint={'x': 600.0 / Window.width, 
                            'y':600.0 /  Window.height},
                      size_hint=(None, None), size=(500,200)) 
        check1 = self.ids.check1
        check2 = self.ids.check2
        check3 = self.ids.check3
        test.time_to_event()
        if(check1.active==True and interest1==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(test.time_to_event()[0], test.time_to_event()[6])
            cursor.execute(sql)
            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, test.time_to_event()[0])
            cursor.execute(sql)
            #interest1 = True
            print('here')
            conn.commit()
        elif(check1.active==True and interest1==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)
            

            #print(test.time_to_event()[0])
        if(check2.active==True and interest2==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(test.time_to_event()[1],test.time_to_event()[7])
            cursor.execute(sql)
            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, test.time_to_event()[1])
            cursor.execute(sql)
            #interest2 = True
            conn.commit()
        elif(check2.active==True and interest2==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)
        if(check3.active==True and interest3==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(test.time_to_event()[2],test.time_to_event()[8])
            cursor.execute(sql)
            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, test.time_to_event()[2])
            cursor.execute(sql)
            #interest3 = True
            conn.commit()
        elif(check3.active==True and interest3==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)
        for child in reversed(self.ids.two.children):
            if isinstance(child, CheckBox):
                child.active = False

    def update_interest(self,x): 
        test = SecondWindow()
        sql = "SELECT Description, Time, COUNT(*) occurences FROM INTEREST GROUP BY Description HAVING COUNT(*)>1 ORDER BY occurences DESC "#i#nsertStatement = "INSERT INTO LOGIN321  (User, Pass)   VALUES('test', 'user')"
        cursor.execute(sql)
        interest = cursor.fetchall()
        #print(interest[1][0])
        events1 = self.ids.interest1
        events2 = self.ids.interest2
        events3 = self.ids.interest3
        try:
            events1.text = str(interest[0][0]) + " taking place at " + str(interest[0][1])
        except:
            x = 1
        try:
            events2.text = str(interest[1][0]) + " taking place at " + str(interest[1][1])
        except:
            x=1
        try:
            events3.text = str(interest[2][0]) + " taking place at " + str(interest[2][1])
        except:
            x=1

        #events1.text = 
        
class DefaultWindow(Screen):
    pass
class CreateWindow(Screen):
    def Create_Account(self,loginText, passwordText):
        layout = GridLayout(cols = 1)
        #popupLabel = Label(text = "Incorrect Login Information") 
        closeButton = Button(text = "Close") 
  
        #layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)

        popup = Popup(title ='Fields cannot be Blank', 
                      content = layout,
                      size_hint=(None, None), size=(500,200))   
        test = CreateWindow()
        app = App.get_running_app()
        app.username = loginText
        app.password = passwordText
        if app.username!='' and app.password!='':
            salt = os.urandom(32)
            password = test.hash_password(app.password)
            sql = """INSERT INTO LOGIN321 (User, Pass) VALUES('%s','%s')"""%(app.username, password)
            cursor.execute(sql)
            conn.commit()
        else:
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)



    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000, dklen=45)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
        #cursor.execute('INSERT INTO LOGIN321 (User, Pass) VALUES('%s')'
class MapWindow(Screen):
    def set_marker_position(self,x):
        
        map = MapView(zoom=11, lat=41.605, lon=-93.655, double_tap_zoom = True)
        marker_1 = MapMarker(lon=-93.655, lat=41.605)
        map.add_marker(marker_1)

class WindowManager(ScreenManager):
    pass

class PopUpWindow(Screen):
    def set_marker_position(self,x):
        
        map = MapView(zoom=11, lat=41.605, lon=-93.655, double_tap_zoom = True)
        marker_1 = MapMarker(lat=41.605, lon=-93.655)
        map.add_marker(marker_1)
        #return map



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
