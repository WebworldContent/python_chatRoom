import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import socket_client
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import sys
import os
from kivy.uix.image import Image
# from kivy.graphics import Rectange , Color
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
import json



user_list = []


class ConnectPage(GridLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2 
        self.spacing = 10


        with self.canvas: 

            # Color(.234, .456, .678, .9)  # set the colour  

            # Seting the size and position of canvas 
            self.rect = Rectangle(source = 'front.png', pos = self.center, 
                                    size =self.size) 
    
            # Update the canvas as the screen size change 
            self.bind(pos = self.update_rect, 
                    size = self.update_rect) 
        
        

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt","r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
        else:
            prev_ip =""
            prev_port = ""
            prev_username = ""

        self.add_widget(Label(text='IP:', font_size = '30sp' ))  # widget #1, top left
        self.ip = TextInput(text=prev_ip, multiline=False)  # defining self.ip...
        self.add_widget(self.ip) # widget #2, top right

        self.add_widget(Label(text='Port:' ,font_size = '30sp'))
    
        self.port = TextInput(text=prev_port, multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text='  Username:' , font_size = '30sp'))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        # add our button.
        self.join = Button(text="Join >>",background_color= (0,255,0,0.5))
        self.join.bind(on_press=self.join_button)
        self.add_widget(Label())  # just take up the spot.
        self.add_widget(self.join)

    def update_rect(self, *args): 
            self.rect.pos = self.pos 
            self.rect.size = self.size 

    def join_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text
        with open("prev_details.txt","w") as f:
            f.write(f"{ip},{port},{username}")
        info = f" C O N N E C T I N G...  \n \n {ip} : {port} as {username} "
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Info'
        Clock.schedule_once(self.connect, 3)

    
    def connect(self, _):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not socket_client.connect(ip, port, username, show_error):
            return

        user_list.append(username)
        chat_app.create_chat_page()
        chat_app.screen_manager.current = 'Chat'




class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()
        
    

       
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    
    def update_chat_history_send(self, message):
        
        self.chat_history.text += '\n' + message
        self.chat_history.halign = 'left'
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        # self.chat_history.halign = 'right'
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        self.scroll_to(self.scroll_to_point)
    
    def update_chat_history_rcv(self, message):
        
        self.chat_history.text += '\n' + message
        self.chat_history.halign = 'right'
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        # self.chat_history.halign = 'right'
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

       

    def update_chat_history_layout_recv(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

class Stack:
    def __init__(self):
        self.stk = []
    
    def push(self,data):
        self.stk.append(data)
    
    def pop(self):
        self.stk.pop()


class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=self.pos, size=self.size)



    

class ChatPage(GridLayout):

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         
        
        # self.user_list = ['join']
        # Window.color = (0,3,0,1)
    
        with self.canvas: 

            # Color(.234, .456, .678, .9)  # set the colour  

            # Seting the size and position of canvas 
            self.rect = Rectangle(source = 'back2.jpg', pos = self.center, 
                                    size =self.size) 

            # Update the canvas as the screen size change 
            self.bind(pos = self.update_rect, 
                    size = self.update_rect) 

        
        self.cols = 1
        self.rows = 2
        
        # self.side_but = Button(text='cool')
        self.history = ScrollableLabel(height=Window.size[1]*0.9, size_hint_y=None)
        self.history_recv = ScrollableLabel(height=Window.size[1]*0.9, size_hint_y=None)
        # self.add_widget(self.side_but)
        side_bar = GridLayout(cols = 3)
        self.box = BoxLayout(orientation='vertical')
        self.box.size_hint_x = .4

        # user_list = self.set_arr()
        # if len(user_list) > 0:
        # stack = Stack()

        # for i in stack.stk:
        self.side_label = MyLabel(
            text=  'Joined', 
            pos=(20, 20),
            size_hint=(1, 0.5))
        
        self.side_label.text =  user_list[0].upper() 
        self.side_label.text =  self.side_label.text 
        self.side_label.font_size ='25sp'
        self.side_label.color = [0.41, 0.42, 0.74, 1]
        # self.side_label.text_size = (6,4)
        self.box.add_widget(self.side_label)
        # else:
        #     label = MyLabel(
        #             text="Joined Users",
        #             pos=(20, 20),
        #             size_hint=(1, 0.5))
                
        #     box.add_widget(label)

        
        # with label.canvas:
        #     Color(0, 1, 0, 0.25)
        #     Rectangle(pos=label.pos, size=label.size)
        

        side_bar.add_widget(self.box)
        side_bar.add_widget(self.history)
        side_bar.add_widget(self.history_recv)
        self.add_widget(side_bar)   #########################################
      

        self.new_message = TextInput(width=Window.size[0]*0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send",background_color= (0,0,255,0.8))
        # self.send.halign = 'right'
        # self.send.size = 80,50
        # self.send.size_hint = None,None
        self.send.bind(on_press=self.send_message)

        bottom_line = GridLayout(cols=2 , row_force_default=True, row_default_height=40)
        bottom_line.size_hint_y = .07
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)

        # bottom_line = FloatLayout()
        # bottom

        self.add_widget(bottom_line)    ############################################

        Window.bind(on_key_down=self.on_key_down)

        Clock.schedule_once(self.focus_text_input, 1)
        socket_client.start_listening(self.incoming_message, show_error)
        self.bind(size=self.adjust_fields)

    def update_rect(self, *args): 
        self.rect.pos = self.pos 
        self.rect.size = self.size 

    def adjust_fields(self,*_):
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height
        self.history_recv.height  = new_height

        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        Clock.schedule_once(self.history.update_chat_history_layout,0.01)
        Clock.schedule_once(self.history_recv.update_chat_history_layout_recv,0.01)


  
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):

        if keycode == 40:
            self.send_message(None)


    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ''
        if message:
            username = chat_app.connect_page.username.text
            user = username.replace(username[0],username[0].upper(),1)
            self.history.update_chat_history_send(f'[color=dd2020][b][size=18]{user}[/size][/b][/color] >> [color=09020f][font_family=Arial]{message}[/font_family][/color]')
            socket_client.send(message)
        
        

        Clock.schedule_once(self.focus_text_input, 0.1)


    
    def focus_text_input(self, _):
        self.new_message.focus = True

  
    def incoming_message(self, username, message,arr):

        stack = Stack()
        for i in arr:
            stack.push(i)
        
        user = username.replace(username[0],username[0].upper(),1)
        self.history_recv.update_chat_history_rcv(f'[color=09020f][font_family=Arial]{message}[/font_family][/color]  <<  [color=7f20dd][b][size=18]{user}[/size][/b][/color]')

        
        

class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas: 
  
            # Color(.234, .456, .678, .9)  # set the colour  
  
            # Seting the size and position of canvas 
            self.rect = Rectangle(source ='back.jpg',pos = self.pos, 
                                  size =self.size)

            self.bind(pos = self.update_rect, 
                  size = self.update_rect) 
            
        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=25)
        self.message.bind(width=self.update_text_width)
        
        self.add_widget(self.message)

    def update_rect(self, *args): 
        self.rect.pos = self.pos 
        self.rect.size = self.size

        
        

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)


class Chat_ArenaApp(App):
    Window.size = (700,600)
    
    def build(self):

        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.info_page = InfoPage()
        screen = Screen(name='Info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name='Chat')
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)


def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = 'Info'
    Clock.schedule_once(sys.exit, 10)

if __name__ == "__main__":
    chat_app = Chat_ArenaApp()
    chat_app.run()