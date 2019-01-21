from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.geometry('600x600')
canvas = Canvas(root, width=999, height=999)
canvas.pack()
pilImage = Image.open("pic/tank0.png")
image = ImageTk.PhotoImage(pilImage)
sprites = []
for i in range(6):
    sprite = canvas.create_image(image.width()//2 + 80*i,
                                 image.height()//2 + 40*i, image=image)
    sprites.append(sprite)

root.mainloop()
