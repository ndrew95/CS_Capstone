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

'''Connecting to the database so various features can be used'''
host='cap-comp.cpwue0appyn7.us-west-2.rds.amazonaws.com'
port=3306
dbname= 'Companion'
user="admin234"
password="tf7A8sjX#!"

conn = pymysql.connect(db=dbname,host=host, password=password, port=port, user=user)
cursor = conn.cursor()

class MainWindow(Screen):
    
    def do_login(self, loginText, passwordText):
        '''
        the do_login feature allows users to sign in as long as their information is correct. As passwords are encrypted via hashing,
        the verify_password function hashes the password that is typed in, and do_login checks the password typed-in, now hashed, against
        the databases passwords. If the password is connected with a username, a user can login
        '''

        app = App.get_running_app()
        mainWindow = MainWindow()

        global login123
        login123 =loginText

        app.username = loginText
        app.password = passwordText

        checkUser = False

        layout = GridLayout(cols = 1)
        closeButton = Button(text = "Close") 
        layout.add_widget(closeButton)
        incorrectPopup = Popup(title ='Incorrect Login Information', content = layout, size_hint=(None, None), size=(500,200))  


        userQuery = """SELECT User, Pass from LOGIN321 WHERE User='%s'"""%(app.username)
        cursor.execute(userQuery)
        logins = cursor.fetchone()
        
    
        #checking if a user exists with the username and password#
        if logins!= None:
            if(mainWindow.verify_password(logins[1], app.password)==True):
                checkUser = True

        #if the username and password combo exist, then access is granted#
        if checkUser == True:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'second'

        else:
            incorrectPopup.open() 
            closeButton.bind(on_press = incorrectPopup.dismiss)


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

        #querying the database to get all upcoming events (this function is used later by time_to_event)#
        cursor.execute('SELECT Description, Time, EventID from EVENTS order by time')
        next_event = cursor.fetchall()

        return(next_event)

    def time_to_event(self):
        '''
        the time_to_event function gets the event list from the get_next_event function. time_to_event then runs a loop to determine which
        events are upcoming, and which events just recently ended. This function returns the events that are closest to the time currently,
        as well as the events that most recently ended. These returned variables are then utilized to populate the results tab and the events tab
        '''

        secondWindow = SecondWindow()
        events = secondWindow.get_next_event()

        timeNow = datetime.now().time()

        dummyDate = date(1, 1, 1)
        dateTimeCurrent = datetime.combine(dummyDate, timeNow)
       
        firstList = []

        count = 0 
        for event in events:

            eventDateTime = datetime.strptime(str(event[1]), '%H:%M:%S')
            eventStartTime = datetime.time(eventDateTime)

            eventTime = datetime.combine(dummyDate, eventStartTime)

            #the difference of time between the current time and the time to the event#
            timeUntilEvent = eventTime - dateTimeCurrent

            if "day" in str(timeUntilEvent):                                                     
                daySplit = str(timeUntilEvent).split('day, ')
                firstList.append(str(daySplit[1]))
      
            else:
                firstList.append(str(timeUntilEvent))
                count = count + 1

      
        finalList = [None] * len(firstList)
        count = 0

        #splitting the time so it can be properly sorted#
        for listItem in firstList:
            timeSplit=listItem.split(":")
            finalList[count] =(int(f"{timeSplit[0]}{timeSplit[1]}"))
            count = count +1
        
        #obtaining the original index from the list to ensure that the correct event is obtained from the database#
        l = sorted(enumerate(finalList), key=lambda i: i[1])
        
        #return items 0-2 are the event descriptions of closest upcoming events, return items 3-5 are the eventID's of the events that just ended,#
        #return items 6-8 are the event times that are closest to the current time#
        return(events[l[0][0]][0], events[l[1][0]][0], events[l[2][0]][0], events[l[len(l)-1][0]][2], events[l[len(l)-2][0]][2], events[l[len(l)-3][0]][2], events[l[0][0]][1],events[l[1][0]][1], events[l[2][0]][1])
        
    def update_results(self,x):
        '''
        the update_results function utilizes the time_to_event function to obtain return items 3-5. These items are the eventID's of events
        that most recently ended. 3 queries are then run against those eventID's so users can see what the results are for events that
        most recently ended.
        '''
        
        secondWindow = SecondWindow()

        result1 = self.ids.result1
        result2 = self.ids.result2
        result3 = self.ids.result3

        #these  queries find the events, athlete, and results of the most recently ended events#
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[3])
        cursor.execute(query)
        next_result1 = cursor.fetchone()
        
        
        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[4])
        cursor.execute(query)
        next_result2 = cursor.fetchone()


        query = """SELECT EVENTS.Description, ATHLETE.FirstName, ATHLETE.LastName, RESULTS.AthleteRank, SCHOOL.SchoolName from RESULTS, ATHLETE, EVENTS, SCHOOL WHERE RESULTS.EventID = '%s' AND RESULTS.AthleteID = ATHLETE.AthleteID AND RESULTS.EventID = EVENTS.EventID AND ATHLETE.SchoolID = SCHOOL.SchoolID""" %(secondWindow.time_to_event()[5])
        cursor.execute(query)
        next_result3 = cursor.fetchone()
        
        #"injecting" the query results into the result labels#
        result1.text = str(next_result1[0]) + " Winner:  " + str(next_result1[1]) + " " + str(next_result1[2] + " of " + str(next_result1[4]))
        result2.text = str(next_result2[0]) + " Winner:  " + str(next_result2[1]) + " " + str(next_result2[2] + " of " + str(next_result2[4]))
        result3.text = str(next_result3[0]) + " Winner:  " + str(next_result3[1]) + " " + str(next_result3[2] + " of " + str(next_result3[4]))

    def update_events(self,x):
        '''
        Update events utilizes time_to_event to display events that are closest to the current time
        '''

        secondWindow = SecondWindow()

        event1 = self.ids.event1
        event2 = self.ids.event2
        event3 = self.ids.event3

        time1 = self.ids.time1
        time2 = self.ids.time2
        time3 = self.ids.time3
        
        #"Injecting" the event description into the events labels#
        event1.text = secondWindow.time_to_event()[0]
        event2.text = secondWindow.time_to_event()[1]
        event3.text = secondWindow.time_to_event()[2]

        #"Injecting" the times into the time labels#
        time1.text = str(secondWindow.time_to_event()[6])
        time2.text = str(secondWindow.time_to_event()[7])
        time3.text = str(secondWindow.time_to_event()[8])

        
    def reset_checkbox(self):

        '''
        reset_checkbox resets the checkboxes when the submit interest button is pressed. Furthermore, reset_checkbox also
        sends an insert query to the "Interest" table of the database so that interest can be calculated in various events.
        there is also a "safety-check" to ensure that the same user cannot submit interest for the same event multiple times.
        '''

        secondWindow = SecondWindow()
        firstEvent = secondWindow.time_to_event()[0]
        secondEvent = secondWindow.time_to_event()[1]
        thirdEvent = secondWindow.time_to_event()[2]

        #obtaining the checkboxes by their id#
        check1 = self.ids.check1
        check2 = self.ids.check2
        check3 = self.ids.check3
        
        layout = GridLayout(cols = 1)
        closeButton = Button(text = "Close")  
        layout.add_widget(closeButton)
        alreadyPopup = Popup(title ='Already Submitted Interest for this Event', content = layout, size_hint=(None, None), size=(500,200)) 

        #setting the interest to false at the start#
        interest1 = False
        interest2 = False
        interest3 = False
       
        #querying the "DUPLICATE" table#
        sql = """SELECT User, Event FROM DUPLICATE WHERE User = '%s'"""%(login123)
        cursor.execute(sql)
        duplicate = cursor.fetchall()


        #if a user has already submitted interest in an event, the interest is set to true, depending on which#
        #event they showed interest in#
        if duplicate!=None:
            for users in duplicate:
                if users[1] == firstEvent:
                    interest1=True 
                elif users[1] == secondEvent:
                    interest2=True
                elif users[1] == thirdEvent:
                    interest3=True
        
        #if the checkboxes are active, and a user has not already submitted interest, the event that someone indicated interest for#
        #is inserted into the INTEREST table of the database.#
        if(check1.active==True and interest1==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(firstEvent, secondWindow.time_to_event()[6])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, firstEvent)
            cursor.execute(sql)

            conn.commit()

        #if the interest is true, meaning that the user already submitted interest, display a popup indicating that they already submitted
        #their interest, and do not insert anything into the INTEREST table#
        elif(check1.active==True and interest1==True):
            alreadyPopup.open() 
            closeButton.bind(on_press = alreadyPopup.dismiss)
        
        if(check2.active==True and interest2==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(secondEvent, secondWindow.time_to_event()[7])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, secondEvent)
            cursor.execute(sql)

            conn.commit()

        elif(check2.active==True and interest2==True):
            alreadyPopup.open() 
            closeButton.bind(on_press = alreadyPopup.dismiss)

        if(check3.active==True and interest3==False):
            sql = """INSERT INTO INTEREST (Description, Time) VALUES('%s', '%s')"""%(thirdEvent, secondWindow.time_to_event()[8])
            cursor.execute(sql)

            sql = """INSERT INTO DUPLICATE (User, Event) VALUES('%s', '%s')"""%(login123, thirdEvent)
            cursor.execute(sql)

            conn.commit()

        elif(check3.active==True and interest3==True):
            alreadyPopup.open() 
            closeButton.bind(on_press = alreadyPopup.dismiss)

        #resetting the checkboxes
        for child in reversed(self.ids.two.children):
            if isinstance(child, CheckBox):
                child.active = False

    def update_interest(self,x): 
        '''
        the update_interest function updates the interest tab to show events that are upcoming, yet have a lot of interest
        '''
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

        #populating the results page that only shows upcoming events, not events that already happened. This for loop also
        #ensures that labels won't bee populated more than once.
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
            if(time1==True and time2==True and time3==True):
                break



