#Fixation V2.5
#automated sequence stop automatically after 0.5 seconds before the hrt is done with the sequence

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import time

from automated_list import automated_list
import foot_switch

class MyApp():
    def __init__(self, root):

        #import setting default
        with open('default.txt', "r") as file:
            lines = file.readlines()
            self.settings = {}
            for line in lines:
                key, value = line.strip().split("=")
                try:
                    self.settings[key] = int(value)
                except:
                    try:
                        self.settings[key] = float(value)
                    except:
                        self.settings[key] = str(value)

        #set root
        width = 650
        height = 380
        self.root = root
        self.root.geometry(f"{width}x{height}")
        self.root.title("Fixation for HRT III - V2.5")
        self.root.resizable(False, False)

        self.root.bind('<Return>', self.start_event)
        self.root.bind('<KP_Enter>', self.start_event)

        self.screen_width = 0
        self.screen_height = 0

        def center_window(root, width=310, height=250):
            # Bildschirmbreite und -höhe abrufen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            # Die x- und y-Koordinaten berechnen
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            # Setze Mindestgröße, damit Fenster nicht zu klein werden kann.
            root.minsize(width, height)
            # Hier könnte man ebenfalls die maximale Größe setzen
            # root.maxsize(max_width, max_height)
            root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            self.screen_width = screen_width
            self.screen_height = screen_height
        center_window(self.root, width, height)

        #Some parameters
        #starting colour of the points
        self.colour = 'yellow'
        #Create list for movement
        self.config_list = []
        #variable to know if config mode was used or not
        self.config_bool = False
        #name of default pattern file
        self.filename = self.settings['pattern_file']
        self.short_name = os.path.basename(self.filename)

        #Eye
        self.eye_input = tk.IntVar(value=self.settings['fixation_eye'])                              #default 2
        eye_label = tk.Label(self.root, text="Fixation eye: ")
        eye_label.grid(row=0 , column=0, sticky=tk.E)
        E1 = tk.Radiobutton(self.root, text="OS", variable=self.eye_input, value=1)
        E1.grid(row=0, column=1, sticky=tk.W)
        E2 = tk.Radiobutton(self.root, text="OD", variable=self.eye_input, value=2)
        E2.grid(row=0, column=2, sticky=tk.W)

        #Points distance in the rectangle
        dist_label = tk.Label(self.root, text="Distance between points [mm]:")
        dist_label.grid(row=1, column=0, sticky=tk.E)
        self.dist = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.dist.insert(0, self.settings['distance_between_points'])                                #default 4
        self.dist.grid(row=1, column=1)
        #distance between points on the whorl region
        distw_label = tk.Label(self.root, text="and in the whorl region:")
        distw_label.grid(row=1, column=2, sticky=tk.E)
        self.distw = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.distw.insert(0, self.settings['distance_between_points_whorl'])                         #default 4
        self.distw.grid(row=1, column=3)

        #Size of points
        dist_label = tk.Label(self.root, text="Size of dot [pixel]:")
        dist_label.grid(row=2, column=0, sticky=tk.E)
        self.diam = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.diam.insert(0, self.settings['dot_size'])                                               #default 3
        self.diam.grid(row=2, column=1)

        #define monitor direction
        self.monitor = tk.IntVar(value=self.settings['monitor_direction'])                           #default 3
        monitor_label = tk.Label(self.root, text="Monitor direction: ")
        monitor_label.grid(row=3, column=0, sticky=tk.E)
        R1 = tk.Radiobutton(self.root, text="hor", variable=self.monitor, value=1)
        R1.grid(row=3, column=1, sticky=tk.W)
        R2 = tk.Radiobutton(self.root, text="vert_clock", variable=self.monitor, value=2)
        R2.grid(row=3, column=2, sticky=tk.W)
        R3 = tk.Radiobutton(self.root, text="vert_counter", variable=self.monitor, value=3)
        R3.grid(row=3, column=3, sticky=tk.W)

        #define movement direction
        self.movement = tk.IntVar(value=self.settings['movement_direction'])                         #default 2
        movement_label = tk.Label(self.root, text="Movement direction: ")
        movement_label.grid(row=5, column=0, sticky=tk.E)
        R4 = tk.Radiobutton(self.root, text="fixation", variable=self.movement, value=1)
        R4.grid(row=5, column=1, sticky=tk.W)
        R5 = tk.Radiobutton(self.root, text="plexus", variable=self.movement, value=2)
        R5.grid(row=5, column=2, sticky=tk.W)

        #define screen dimensions
        dim_w_label = tk.Label(self.root, text="Screen dimensions: width[mm]")
        dim_w_label.grid(row=6, column=0, sticky=tk.E)
        self.dim_w = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.dim_w.insert(0, self.settings['screen_width'])                                          #default 155
        self.dim_w.grid(row=6, column=1)
        dim_h_label = tk.Label(self.root, text="height[mm]")
        dim_h_label.grid(row=6, column=2, sticky=tk.E)
        self.dim_h = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.dim_h.insert(0, self.settings['screen_height'])                                         #default 87
        self.dim_h.grid(row=6, column=3)

        #test section title
        section_label = tk.Label(self.root, text='SEQUENCE')
        section_label.grid(row=8, column=0)
        whorl_button = tk.Button(self.root, text="Config.", command=self.open_config_window)
        whorl_button.grid(row=8, column=1)
        open_button = tk.Button(self.root, text='Open', command=self.load_config)
        open_button.grid(row=8, column=2)
        if self.settings['pattern_check']:# and self.settings['pattern_file']:
            self.open_text = tk.StringVar(self.root, "loaded")
            self.load_config_list()
        else:
            self.open_text = tk.StringVar(self.root, "")
        open_label = tk.Label(self.root, textvariable=self.open_text)
        open_label.grid(row=8, column=3)

        #Dimensions of rectangle
        rect_w_label = tk.Label(self.root, text="Rectangle: width[images]")
        rect_w_label.grid(row=9, column=0, sticky=tk.E)
        self.rect_w = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.rect_w.insert(0, self.settings['rectangle_width'])                                      #default 8
        self.rect_w.grid(row=9, column=1)
        rect_h_label = tk.Label(self.root, text="height[images]")
        rect_h_label.grid(row=9, column=2, sticky=tk.E)
        self.rect_h = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.rect_h.insert(0, self.settings['rectangle_height'])                                     #default 8
        self.rect_h.grid(row=9, column=3)

        #distance between whorl and rectangle
        d_whorl_label = tk.Label(self.root, text="Distance between whorl and rectangle:")
        d_whorl_label.grid(row=10, column=0, sticky=tk.E)
        self.whorl = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.whorl.insert(0, self.settings['distance_between_whorl_and_rectangle'])                  #default 4
        self.whorl.grid(row=10, column=1)
        im_whorl_label = tk.Label(self.root, text="[images]")
        im_whorl_label.grid(row=10, column=2, sticky=tk.W)

        #how many steps nasal?
        nasal_label = tk.Label(self.root, text="Number of steps nasally (even):")
        nasal_label.grid(row=11, column=0, sticky=tk.E)
        self.steps_n = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.steps_n.insert(0, self.settings['number_of_steps_nasally'])                             #default 2
        self.steps_n.grid(row=11, column=1)
        nasal_im_label = tk.Label(self.root, text="[images]")
        nasal_im_label.grid(row=11, column=2, sticky=tk.W)

        #use Rostock plug in
        self.pedal_var = tk.IntVar(value=self.settings['foot_switch'])
        C1 = tk.Checkbutton(self.root, text = "virtual pedal", variable = self.pedal_var, onvalue = 1, offvalue = 0)
        C1.grid(row=10, column=3)

        #test Rostock-plugin
        vptest_button = tk.Button(self.root, text='Init. VP', command=self.test_port)
        vptest_button.grid(row=11, column=3)
        self.ser = None

        #Speed of movement
        speed_label = tk.Label(self.root, text='How many sec each point [s]:')
        speed_label.grid(row=12, column=0, sticky=tk.E)
        self.speed = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.speed.insert(0, self.settings['time_between_points'])                                   #default 0.2
        self.speed.grid(row=12, column=1)

        #Sequence configuration from IVCM
        ivcm_label = tk.Label(self.root, text='HRT-Rate: [imgs/s]')
        ivcm_label.grid(row=12, column=2, sticky=tk.E)
        self.ivcm_rate = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.ivcm_rate.insert(0, self.settings['ivcm_rate'])                                         #default 3
        self.ivcm_rate.grid(row=12, column=3)

        #Enable auto-motion
        self.switch = tk.IntVar(value=self.settings['mode'])                                         #default 2
        auto_switch_label = tk.Label(self.root, text="Mode: ")
        auto_switch_label.grid(row=13, column=0, sticky=tk.E)
        S1 = tk.Radiobutton(self.root, text="automated", variable=self.switch, value=1)
        S1.grid(row=13, column=1, sticky=tk.W)
        S2 = tk.Radiobutton(self.root, text="semi-automated", variable=self.switch, value=2)
        S2.grid(row=13, column=2, sticky=tk.W)
        S3 = tk.Radiobutton(self.root, text="manual", variable=self.switch, value=3)
        S3.grid(row=13, column=3, sticky=tk.W)

        #define starting point coordinates
        start_x_label = tk.Label(self.root, text="Starting point coordinates: x [0-1]")
        start_x_label.grid(row=14, column=0, sticky=tk.E)
        self.start_x = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.start_x.insert(0, self.settings['starting_point_x'])                                   #default 0.5
        self.start_x.grid(row=14, column=1)
        start_x_label = tk.Label(self.root, text="y [0-1]")
        start_x_label.grid(row=14, column=2, sticky=tk.E)
        self.start_y = tk.Entry(self.root, bd=2, width=8, justify="right")
        self.start_y.insert(0, self.settings['starting_point_y'])                                         #default 0.5
        self.start_y.grid(row=14, column=3)

        #Patient ID
        id_label = tk.Label(self.root, text='Patient ID: ')
        id_label.grid(row=15, column=0, sticky=tk.E)
        self.id = tk.Entry(self.root, bd=2, width=27)
        self.id.grid(row=15, column=1, columnspan=2, sticky=tk.E)

        #Start the application
        start_button = tk.Button(self.root, text="Start", command=self.start_event, activebackground="green")
        start_button.grid(row=17, column=1, columnspan=3)

        #Close application
        close_button = tk.Button(self.root, text="Close", activebackground="red", command=self.close_event)
        close_button.grid(row=17, column=0, columnspan=2)
    
    def test_port(self):
        try:
            self.ser = foot_switch.initialise_port()
            foot_switch.send_signal(self.ser)
        except:
            messagebox.showerror("Error", "No connection to virtual pedal.\nConnect device and try again.")

    def ratio(self) -> list:
        """Calculate ratio pixel/mm of display."""
        w_ratio = self.screen_width / int(self.dim_w.get())
        h_ratio = self.screen_height / int(self.dim_h.get())
        return [w_ratio, h_ratio]

    def check_inbound(self, coord):
        """Check if next point is inside screen."""
        return coord[0] - self.d > 0 and coord[0] + self.d < self.max_x and coord[1] - self.d > 0 and coord[1] + self.d < self.max_y
    
    def get_steps_available(self, coord):
        """Get how many steps are possible inside screen in each direction."""
        return {'x_left': coord[0] // self.step_x, 'x_right': (self.max_x - coord[0]) // self.step_x, 'y_up': coord[1] // self.step_y, 'y_down': (self.max_y - coord[1]) // self.step_y}

    def on_escape_key(self, event=None):
        """Close window, when 'Escape' is pushed."""
        event.widget.destroy()

    def show_point(self, coord, colour='white'):
        self.canvas.create_oval(coord[0]-self.d, coord[1]-self.d, coord[0]+self.d, coord[1]+self.d, fill=colour)

    def point_movement(self, a, b):
        """Move the point."""
        self.canvas.delete("all")
        temp_x = self.x + a * self.step_x
        temp_y = self.y + b * self.step_y

        if self.check_inbound([temp_x, temp_y]):
            self.x = temp_x
            self.y = temp_y

        self.show_point([self.x, self.y], colour=self.colour)
    
    def left_key(self, event=None):
        """Calculate direction of movement for left key."""
        if self.mon == 1:
            a = (-1) ** (self.mon + self.mov)
            b = 0
        else:
            a = 0
            b = (-1) ** (self.mon + self.mov)
        self.point_movement(a, b)

    def up_key(self, event=None):
        """Calculate direction of movement for up key."""
        if self.mon == 1:
            a = 0
            b = (-1) ** (self.mon + self.mov + 1)
        else:
            a = (-1) ** (self.mon + self.mov)
            b = 0
        self.point_movement(a, b)

    def right_key(self, event=None):
        """Calculate direction of movement for right key."""
        if self.mon == 1:
            a = (-1) ** (self.mon + self.mov + 1)
            b = 0
        else:
            a = 0
            b = (-1) ** (self.mon + self.mov + 1)
        self.point_movement(a, b)

    def down_key(self, event=None):
        """Calculate direction of movement for down key."""
        if self.mon == 1:
            a = 0
            b = (-1) ** (self.mon + self.mov)
        else:
            a = (-1) ** (self.mon + self.mov + 1)
            b = 0
        self.point_movement(a, b)

    def config_up_event(self, event=None):
        """Create a point up on canvas and on the list for region around whorl, in config window."""
        #create and display point on canvas
        temp_y = self.config_y
        self.config_y -= 20
        line = self.canvas.create_line(self.config_x, temp_y, self.config_x, self.config_y)
        point = self.canvas.create_oval(self.config_x-2, self.config_y-2, self.config_x+2, self.config_y+2, fill='blue')
        self.config_list_canvas.append(line)
        self.config_list_canvas.append(point)
        #appending to the list for movement
        self.config_list.append('up')

    def config_nasal_event(self, event=None):
        """Create a point nasal on canvas and on the list for region around whorl, in config window."""
        #create and display point on canvas
        temp_x = self.config_x
        self.config_x -= 20
        line = self.canvas.create_line(temp_x, self.config_y, self.config_x, self.config_y)
        point = self.canvas.create_oval(self.config_x-2, self.config_y-2, self.config_x+2, self.config_y+2, fill='yellow')
        self.config_list_canvas.append(line)
        self.config_list_canvas.append(point)
        #appending to the list for movement
        self.config_list.append('nasal')

    def config_temp_event(self, event=None):
        """Create a point temp on canvas and on the list for region around whorl, in config window."""
        #create and display point on canvas
        temp_x = self.config_x
        self.config_x += 20
        line =self.canvas.create_line(temp_x, self.config_y, self.config_x, self.config_y)
        point = self.canvas.create_oval(self.config_x-2, self.config_y-2, self.config_x+2, self.config_y+2, fill='green')
        self.config_list_canvas.append(line)
        self.config_list_canvas.append(point)
        #appending to the list for movement
        self.config_list.append('temporal')

    def config_down_event(self, event=None):
        """Create a point down on canvas and on the list for region around whorl, in config window."""
        #create and display point on canvas
        temp_y = self.config_y
        self.config_y += 20
        line = self.canvas.create_line(self.config_x, temp_y, self.config_x, self.config_y)
        point = self.canvas.create_oval(self.config_x-2, self.config_y-2, self.config_x+2, self.config_y+2, fill='brown')
        self.config_list_canvas.append(line)
        self.config_list_canvas.append(point)
        #appending to the list for movement
        self.config_list.append('down')

    def config_reset_event(self, event=None):
        """Erase all point oon the config-canvas."""
        #erase elements on canvas
        for item in self.config_list_canvas:
            self.canvas.delete(item)
        #set start coordinates to whorl again
        self.config_x = self.x0
        self.config_y = self.y0
        #delete elements of config_list
        self.config_list = []
        #set config mode variable on false
        self.config_bool = False

    def config_save_event(self, event=None):
        #save pattern in a file
        self.filename = f"./saved/patterns/pattern_{self.save_link.get()}.txt"
        with open(self.filename, "w") as file:
            for item in self.config_list:
                file.write(f'{item} ')
        self.config_window.destroy()
        self.open_text.set('loaded')
        self.load_config_list()
    
    def load_file(self, event=None):
        #load pattern-file and show it in the input, return file name
        self.filename = filedialog.askopenfilename(initialdir="./saved/patterns/", title="Select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        self.short_name = os.path.basename(self.filename)
        self.open_variable.set(self.short_name)
        self.config_bool = True
        self.open_file()
    
    def load_config_list(self):
        try:
            with open(self.filename, "r") as file:
                for row in file:
                    self.config_list = row.strip().split(" ")
            self.config_bool = True
        except:
            messagebox.showerror("Error", "The file doesen't exist.\n Load another file.")
            self.settings['pattern_check'] = 0
            self.open_text.set('')
    
    def open_file(self, event=None):
        if self.config_bool:
            try:
                self.open_text.set('loaded')
                self.load_window.destroy()
                #read file into self.config_list
                self.load_config_list()
            except:
                pass

    def create_list(self, event=None):
        #adapt list around whorl
        if not self.config_bool:
            self.config_list = ['nasal', 'up', 'temporal', 'temporal', 'down', 'down', 'nasal', 'nasal']
        elif self.settings['pattern_check']:
            pass
        #create list
        self.list_of_points = automated_list(self.mon, self.eye, [self.x, self.y], self.get_steps_available([self.x, self.y]), 
                                                self.seq_param, [self.step_x, self.step_y, self.step_x_whorl, self.step_y_whorl], 
                                                self.id.get(), self.config_list, self.config_bool)
        self.temp_list = self.list_of_points

    def control_raster(self, event=None):
        """Show list at once, for controlling purpose."""
        self.create_list()
        for point in self.temp_list:
            self.show_point(point, colour='orange')
        self.create_bool = False

    def auto_mov(self, event=None):
        """Get list of points and move along it, manually or automatically."""
        col = 'white'
        self.canvas.delete("all")

        if self.create_bool:
            self.create_list()
            self.create_bool = False

        #disable arrows keys
        self.test_window.unbind('<KP_Left>')
        self.test_window.unbind('<KP_Up>')
        self.test_window.unbind('<KP_Right>')
        self.test_window.unbind('<KP_Down>')
        self.test_window.unbind('<Left>')
        self.test_window.unbind('<Up>')
        self.test_window.unbind('<Right>')
        self.test_window.unbind('<Down>')
        self.test_window.unbind('t')
        self.test_window.unbind('<KP_5>')

        #stay at last point, colored in red
        if self.count == len(self.list_of_points):
            col = 'red'
            self.count -= 1

        amount_of_points_showed = 0
        #show point
        if self.switch.get() == 1:              # if mode automated
            #disable buttons, enable "pause"-button
            self.test_window.unbind('<KP_Enter>')
            self.test_window.bind('<KP_Enter>', self.auto_go_pause)
            self.test_window.unbind('<Return>')
            self.test_window.bind('<Return>', self.auto_go_pause)
            self.test_window.bind('<KP_Subtract>', self.auto_pause)
            self.test_window.bind('<a>', self.auto_pause)

            time.sleep(1)
            #send signal to virtual pedal
            if self.pedal:
                foot_switch.send_signal(self.ser)
            
            for count in range(self.point_amount):
                try:
                    self.canvas.delete("all")
                    self.show_point(self.temp_list[count], colour=col)
                    self.canvas.update()
                    time.sleep(self.pause)
                    #if virtual pedal not used
                    if not self.pedal:
                        #pause if subtract or a is pressed
                        if self.pause_check or count == self.point_amount - 1:
                            #remove point from temp list that have already been shown
                            self.temp_list = self.temp_list[count:]
                            self.count += 1
                            self.pause_check = True
                            break
                    else:   #if virtual pedal is used
                        if count == self.point_amount-1:
                            #remove point from temp list that have already been shown
                            self.temp_list = self.temp_list[count:]
                            self.count += 1
                            #pause for 5 seconds (to achieve a pause of 6 seconds)
                            time.sleep(5)
                            #restart
                            self.auto_mov()

                    amount_of_points_showed += 1
                except:
                    break
            #stay on last point on red
            try:
                if amount_of_points_showed == len(self.temp_list):
                    self.show_point(self.temp_list[-1], colour='red')
            except:
                pass

        else:                                   # if mode semi-automated
            self.show_point(self.temp_list[self.count], colour=col)
            self.count += 1

    def auto_go_pause(self, event=None):
        """Start or pause sequences of points again if mode=automated when "Enter" is pressed."""
        if not self.pause_check:
            self.pause_check = True
            self.pause_count = 1
        else:
            self.pause_check = False
            self.auto_mov()

    def auto_go(self, event=None):
        """Start sequences of points again if mode=automated and it was paused"""
        self.pause_check = False
        self.auto_mov()
    
    def auto_pause(self, event=None):
        """Pause sequence in mode=automated."""
        self.pause_check = True
        self.pause_count = 1,
    
    def images_rate(self, point_rate, image_rate):
        """Return time for automated mode, after which the sequence should be paused."""
        duration = 100 / image_rate
        amount = duration / point_rate
        return int(amount - 1)

    def open_config_window(self, event=None):
        """Open config window."""
        #configure window
        self.config_window = tk.Toplevel(self.root)
        self.config_window.geometry("660x400")
        self.config_window.title("Pattern Configuration")

        #bind keys to events
        self.config_window.bind('<Escape>', self.on_escape_key)
        self.config_window.bind('<Return>', self.config_save_event)
        self.config_window.bind('<KP_Enter>', self.config_save_event)
        self.config_window.bind('<KP_Left>', self.config_nasal_event)
        self.config_window.bind('<KP_Up>', self.config_up_event)
        self.config_window.bind('<KP_Right>', self.config_temp_event)
        self.config_window.bind('<KP_Down>', self.config_down_event)
        self.config_window.bind('<Left>', self.config_nasal_event)
        self.config_window.bind('<Up>', self.config_up_event)
        self.config_window.bind('<Right>', self.config_temp_event)
        self.config_window.bind('<Down>', self.config_down_event)

        #Instruction window
        def open_instruction():
            instruction_window = tk.Toplevel(self.config_window)
            instruction_window.title("Pattern Configuration Instruction")
            instruction_label = tk.Label(instruction_window, text="INSTRUCTIONS: Here you can draw your own pattern around the whorl (red point). "  
                                     "From your last point, the software will add a step down and then start with the rectangle, moving first temporally. " +
                                     "Insert the point for the right eye fixating: on the canvas will be displayed how the point will move on the screen. " +
                                     "The colors of the points are only to show in which direction you moved: no other meaning behind. " +
                                     "You can use the arrows on the keypad or the buttons to add points.\n" +
                                     "RESET: erase all points and you can start again from the whorl.\n" +
                                     "CLOSE: close the window without saving the pattern.\n"+
                                     "SAVE: save the pattern in a file, please before pushing the button, insert a vaild name. The pattern "+
                                     "will be directly uploaded in the software.", wraplength=400, justify='left')
            instruction_label.grid(row=0, column=0)
            close_button = tk.Button(instruction_window, text='Close', command=instruction_window.destroy)
            close_button.grid(row=1, column=0)

        #empty config_list
        self.config_list = []
        
        #create Frames
        button_frame = tk.Frame(self.config_window, width=100)
        canvas_frame = tk.Frame(self.config_window, width=400, height=400)
        end_frame = tk.Frame(self.config_window)
        button_frame.grid(row=0, column=0)
        canvas_frame.grid(row=0, column=1)
        end_frame.grid(row=3, column=0)

        #Instruction button
        instruction_button = tk.Button(button_frame, text='README', command=open_instruction)
        instruction_button.grid(row=0, column=1)
        #empty row
        empty_row = tk.Label(button_frame)
        empty_row.grid(row=1, column=0)
        #Directions buttons
        up_button = tk.Button(button_frame, text="up", command=self.config_up_event, width=7)
        up_button.grid(row=2, column=1)
        nasal_button = tk.Button(button_frame, text="nasal", command=self.config_nasal_event, width=7)
        nasal_button.grid(row=3, column=0)
        temp_button = tk.Button(button_frame, text="temporal", command=self.config_temp_event, width=7)
        temp_button.grid(row=3, column=2)
        down_button = tk.Button(button_frame, text="down", command=self.config_down_event, width=7)
        down_button.grid(row=4, column=1)
        #empty row
        empty_row = tk.Label(button_frame)
        empty_row.grid(row=5, column=0)
        #Other buttons
        reset_button = tk.Button(button_frame, text="Reset", command=self.config_reset_event, background="red")
        reset_button.grid(row=8, column=0)
        close_button = tk.Button(button_frame, text="Close", command=self.config_window.destroy)
        close_button.grid(row=8, column=1)
        #save pattern
        save_label = tk.Label(button_frame, text='File name: ')
        save_label.grid(row=6, column=0, sticky=tk.E)
        self.save_link = tk.Entry(button_frame, bd=2, width=20)
        self.save_link.grid(row=6, column=1, columnspan=2, sticky=tk.E)
        save_button = tk.Button(button_frame, text="Save", command=self.config_save_event, background='green')
        save_button.grid(row=8, column=2)

        #Canvas to display movements
        self.canvas = tk.Canvas(canvas_frame, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_rectangle(1, 1, 399, 399, outline='blue')

        #List of points for canvas, without whorl
        self.config_list_canvas = []
        #Startpoint coordinates
        self.x0, self.y0 = 200, 200
        #create variables
        self.config_x, self.config_y = self.x0, self.y0
        #Startpoint on canvas
        self.canvas.create_oval(self.x0-5, self.y0-5, self.x0+5, self.y0+5, fill='red')

    def load_config(self):
        """Open loading window."""
        #Loading window
        self.load_window = tk.Toplevel(self.root)
        #self.load_window.geometry("400x100")
        self.load_window.title("Load Pattern")
        #if file saved as default, load it
        file = ''
        if self.settings['pattern_check']:
            file = self.short_name
        else:
            self.config_bool = False
        #entry field for file name
        self.open_variable = tk.StringVar(self.load_window, value=file)
        self.open_link = tk.Entry(self.load_window, textvariable=self.open_variable, bd=2, width=27)
        self.open_link.grid(row=0, column=0, columnspan=2, sticky=tk.E)
        #button to search file
        load_button = tk.Button(self.load_window, text="...", command=self.load_file)
        load_button.grid(row=0, column=2) 
        open_button = tk.Button(self.load_window, text="Open", command=self.open_file)
        open_button.grid(row=0, column=3)
        #should the file be set as default?
        open_label = tk.Label(self.load_window, text='Define this pattern as default?')
        open_label.grid(row=1, column=0)
        self.open_check = tk.IntVar(self.load_window, value=self.settings['pattern_check'])
        open_checkbox = tk.Checkbutton(self.load_window, variable=self.open_check)
        open_checkbox.grid(row=1, column=1)
        #bind escape and enter button
        self.load_window.bind('<Escape>', self.on_escape_key)
        self.load_window.bind('<KP_Delete>', self.on_escape_key)
        self.load_window.bind('<Return>', self.open_file)
        self.load_window.bind('<KP_Enter>', self.open_file)

    def open_test_window(self):
        """Open test window, create list of points, be ready to show points."""

        #configure window
        self.test_window = tk.Toplevel(self.root)
        self.test_window.attributes('-fullscreen', True)         #for Windows-OS
        self.test_window.configure(background="black")
        # Konfigurieren Sie das Grid so, dass es expandiert
        self.test_window.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.test_window, bg='black', width=self.screen_width,  height=self.screen_height)  # Definieren Sie canvas als Klassenattribut
        self.canvas.grid(sticky="ns")  # Sticky in alle vier Richtungen

        #variables to create only once the list of points for automatic movement
        self.count = 0
        self.create_bool = True

        #bind keys to events
        self.test_window.bind('<Escape>', self.on_escape_key)
        self.test_window.bind('<KP_Delete>', self.on_escape_key)
        self.test_window.bind('<KP_Left>', self.left_key)
        self.test_window.bind('<KP_Up>', self.up_key)
        self.test_window.bind('<KP_Right>', self.right_key)
        self.test_window.bind('<KP_Down>', self.down_key)
        self.test_window.bind('<Left>', self.left_key)
        self.test_window.bind('<Up>', self.up_key)
        self.test_window.bind('<Right>', self.right_key)
        self.test_window.bind('<Down>', self.down_key)
        self.test_window.bind('t', self.control_raster)
        self.test_window.bind('<KP_5>', self.control_raster)

        #if sequence (semi-)automated is selected, enable "Enter"-button, if not set colour of dot on white
        if self.switch.get() != 3:
            self.colour='yellow'
            self.test_window.bind('<Return>', self.auto_mov)
            self.test_window.bind('<KP_Enter>', self.auto_mov)
            self.pause_check = False
            self.pause_count = 0
            temp_ivcmrate = float(self.ivcm_rate.get())
            if temp_ivcmrate == 0:
                temp_ivcmrate = 0.01
                print(temp_ivcmrate)
            self.point_amount = self.images_rate(float(self.speed.get()), temp_ivcmrate)
        else:
            self.colour='white'

        #get dimensions of screen
        self.max_x = self.test_window.winfo_screenwidth()
        self.max_y = self.test_window.winfo_screenheight()
        #call diameter of point, monitor and movement directions
        self.d = int(self.diam.get())
        self.mon = self.monitor.get()
        monitor = ['horizontal', 'vertical, clockwise', 'vertical, counterclockwise']
        self.mov = self.movement.get()
        movement_descr = ['fixation', 'plexus']
        #get information for automated sequence
        self.auto = self.switch.get()
        mode = ['AUTOMATED', 'SEMI-AUTOMATED', 'MANUAL']
        pedal = ['deactivated', 'activated']
        self.eye = self.eye_input.get()
        eyes = ['OS', 'OD']
        self.seq_param = [int(self.rect_w.get()), int(self.rect_h.get()), int(self.whorl.get()), int(self.steps_n.get())]
        self.pause = float(self.speed.get())
        self.identification = self.id.get()
        #determine step sizes
        self.step_x = int(self.dist.get()) * self.ratio()[0]
        self.step_y = int(self.dist.get()) * self.ratio()[1]
        self.step_x_whorl = int(self.distw.get()) * self.ratio()[0]
        self.step_y_whorl = int(self.distw.get()) * self.ratio()[1]
        #starting point
        self.x = self.max_x * float(self.start_x.get())
        self.y = self.max_y * float(self.start_y.get())
        self.canvas.create_rectangle(self.x-self.d-2, self.y-self.d-2, self.x+self.d+2, self.y+self.d+2, fill='yellow')     

        #save settings
        with open(f"saved/settings/settings_{self.identification}.txt", "w") as file:
            file.write(f"id= {self.identification}\n")
            file.write(f"fixation eye= {eyes[self.eye-1]}\n")
            file.write(f"distance between points= {self.dist.get()} mm\n")
            file.write(f"distance between points in whorl= {self.distw.get()} mm\n")
            file.write(f"dot size= {self.d} mm\n") 
            file.write(f"monitor direction= {monitor[self.mon-1]}\n")    
            file.write(f"movement direction= {movement_descr[self.mov-1]}\n") 
            file.write(f"screen dimensions= {self.dim_w.get()} / {self.dim_h.get()} mm\n") 
            file.write(f"screen resolution= {self.screen_width} / {self.screen_height} pixels\n\n") 
            file.write(f"SEQUENCE\nrectangle dimensions= {self.seq_param[0]} / {self.seq_param[1]} images\n")
            file.write(f"distance between whorl and rectangle= {self.seq_param[2]} images\n")
            file.write(f"number of steps nasally= {self.seq_param[3]} images\n")
            file.write(f"mode= {mode[self.auto-1]}\n")
            file.write(f"time between points= {self.pause} s\n")
            file.write(f"foot switch= {pedal[self.pedal]}\n")
            if self.config_bool:
                file.write(f'pattern used= {self.filename}')

    def close_event(self):
        """Close program."""
        #change default.txt file if something changed
        try:
            temp_check = self.open_check.get()
        except:
            temp_check = self.settings['pattern_check']

        self.settings['pattern_check'] = temp_check
        if temp_check and self.filename != self.settings['pattern_file']:
            self.settings['pattern_file'] = self.filename
            
        with open(f"./default.txt", "w") as file:
            for key,value in self.settings.items():
                file.write(f'{key}={value}\n')
        
        #close port
        try:
            foot_switch.close_port(self.ser)
        except:
            pass

        #close software
        self.root.destroy()

    def start_event(self, event=None):
        """Start test window."""
        #create connection to foot_switch
        self.pedal = self.pedal_var.get()

        if self.pedal:
            if self.ser:
                self.root.after(100, self.open_test_window)
            else:
                messagebox.showerror("Error", "Virtual pedal has not been initialised.\nDo it and try again.")   
        else:
            self.root.after(100, self.open_test_window)

root = tk.Tk()
app = MyApp(root)

if __name__ == '__main__':
    
    root.mainloop()
