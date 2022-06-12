# This is a sample Python script.
import PySimpleGUI as sg

#This imports for OS commands
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
sg.theme('DarkAmber')

layout = [  [sg.Text('Select filterbank: '), sg.Input(size=(30,1)), sg.FileBrowse(key='filterbank')],
            [sg.Text('DM trials range')],
            [sg.Text('from: '), sg.InputText(size=(6,1),key="from0"), 
             sg.Text('to: '),   sg.InputText(size=(6,1),key="to0"), 
             sg.Text('with DM step'), sg.InputText(size=(6,1),key="dmstep0")
            ],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Button('Launch')]
        ]

def create_input_files():
    f = open("astroaccelerate_input_file.txt","w")
    f.write("range\t" + 
            values['from0'] + "\t" + 
            values['to0'] + "\t" +
            values['dmstep0'] + "\n"
            )
    f.write("file" + "\t" + values['filterbank'])
    f.close()
    #print('You entered ', values['from0'], values['to0'], values['dmstep0'])


def AstroAccelerate_launch():
    status = "Create AA input file"
    print("Starting AstroAccelerate")
    create_input_files()
    status = "Starting AA" 
    cmd = 'cat astroaccelerate_input_file.txt' #'./astro-accelerate ska_test_file-small.txt'
    AA_return_value = os.system(cmd)
    print("\nAstroAccelerate finished with exit code: ", AA_return_value)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the Window
    window = sg.Window('AstroAccelerate -- Simple GUI -- testing ', layout) #.Finalize()
#   window.Maximize()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == 'Launch':
            AstroAccelerate_launch()
        window['-OUTPUT-'].update("Range 0: " + values['from0'] + 
                " to " + values['to0'] + 
                " with DM step " + values['dmstep0'], text_color='red')

    window.close()
