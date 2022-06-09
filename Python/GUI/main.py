# This is a sample Python script.
import PySimpleGUI as sg

#This imports for OS commands
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
sg.theme('DarkAmber')

layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Button('Launch')]
        ]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the Window
    window = sg.Window('AstroAccelerate -- Simple GUI -- testing ', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == 'Launch':
            cmd = 'ls -l'
            os.system(cmd)
            print("Starting AstroAccelerate")
        print('You choose event', event)
        print('You entered ', values[0])

    window.close()
