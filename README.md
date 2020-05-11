# Drake CS Capstone Team I
Drake Relays Companion Application

The Drake Relays Companion Application is one that aids spectators of the Drake Relays. It ensures that people will not miss upcoming events, that they can see the most recent results, and alerts users to what upcoming events have a lot of people interested in them.

To Run:

First, Kivy will need to be installed in the computer running the application (assuming the computer has Python installed).


  Windows: 
  
           Create a virtual env: 
           
                    python -m virtualenv kivy_venv
                    
           Activate the virtual env when opening CMD: 
           
                    kivy_venv\Scripts\activate
                    
           Install the dependencies:
           
                    python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
                    
                    python -m pip install kivy_deps.gstreamer==0.1.*
                    
           Install Kivy:
           
                    python -m pip install kivy==1.11.1

  Mac OS:
  
          Install Kivy:
          
                    python -m pip install kivy

  Linux:
  
          Install Kivy:
          
                    python -m pip install kivy
                    
          Optionally, create a virtual env:
          
                    python -m virtualenv ~/kivy_venv
                    
                    source ~/kivy_venv/bin/activate

Secondly, PyMySql will need to be installed

          pip Install pymysql 
                  
  Additionally, Garden may or may not need to be installed. Garden also may or may not need to be upgraded--this depends on     the computer used.

Running DRCA:

      Download the GitHub repository, find your way to the directory through CMD, Bash, or Terminal, 
      and type "python DRCA.py"
  
  
  In the Application:

      If you are a new user, you will be required to sign up via the "Sign Up" button. The new window 
      that appears will prompt you to enter a username and password. Passwords are encrypted 
      so the administrator of the database cannot see passwords.
  
  


                  
