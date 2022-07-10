
from tkinter import HORIZONTAL, Checkbutton, OptionMenu, Tk ,Toplevel
from tkinter import Canvas, Frame
from tkinter import Label, Text, Entry, Button, messagebox, Listbox
from tkinter import END, TOP, RIGHT, LEFT, N, W, S, BOTH, VERTICAL, Y, E, WORD
from tkinter import StringVar, INSERT, IntVar
from tkinter import ttk
from tkinter.constants import ANCHOR
import GUI.constants as c
import GUI.functions as f
import Scrape.constants as browser_config
from Scrape.scrape import ScrapeAuction
import threading, os

class ScrollableFrame(Frame):
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.canvas = Canvas(self, borderwidth=0, background="#EEF5DB")
        self.frame = Frame(self.canvas, background="#EEF5DB")
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)


    def add_data(self, bidder_lst, acc):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for index,item in enumerate(bidder_lst):

            money = '{:,}'.format(item['money'])
            canvas_color = c.CanvasEven if index%2 else c.CanvasOdd

            self.row_canvas = Canvas(self.frame, bg=canvas_color)
            self.row_canvas.pack(pady=index%2*10)
            
            Label(self.row_canvas, fg=c.LabelFgColour, bg=canvas_color, font=c.Fonth2, text="ITEM NAME:").grid(sticky=W, row=0, column=0, pady=5, padx=10)
            Label(self.row_canvas, fg=c.LabelFgColour, bg=canvas_color, font=c.Fonth2, text=c.item_name_lst[item["id"]]).grid(sticky=W, row=0, column=1, pady=5, padx=10)

            Label(self.row_canvas, fg=c.LabelFgColour, bg=canvas_color, font=c.Fonth2, text="USERNAME:").grid(sticky=W, row=1, column=0, pady=5, padx=10)
            Label(self.row_canvas, fg=f.check_name(acc['name'], item['name'], c.LabelFgColour), bg=canvas_color, font=c.Fonth2, text=item['name']).grid(sticky=W, row=1, column=1, pady=5, padx=10)

            Label(self.row_canvas, fg=c.LabelFgColour, bg=canvas_color, font=c.Fonth2, text="MONEY:").grid(sticky=W, row=2, column=0, pady=5, padx=10)
            Label(self.row_canvas, fg=f.check_money(acc['money'], item['money']), bg=canvas_color, font=c.Fonth2, text=money).grid(sticky=W, row=2, column=1, pady=5, padx=10)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_rows(self):
        for row in self.frame.winfo_children():
            row.destroy()

