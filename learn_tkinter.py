from tkinter import *
'''
root = Tk()

myContainer1 = Frame(root)  ### (1)
myContainer1.pack()         ### (2)

button1 = Button(myContainer1)
button1['text'] = 'Hello'
button1['background'] = 'green'
button1.pack()

root.mainloop()
'''


class MyApp:
    def __init__(self,myParent):
        self.myContainer1 = Frame(myParent)
        self.myContainer1.pack()

        self.button1 = Button(self.myContainer1)
        self.button1['text'] = 'Hello'
        self.button1['background'] = 'green'
        self.button1.pack()

        self.button2 = Button(self.myContainer1)
        self.button2.configure(text="Off to join the circus!")  ### (2)
        self.button2.configure(background="tan")  ### (2)
        self.button2.pack()

        self.button3 = Button(self.myContainer1)
        self.button3.configure(text='Join me',background='cyan')
        self.button3.pack()


root = Tk()
myapp = MyApp(root)
root.mainloop()