class DefaultWindow(Screen):
    pass
    
class CreateWindow(Screen):

    def create_account(self,loginText, passwordText):
        '''
        the create_account functions allows users to create an account. Passwords are encrypted to ensure that the database administrator
        cannot see real passwords. There are a few "safety-checks." One ensures that the fields are not blank, another ensures that the 
        username is not taken, and one ensures that the account was created successfully. If the fields are blank, a popup will indicate
        that they cannot be blank. If the user exists, it will alert the user that it already exists. If the account is created successfully
        it will also alert the user.
        '''
        createWindow = CreateWindow()
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        duplicateUser = False

        layout = GridLayout(cols = 1)
        layout2 = GridLayout(cols = 1)
        layout3 = GridLayout(cols = 1)

        closeButton = Button(text = "Close") 
        closeButton2 = Button(text = "Close")
        closeButton3 = Button(text = "Close")

        layout.add_widget(closeButton)
        layout2.add_widget(closeButton2)
        layout3.add_widget(closeButton3)

        blankPopup = Popup(title ='Fields cannot be Blank', content = layout, size_hint=(None, None), size=(500,200)) 
        existsPopup = Popup(title ='This Username Already Exists', content = layout2, size_hint=(None, None), size=(500,200))
        createdPopup = Popup(title ='Account Successfully Created', content = layout3, size_hint=(None, None), size=(500,200))  


        query = """SELECT User, Pass from LOGIN321 WHERE User = '%s'"""%(app.username)
        cursor.execute(query)
        logins = cursor.fetchall()

        #checking if the username exists
        if logins:
            duplicateUser=True
        
        #checking that the fields arent blank and that the username doesnt exist. If these are both true,#
        #the password is encrypted, and the login information is sent to the database#
        if app.username!='' and app.password!='' and duplicateUser==False:
           
            password = createWindow.hash_password(app.password)

            sql = """INSERT INTO LOGIN321 (User, Pass) VALUES('%s','%s')"""%(app.username, password)
            cursor.execute(sql)
            conn.commit()

            createdPopup.open()
            closeButton3.bind(on_press=createdPopup.dismiss)

        if duplicateUser==True:
            existsPopup.open()
            closeButton2.bind(on_press = existsPopup.dismiss)
            
        if (app.username=='' and app.password=='') or (app.username=='') or (app.password==''):
            blankPopup.open() 
            closeButton.bind(on_press = blankPopup.dismiss)

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
