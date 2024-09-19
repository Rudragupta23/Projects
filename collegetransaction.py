import mysql.connector
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# This class is responsible for creating main
# window with menu buttons, container and 4 frames for 4 different pages
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("College Transactions")
        self.iconbitmap("logo.ico")
        self.geometry("990x615+175+90")
        self.minsize(900,550)
        self.bind('<Escape>', lambda event: self.quit())

        style = ttk.Style()
        style.configure("TButton",font=('', 11), width=20)
        menu = ttk.Frame(self, borderwidth=4)
        menu.pack(side='left', fill='y')

        title = ttk.Label(menu, text="College Transactions", font="Helvetica 15 bold")
        home = ttk.Button(menu, text="Home Page", command=lambda: self.show_frame(HomePage))
        add = ttk.Button(menu, text="Data Page", command=lambda: self.show_frame(Add))
        analyse = ttk.Button(menu, text="Analysis Page", command=lambda: self.show_frame(Analyse))

        title.pack()
        home.pack()
        add.pack()
        analyse.pack()

        container = ttk.Frame(self)
        container.pack(side="top", expand=True, fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.HomePage = HomePage
        self.Add = Add
        self.Analyse = Analyse

        # first time creating frame and storing in frames list
        for F in {HomePage, Add, Analyse}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    # simple function to lift the frame on top
    def show_frame(self, frame):
        self.frames[frame].tkraise()

# This class only has image
class HomePage(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        # Importing image(in variable background), creating canvas, pack image in canvas in nw.
        self.background = Image.open("img1.jpg").resize((948,767))
        self.background_tk = ImageTk.PhotoImage(self.background)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')
        self.canvas.create_image(0, 0, image=self.background_tk, anchor='nw')
        self.canvas.bind('<Configure>', self.resize_image)

    # this function resizes the image according to img aspect ratio.
    def resize_image(self, event):
        image_ratio = 1.75
        canvas_ratio = event.width / event.height

        if canvas_ratio > image_ratio:  # canvas is wider then image
            width = event.width
            height = int(event.width / image_ratio)
        else:  # canvas is narrower then image
            height = event.height
            width = int(event.height * image_ratio)

        new_background = self.background.resize((width, height))
        self.background_tk = ImageTk.PhotoImage(new_background)
        self.canvas.create_image(int(event.width/2), int(event.height/2), image=self.background_tk, anchor='center')

# This is the biggest and most important part...
# This class facilitates adding new data and showing past data
# this data page frame is further have 2 frames (add_f1 and add_f2).pack()
# inside add_f1 we use grid where as in add_f2 we use pack()
class Add(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        add_t = ttk.Label(self, text="Add Transactions", font=('Times', '20'))
        add_t.pack()

        # These are placeholders for add_f1
        courser.execute("select count(*) from entry;")
        self.no = tk.IntVar(value=courser.fetchone()[0]+1)
        date_value = tk.StringVar(value="dd/mm/2024")
        note_value = tk.StringVar(value="note")
        type_value = tk.StringVar(value="Category")
        mode_value = tk.BooleanVar()
        amount_value = tk.DoubleVar()

        add_f1 = ttk.Frame(self)
        add_f1.pack(fill='x')
        add_f1.columnconfigure((0,1,2,3,4,5,6), weight=1)
        add_f1.rowconfigure(0, weight=1)

        # add_f1 widgets
        types = ["food","pocket money","friend/partner","stationary","events","personal","shopping","other"]
        date_entry = ttk.Entry(add_f1, textvariable=date_value)
        note_entry = ttk.Entry(add_f1, textvariable=note_value)
        type_entry = ttk.Combobox(add_f1, textvariable=type_value)
        type_entry['value'] = types
        mode_online = ttk.Radiobutton(add_f1, text="Online", value=False, variable=mode_value)
        mode_offline = ttk.Radiobutton(add_f1, text="Offline", value=True, variable=mode_value)
        amount_entry = ttk.Entry(add_f1, textvariable=amount_value)

        # griding add_f1 widgets
        ttk.Label(add_f1, textvariable=self.no).grid(row=0, column=0,rowspan=2, sticky='ew')
        date_entry.grid(row=0, column=1,rowspan=2, sticky='ew')
        note_entry.grid(row=0, column=2,rowspan=2, sticky='ew')
        mode_online.grid(row=0, column=3)
        mode_offline.grid(row=1, column=3)
        type_entry.grid(row=0, column=4,rowspan=2, sticky='ew')
        amount_entry.grid(row=0, column=5,rowspan=2, sticky='ew')
        add_data = ttk.Button(add_f1, text="Add Data",
                              command=lambda: self.add_data(date_value,note_value,type_value,mode_value,amount_value))
        add_data.grid(row=0, column=6, rowspan=2)

        show_t = ttk.Label(self, text="Show Transactions", font=('Times', '20'))
        show_t.pack()
        add_f2 = ttk.Frame(self)
        add_f2.pack()

        refresh = ttk.Button(add_f2, text="Refresh Data",
                             command=lambda:self.show_data("select * from entry order by Date desc;"))
        refresh.pack(side='left')

        # different qsl commands stored in dict
        dicti = {
            '2023': "select * from entry where YEAR(Date)=2023;",
            '2024': "select * from entry where YEAR(Date)=2024;",
            'Online': "select * from entry where Mode=False order by Date desc;",
            'Offline': "select * from entry where Mode=True order by Date desc;",
            'amount+': "select * from entry where Amount>0 order by Date desc;",
            'amount-': "select * from entry where Amount<0 order by Date desc;",
            'amount+desc': "select * from entry where Amount>0 order by Amount desc;",
            'amount-desc': "select * from entry where Amount<0 order by Amount;"
        }
        # making combo-box
        filters = ['2023','2024','Online','Offline','amount+','amount-','amount+desc','amount-desc']
        filter_value = tk.StringVar(value="Filters")
        combo = ttk.Combobox(add_f2, textvariable=filter_value)
        combo['values'] = filters
        combo.pack(side='left')
        combo.bind('<<ComboboxSelected>>', lambda event:self.show_data(dicti[filter_value.get()]))

        type_combo = ttk.Combobox(add_f2)
        type_combo['values'] = types
        type_combo.set("Type Filters")
        type_combo.pack(side='left')
        type_combo.bind('<<ComboboxSelected>>',
                        lambda event: self.show_data(
                            f"select * from entry where Type='{type_combo.get()}' order by Date desc;"))

        # Creating tree view(Table) and setting initial properties of it
        self.tree = ttk.Treeview(self, columns=('sno', 'date', 'note', 'category', 'amount'), show='headings', height=5)
        self.tree.column("sno", width=50)
        self.tree.column("date", width=95)
        self.tree.column('note', width=210)
        self.tree.heading('sno', text='SNo.')
        self.tree.heading('date', text='Date')
        self.tree.heading('note', text='Note')
        self.tree.heading('category', text='Category')
        self.tree.heading('amount', text='Amount')
        self.tree.pack(expand=True,fill='both',padx=9, pady=9)
        ttk.Style().configure('Treeview', rowheight=28)
        self.tree.tag_configure("colour_blue", foreground="blue")
        self.tree.tag_configure("tree_font", font='None 13')

        self.show_data("select * from entry order by Date desc;")

    # This function takes sql query and display one-by-one in tree view
    def show_data(self, query):
        self.tree.delete(*self.tree.get_children())
        courser.execute(query)
        i = 1
        for t in courser:
            old_date = str(t[1])
            new_date = old_date[8:]+"/"+old_date[5:7]+"/"+old_date[0:4]
            row = (i, new_date, t[2], t[3], t[5])
            if t[4]: self.tree.insert('', 'end', values=row, tags=('colour_blue',"tree_font",))
            else: self.tree.insert('', 'end', values=row, tags=("tree_font",))
            i += 1

    # This function takes few data from placeholders of add_f1 and runs sql query for insertion.
    def add_data(self, date_value, note_value, type_value, mode_value, amount_value):
        courser.execute(f"insert into entry values({self.no.get()},STR_TO_DATE('{date_value.get()}', '%d/%m/%Y'),"
                        f"'{note_value.get()}','{type_value.get()}',{mode_value.get()},{amount_value.get()});")
        db.commit()
        self.no.set(self.no.get() + 1)
        self.show_data("select * from entry order by Date desc;")


# This class is for analyzing the data.
class Analyse(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ttk.Label(self, text="Analyzing Page", font=('Times', '20'))
        frame3 = ttk.Frame(self)
        label.pack()
        frame3.pack()
        dect = {
            "food":"select Amount from entry where Type ='food' order by Date;",
            "small entries":"select Amount from entry where Amount>-500 and Amount<500 order by Date;",
            "all entries":"select Amount from entry order by Date;"
        }
        ttk.Button(frame3, command=lambda: self.clear_graph(), text="Clear Graph").pack()
        box1 = ttk.Button(frame3, text="food", command=lambda: self.graph(dect.get("food"), "food"))
        box2 = ttk.Button(frame3, text="small entries", command=lambda: self.graph(dect.get("small entries"),"small entries"))
        box3 = ttk.Button(frame3, text="all entries", command=lambda: self.graph(dect.get("all entries"),"all entries"))
        box1.pack(side='left')
        box2.pack(side='left')
        box3.pack(side='left')

        self.fig = Figure(figsize=(7, 6), dpi=110)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand=True,fill='both',padx=20, pady=20)
        self.plt = self.fig.add_subplot(111)

    def clear_graph(self):
        self.fig.clf()
        self.plt = self.fig.add_subplot(111)
        self.canvas.draw()

    def graph(self, query, legend):
        courser.execute(query)
        x_axis, values = [], []
        data = courser.fetchall()
        x_axis = [i for i in range(len(data))]
        for t in data: values.append(t[0])

        self.plt.plot(x_axis, values, label=legend)
        self.plt.set_title("Graph")
        self.plt.set_ylabel("Amount")
        self.plt.set_xlabel("Entries")
        self.plt.legend()
        self.canvas.draw()


# The program starts its execution from here, connection is established with database.
# for security purposes host, password, user and database name is removed.
if __name__ == "__main__":
    db = mysql.connector.connect(host='localhost', password='12345akshat', user='root', database="money")
    courser = db.cursor()
    if db.is_connected(): print("Connection successfully...")
    app = App()
    app.mainloop()
    db.close()