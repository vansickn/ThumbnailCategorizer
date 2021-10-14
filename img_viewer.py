from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os


class imgViewer:

    def __init__(self, img_path) -> None:
        self.img_path = img_path
        self.face = True
        self.ws = Tk()
        self.canvas = None
        self.top_head = None
        self.bottom_chin = None
        self.bottom_torso = None

    def createFrame(self):

        self.ws.title('PythonGuides')
        self.ws.geometry('600x300')

        self.canvas = Canvas(
            self.ws,
            width=700,
            height=700
        )
        self.canvas.pack()
        img = ImageTk.PhotoImage(Image.open(self.img_path))
        self.canvas.create_image(
            10,
            10,
            anchor=NW,
            image=img
        )
        self.canvas.bind("<Button-1>", self.callback)

        button_no_face = ttk.Button(text="No Face!", command=self.no_face)
        button_no_face.place(x=10, y=230)
        button_no_face = ttk.Button(
            text="Retry Face Points", command=self.retry)
        button_no_face.place(x=100, y=230)
        button_no_face = ttk.Button(
            text="Done With Face Points", command=self.submit)
        button_no_face.place(x=240, y=230)
        self.canvas.create_text(480, 10, fill="darkblue", font="Times 20 italic bold",
                                text="Click the Top of the Face")
        self.ws.mainloop()

    def no_face(self):
        self.face = False
        self.ws.destroy()

    def submit(self):
        self.ws.destroy()

    def get_face_points(self):
        package = [self.top_head, self.bottom_chin, self.bottom_torso]
        return package

    def retry(self):
        self.top_head = None
        self.bottom_chin = None
        self.bottom_torso = None

    def face_exists(self):
        return self.face

    def callback(self, event):
        print(event.x)
        print(event.y)
        if self.top_head == None:
            self.canvas.create_oval(event.x-2.5, event.y-2.5, event.x + 2.5,
                                    event.y + 2.5, outline="#f11", fill="#1f1", width=2)
            self.top_head = (event.x, event.y)
            self.canvas.create_text(480, 30, fill="darkblue", font="Times 20 italic bold",
                                    text="Now Click Bottom Chin")
        elif self.bottom_chin == None:
            self.canvas.create_oval(event.x-2.5, event.y-2.5, event.x + 2.5,
                                    event.y + 2.5, outline="#f11", fill="#00FF00", width=2)
            self.bottom_chin = (event.x, event.y)
            self.canvas.create_text(480, 50, fill="darkblue", font="Times 20 italic bold",
                                    text="Now Click Bottom Torso")
        elif self.bottom_torso == None:
            self.canvas.create_oval(event.x-2.5, event.y-2.5, event.x + 2.5,
                                    event.y + 2.5, outline="#f11", fill="#1f1", width=2)
            self.bottom_torso = (event.x, event.y)