class App(Tk):
    def __init__(self):
        super().__init__()

        self.resizable(width=False, height=False)
        self.title(c.AppTitle)
        self.iconbitmap(c.AppIconPath)

        # Canvas
        self.canvas = Canvas(self, height=550, width=900, bg=c.CanvasColour)
        self.canvas.pack()

        # Frames
        self.frame_A  = Frame(self, bg=c.FrameColourA)
        self.frame_A.place(relx=0.2, rely=0, relwidth=0.3, relheight=0.5)
        
        self.frame_B = Frame(self, bg=c.FrameColourB)
        self.frame_B.place(relx=0.5, rely=0.15, relwidth=0.5, relheight=0.85)

        self.frame_C = Frame(self, bg=c.FrameColourC)
        self.frame_C.place(relx=0, rely=0.5, relwidth=0.2, relheight=0.5)

        self.frame_D = Frame(self, bg=c.FrameColourD)
        self.frame_D.place(relx=0.2, rely=0.5, relwidth=0.3, relheight=0.5)

        self.frame_E = Frame(self, bg=c.FrameColourE)
        self.frame_E.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.15)

        self.frame_F = Frame(self, bg=c.FrameColourF)
        self.frame_F.place(relx=0, rely=0, relwidth=0.2, relheight=0.5)

        # Frame A (ship choosing section)
        Label(self.frame_A, fg=c.BLACK, bg=c.FrameColourA, text="Choose Ship", font=c.Fonth1).pack(pady=10)

        self.ship_list = Listbox(self.frame_A, width=40, height=9, fg=c.ListFgColour, bg=c.ListBgColour)
        self.ship_list.pack(pady=15)

        ship_name_list = f.yaml_return_namelist()
        for num, item in enumerate(ship_name_list, 1):
            self.ship_list.insert(END, f"{num}) {item}")

        self.submit_button = Button(self.frame_A, font=c.Fonth2, text="Run", fg=c.ButtonFgColour, bg=c.ButtonBgColour, height=1, width=6, command=self.start_thread)
        self.submit_button.pack()
    

        # Frame B (results of searching for auction items)
        self.result_frame = ScrollableFrame(self.frame_B)
        self.result_frame.pack(side="top", fill="both", expand=True)
        self.result_frame.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Frame C (check box section)
        self.laserx2 = IntVar(value=1)
        self.laserx3 = IntVar(value=1)
        self.laserabs = IntVar(value=1)
        self.rocket4k = IntVar(value=1)
        self.rocket6k = IntVar(value=1)
        self.speedgen = IntVar(value=1)
        self.shieldgen = IntVar(value=1)
        self.lf3 = IntVar(value=1)
        self.iris = IntVar(value=1)

        c_laserx2 = Checkbutton(self.frame_C, text="Laser X2", variable=self.laserx2, bg=c.FrameColourC)
        c_laserx3 = Checkbutton(self.frame_C, text="Laser X3", variable=self.laserx3, bg=c.FrameColourC)
        c_laserabs = Checkbutton(self.frame_C, text="Laser Absorber", variable=self.laserabs, bg=c.FrameColourC)
        c_rocket4k = Checkbutton(self.frame_C, text="Rocket (4k)", variable=self.rocket4k, bg=c.FrameColourC)
        c_rocket6k = Checkbutton(self.frame_C, text="Rocket (6k)", variable=self.rocket6k, bg=c.FrameColourC)
        c_speedgen = Checkbutton(self.frame_C, text="Speed Generator", variable=self.speedgen, bg=c.FrameColourC)
        c_shieldgen = Checkbutton(self.frame_C, text="Shield Generator", variable=self.shieldgen, bg=c.FrameColourC)
        c_lf3 = Checkbutton(self.frame_C, text="LF-3", variable=self.lf3, bg=c.FrameColourC)
        c_iris = Checkbutton(self.frame_C, text="Iris", variable=self.iris, bg=c.FrameColourC)
        
        c_laserx2.pack(pady=3)
        c_laserx3.pack(pady=3)
        c_laserabs.pack(pady=3)
        c_rocket4k.pack(pady=3)
        c_rocket6k.pack(pady=3)
        c_speedgen.pack(pady=3)
        c_shieldgen.pack(pady=3)
        c_lf3.pack(pady=3)
        c_iris.pack(pady=3)


        # Frame D (Log section)
        # Label(self.frame_D, fg=c.BLACK, bg=c.FrameColourD, text="LOGS", font=c.Fonth1).pack(pady=17)

        self.log_text = Text(self.frame_D, fg=c.TextboxFgColour, bg=c.TextboxBgColour, width=35, height=11, font=c.Fonttext, wrap=WORD)
        self.log_text.pack(pady=17)
        self.log_text.insert(END, "-------------------- LOGS -------------------\n")
        self.log_text.config(state='disabled')

        self.progress_bar = ttk.Progressbar(self.frame_D, orient=HORIZONTAL, length=250, mode='determinate')
        self.progress_bar.pack(pady=10)
        self.progress_count = 5

        # Frame E (General information about daily auction)
        Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="|USERNAME|").grid(sticky=W, row=0, column=0, pady=10, padx=8)
        Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="|CREDI|").grid(sticky=W, row=0, column=1, pady=10, padx=8)
        Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="|URIDIUM|").grid(sticky=W, row=0, column=2, pady=10, padx=8)
        Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="|DEADLINE|").grid(sticky=W, row=0, column=3, pady=10, padx=8)

        self.InfoUsernameLabel = Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="")
        self.InfoCrediLabel = Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="")
        self.InfoUriLabel = Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="")
        self.InfoDeadlineLabel = Label(self.frame_E, fg=c.LabelFgColour, bg=c.FrameColourE, font=c.Fonth2, text="")

        self.InfoUsernameLabel.grid(row=1, column=0, pady=10, padx=8)
        self.InfoCrediLabel.grid(row=1, column=1, pady=10, padx=8)
        self.InfoUriLabel.grid(row=1, column=2, pady=10, padx=8)
        self.InfoDeadlineLabel.grid(row=1, column=3, pady=10, padx=8)

        # Frame F (Config Palet)

        Label(self.frame_F, fg=c.BLACK, bg=c.FrameColourF, font=c.Fonth1, text="Config").pack(pady=7)

        self.clear_data_button = Button(self.frame_F, font=c.Fonth2, text="Clear Data", fg=c.ButtonFgColour, bg=c.ButtonBgColour, height=1, width=12, command=self.clear_data)
        self.clear_data_button.pack()

        self.select_all_button = Button(self.frame_F, font=c.Fonth2, text="Select All Prompts", fg=c.ButtonFgColour, bg=c.ButtonBgColour, height=1, width=16, command=self.select_all_promps)
        self.select_all_button.pack()

        self.deselect_all_button = Button(self.frame_F, font=c.Fonth2, text="Deselect All Prompts", fg=c.ButtonFgColour, bg=c.ButtonBgColour, height=1, width=16, command=self.deselect_all_promps)
        self.deselect_all_button.pack()
        
        self.reverse_all_button = Button(self.frame_F, font=c.Fonth2, text="Reverse All Prompts", fg=c.ButtonFgColour, bg=c.ButtonBgColour, height=1, width=16, command=self.reverse_all_promps)
        self.reverse_all_button.pack()

        self.headless_valid = IntVar(value=int(browser_config.headless_webbrowser))
        headless_box = Checkbutton(self.frame_F, text="Headless", variable=self.headless_valid, bg=c.FrameColourF)
        headless_box.pack(pady=5)

        self.purchase_valid = IntVar(value=int(browser_config.purchase_valid))
        headless_box = Checkbutton(self.frame_F, text="Purchase", variable=self.purchase_valid, bg=c.FrameColourF)
        headless_box.pack(pady=5)

    def _on_mousewheel(self, event):
        self.result_frame.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def clear_data(self):
        self.clear_log()
        self.clear_progress()
        self.result_frame.clear_rows()

    def select_all_promps(self):
        item_lst = [self.laserx2,self.laserx3,self.laserabs,self.rocket4k,self.rocket6k,self.speedgen,self.shieldgen,self.lf3,self.iris]

        for item in item_lst:
            if not item.get():
                item.set(1)

    def deselect_all_promps(self):
        item_lst = [self.laserx2,self.laserx3,self.laserabs,self.rocket4k,self.rocket6k,self.speedgen,self.shieldgen,self.lf3,self.iris]

        for item in item_lst:
            if item.get():
                item.set(0)

    def reverse_all_promps(self):
        item_lst = [self.laserx2,self.laserx3,self.laserabs,self.rocket4k,self.rocket6k,self.speedgen,self.shieldgen,self.lf3,self.iris]

        for item in item_lst:
            if item.get():
                item.set(0)
            else:
                item.set(1)

    def switch_button(self):
        button = self.submit_button
        if button['state'] == 'normal':
            self.submit_button['state'] = 'disable'
        else:    
            self.submit_button['state'] = 'normal'

    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', END)
        self.log_text.insert(END, "-------------------- LOGS -------------------\n")
        self.log_text.config(state='disabled')

    def clear_progress(self):
        self.progress_bar['value'] = 0

    def start_thread(self):
        t = threading.Thread(target=self.run_proc)
        t.start()

    def run_proc(self):

        self.switch_button()
        self.clear_log()
        self.clear_progress()

        anchor = self.ship_list.get(ANCHOR)

        item_lst = [self.laserx2.get(), self.laserx3.get(), self.laserabs.get(), self.rocket4k.get(), self.rocket6k.get(), self.speedgen.get(), self.shieldgen.get(), self.lf3.get(), self.iris.get()]
        new_lst = [i[0] for i in enumerate(item_lst) if i[1]==1]

        if not anchor:
            self.print_log("A ship have to be checked!")
            self.switch_button()
            return False
        
        choosed_ship = f.choose_ship_by_id(anchor[0])

        if not new_lst:
            self.print_log("At least checkbox must be checked!")
            self.switch_button()
            return False

        self.print_log("Bot will have been gathering \n   information as: "+choosed_ship['name'])
        self.progress_bar['value'] += self.progress_count

        scrape = ScrapeAuction()
        self.print_log("Creating a new page...")
        scrape.setUpClass(self)
        self.progress_bar['value'] += self.progress_count
        account, bidder_lst = scrape.run_scrape(choosed_ship['name'], choosed_ship['password'], new_lst, self)
        scrape.tearDownClass()
        self.progress_bar['value'] += self.progress_count

        self.print_results(bidder_lst, account)
        self.progress_bar['value'] += self.progress_count
        self.print_log("Gathering information is succesfully \n   completed!")
        self.print_log("--------------------------------------------")
            
        self.switch_button()
        self.progress_bar['value'] = 100
        
        return True

    def print_log(self, text):
        self.log_text.config(state='normal')
        self.log_text.insert(END, "-> "+text+"\n")
        self.log_text.config(state='disabled')
        self.log_text.see("end")
    
    def print_results(self, bidder_lst, acc):

        self.InfoUsernameLabel.config(text=acc['name'])
        self.InfoCrediLabel.config(text=acc['money'])
        self.InfoUriLabel.config(text=acc['money2'])
        self.InfoDeadlineLabel.config(text=acc['deadline'])

        self.result_frame.add_data(bidder_lst, acc)
    