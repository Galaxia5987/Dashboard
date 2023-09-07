import PySimpleGUI as sg


def your_mom():
    print("hey")


button = sg.Button(button_text="Hey", button_type=9)
window = sg.Window("Your mom", layout=[[button]], margins=(400, 200))

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    print(event)

window.close()



