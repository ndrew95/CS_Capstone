from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.utils import platform
if platform == "ios":
    from os.path import join, dirname
    import kivy.garden
    kivy.garden.garden_app_dir = join(dirname(__file__), "libs", "garden")
from kivy.garden.mapview import MapMarkerPopup
from kivy.uix.bubble import Bubble
from kivy.garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from  kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
from datetime import timedelta
from datetime import date
import time
import pymysql
import pymysql.cursors
import hashlib, binascii, os


host='cap-comp.cpwue0appyn7.us-west-2.rds.amazonaws.com'
port=3306
dbname= 'Companion'
user="admin234"
password="tf7A8sjX#!"


conn = pymysql.connect(db=dbname,host=host, password=password, port=port, user=user)
cursor = conn.cursor()


class MainWindow(Screen):
    
    def do_login(self, loginText, passwordText):

        app = App.get_running_app()
        mainWindow = MainWindow()

        global login123
        login123 =loginText
        checkUser = False

        layout = GridLayout(cols = 1)
        closeButton = Button(text = "Close") 
        layout.add_widget(closeButton)
        popup = Popup(title ='Incorrect Login Information', content = layout, size_hint=(None, None), size=(500,200))  

        cursor.execute('SELECT User, Pass from LOGIN321')
        logins = cursor.fetchall()

        app.username = loginText
        app.password = passwordText
    

        for i in logins:
            if(mainWindow.verify_password(i[1], app.password)==True and i[0]==app.username):
                checkUser = True
                break
           
        if checkUser == True:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'second'

        else:
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)


    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000, dklen=45)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == stored_password

class SecondWindow(Screen):
    
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
            
    def get_next_event(self):

        cursor.execute('SELECT Description, Time, EventID from EVENTS order by time')
        next_event = cursor.fetchall()

        return(next_event)

    def time_to_event(self):

        secondWindow = SecondWindow()

        events = secondWindow.get_next_event()
        dateNow = datetime.now().time()

        dummyDate = date(1, 1, 1)
        dateTimeCurrent = datetime.combine(dummyDate, dateNow)
       
        firstList = []
        secondList = []

        count = 0 
        for event in events:

            eventStartTime = datetime.strptime(str(event[1]), '%H:%M:%S')
            eventStopTime = datetime.time(eventStartTime)

            eventTime = datetime.combine(dummyDate, eventStopTime)

            timeUntilEvent = eventTime - dateTimeCurrent

            if "day" in str(timeUntilEvent):
                                                                        
                daySplit = str(timeUntilEvent).split('day, ')
                firstList.append(str(daySplit[1]))
      
            else:
            
                firstList.append(str(timeUntilEvent))
                
                secondList.append(event[0])
                count = count + 1

      
        finalList = [None] * len(firstList)
        count = 0

        for listItem in firstList:
            timeSplit=listItem.split(":")
            finalList[count] =(int(f"{timeSplit[0]}{timeSplit[1]}"))
            count = count +1
        
        l = sorted(enumerate(finalList), key=lambda i: i[1])
        
        return(events[l[0][0]][0], events[l[1][0]][0], events[l[2][0]][0], events[l[len(l)-1][0]][2], events[l[len(l)-2][0]][2], events[l[len(l)-3][0]][2], events[l[0][0]][1],events[l[1][0]][1], events[l[2][0]][1])
        
    def update_results(self,x):
        
        secondWindow = SecondWindow()
        secondWindow.time_to_event()

        result1 = self.ids.result1
        result2 = self.ids.result2
        result3 = self.ids.result3

        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[3])
        cursor.execute(query)
        next_result1 = cursor.fetchone()
        
        
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[4])
        cursor.execute(query)
        next_result2 = cursor.fetchone()


        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[5])
        cursor.execute(query)
        next_result3 = cursor.fetchone()
        
        
        result1.text = str(next_result1[0]) + " Winner:  " + str(next_result1[1]) + " " + str(next_result1[2] + " of " + str(next_result1[4]))
        result2.text = str(next_result2[0]) + " Winner:  " + str(next_result2[1]) + " " + str(next_result2[2] + " of " + str(next_result2[4]))
        result3.text = str(next_result3[0]) + " Winner:  " + str(next_result3[1]) + " " + str(next_result3[2] + " of " + str(next_result3[4]))

    def update_events(self,x):
        
        secondWindow = SecondWindow()
        secondWindow.time_to_event()

        event1 = self.ids.event1
        event2 = self.ids.event2
        event3 = self.ids.event3

        time1 = self.ids.time1
        time2 = self.ids.time2
        time3 = self.ids.time3
        
        event1.text = secondWindow.time_to_event()[0]
        event2.text = secondWindow.time_to_event()[1]
        event3.text = secondWindow.time_to_event()[2]

        time1.text = str(secondWindow.time_to_event()[6])
        time2.text = str(secondWindow.time_to_event()[7])
        time3.text = str(secondWindow.time_to_event()[8])

        
    def reset_checkbox(self):

        secondWindow = SecondWindow()
        mainWindow = MainWindow()

        check1 = self.ids.check1
        check2 = self.ids.check2
        check3 = self.ids.check3
        
        layout = GridLayout(cols = 1)
        closeButton = Button(text = "Close")  
        layout.add_widget(closeButton)
        popup = Popup(title ='Already Submitted Interest for this Event', content = layout, size_hint=(None, None), size=(500,200)) 

        interest1 = False
        interest2 = False
        interest3 = False
       
        sql = "SELECT User, Event FROM DUPLICATE"
        cursor.execute(sql)
        duplicate = cursor.fetchall()

        
        for users in duplicate:
            if users[0] == login123 and users[1] == secondWindow.time_to_event()[0]:
                interest1=True 
            elif users[0] == login123 and users[1] == secondWindow.time_to_event()[1]:
                interest2=True
            elif users[0] == login123 and users[1] == secondWindow.time_to_event()[2]:
                interest3=True
        
        
        if(check1.active==True and interest1==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(secondWindow.time_to_event()[0], secondWindow.time_to_event()[6])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, secondWindow.time_to_event()[0])
            cursor.execute(sql)

            conn.commit()

        elif(check1.active==True and interest1==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)
        
        if(check2.active==True and interest2==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(secondWindow.time_to_event()[1], secondWindow.time_to_event()[7])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, secondWindow.time_to_event()[1])
            cursor.execute(sql)

            conn.commit()

        elif(check2.active==True and interest2==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)

        if(check3.active==True and interest3==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(secondWindow.time_to_event()[2], secondWindow.time_to_event()[8])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, secondWindow.time_to_event()[2])
            cursor.execute(sql)

            conn.commit()

        elif(check3.active==True and interest3==True):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)

        for child in reversed(self.ids.two.children):
            if isinstance(child, CheckBox):
                child.active = False

    def update_interest(self,x): 

        secondWindow = SecondWindow()
        sql = "SELECT Description, Time, COUNT(*) occurences FROM INTEREST GROUP BY Description HAVING COUNT(*)>1 ORDER BY occurences DESC "
        cursor.execute(sql)
        interest = cursor.fetchall()
        dateNow = datetime.now().time()
        

        timeSplit=str(dateNow).split(":")
        timeNow =(int(f"{timeSplit[0]}{timeSplit[1]}"))

        timeSplit=str(interest[0][1]).split(":")
        interest1Time =(int(f"{timeSplit[0]}{timeSplit[1]}"))

        timeSplit=str(interest[1][1]).split(":")
        interest2Time =(int(f"{timeSplit[0]}{timeSplit[1]}"))

        timeSplit=str(interest[2][1]).split(":")
        interest3Time =(int(f"{timeSplit[0]}{timeSplit[1]}"))

        
        interest1 = self.ids.interest1
        interest2 = self.ids.interest2
        interest3 = self.ids.interest3

        time1=False
        time2=False
        time3=False

        for events in interest:
            timeSplit=str(events[1]).split(":")
            interestTime =(int(f"{timeSplit[0]}{timeSplit[1]}"))

            if(timeNow<=interestTime and time1==False):
                interest1.text = str(events[0]) + " taking place at " + str(events[1])
                time1=True
            elif(timeNow<=interestTime and time2==False):
                interest2.text = str(events[0]) + " taking place at " + str(events[1])
                time2=True
            elif(timeNow<=interestTime and time3==False):
                interest3.text = str(events[0]) + " taking place at " + str(events[1])
                time3=True



