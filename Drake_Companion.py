from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
import os

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
  
    event_update = StringProperty()
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        #this self.event_update having the value of 'new event' is for purposes of showing the utility of the
        #refresh button
        self.event_update = str('new event')
    
    #self.event_update = str('new event')

    def update_events(self):
        
        '''
        here we can have the number of events we want to display and dynamically change the events name
        when the app boots up, so it would also be useful to have a refresh button. The next goal for this would
        be to have the event name update by hooking up to the database, and not have to be entered manually
        via code
        '''
        test = SecondWindow()
        
        events = self.ids.event1
        events2 = self.ids.event2
        
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
        events.text = 'test'
        events2.text = 'test2'
            
            
        
    
class CreateWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass




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