class DefaultWindow(Screen):
    pass
    
class CreateWindow(Screen):

    def create_account(self,loginText, passwordText):

        createWindow = CreateWindow()
        app = App.get_running_app()
        app.username = loginText
        duplicateUser = False

        app.password = passwordText
        cursor.execute('SELECT User, Pass from LOGIN321')
        logins = cursor.fetchall()

        layout = GridLayout(cols = 1)
        layout2 = GridLayout(cols = 1)
        layout3 = GridLayout(cols = 1)

        closeButton = Button(text = "Close") 
        closeButton2 = Button(text = "Close")
        closeButton3 = Button(text = "Close")

        layout.add_widget(closeButton)
        layout2.add_widget(closeButton2)
        layout3.add_widget(closeButton3)

        popup = Popup(title ='Fields cannot be Blank', content = layout, size_hint=(None, None), size=(500,200)) 
        popup2 = Popup(title ='This Username Already Exists', content = layout2, size_hint=(None, None), size=(500,200))
        popup3 = Popup(title ='Account Successfully Created', content = layout3, size_hint=(None, None), size=(500,200))    

        for users in logins:
            if users[0]==app.username:
                duplicateUser=True
        
        if app.username!='' and app.password!='' and duplicateUser==False:
            salt = os.urandom(32)
            password = createWindow.hash_password(app.password)

            sql = """INSERT INTO LOGIN321 (User, Pass) VALUES('%s','%s')"""%(app.username, password)
            cursor.execute(sql)
            conn.commit()

            popup3.open()
            closeButton3.bind(on_press=popup3.dismiss)

        if duplicateUser==True:
            popup2.open()
            closeButton2.bind(on_press = popup2.dismiss)
            
        if (app.username=='' and app.password=='') or (app.username=='') or (app.password==''):
            popup.open() 
            closeButton.bind(on_press = popup.dismiss)

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000, dklen=45)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
        
class MapWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
