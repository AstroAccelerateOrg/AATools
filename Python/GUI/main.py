# This is a sample Python script.
import PySimpleGUI as sg

#This imports for OS commands
import os

sg.theme('DarkAmber')

# number of ranges for the plan
number_of_ranges = 3

# default example of SKA DM survey plan
defaul_ranges = [ [0,150,0.1,1],
                  [150,300, 0.2,1],
                  [300, 500, 0.25, 1],
                  [500, 900, 0.4, 2],
                  [900, 1200, 0.6, 4],
                  [1200, 1500, 0.8, 4],
                  [1500, 2000, 1.0, 4],
                  [2000, 3000, 2.0, 8]
]

heading_ranges_labels = ['Range', 'From', 'To', 'DM_Step', 'Binning']
input_DMrow = [
    [sg.Text("Range " + str(row), pad=(1,0),size=(7,1))] +
    [sg.Input(size=(8,1), pad=(1,0),key=f'-{heading_ranges_labels[col+1]}{row}-', default_text=defaul_ranges[row][col])
     for col in range(len(heading_ranges_labels)-1)]
        for row in range(number_of_ranges)
]

std_output_tab = [
    [sg.Multiline(size=(110, 30), key="-multi-", reroute_stdout=True)]
]

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


left_layout = [  [
             sg.Text('Select filterbank: '), 
             sg.Input(size=(30,1),
                      key="-filterbank-",
                      default_text="/home/jnovotny/filterbanks/ska-mid-b2-small.fil"), 
             sg.FileBrowse(key='-filterbankbrowse-',
                            initial_folder="/home/jnovotny/filterbanks/")
            ],
            [sg.Frame("DM plan:", [
                [sg.Text(h, size=(7,1), pad=(1,0), justification="left") for h in heading_ranges_labels],
                [sg.Column(input_DMrow,pad=(1,0))]
                ])],
            [
             sg.Text(size=(40,1), 
                     key='-OUTPUT-')
            ],
            [
             sg.Button('Ok'), 
             sg.Button('Cancel')
            ],
            [sg.Button('Launch')],
            [sg.Output(size=(60,15))]
        ]

right_layout = [
            [sg.Text("Choose an image from list on left:")],
            [sg.Text(size=(40, 1), key="-TEXT-")],
            [sg.Image(key="-IMAGE-")]
        ]

tab_user = [[
                sg.Column(left_layout),
                sg.VSeparator(),
                sg.Column(right_layout)
]]

layout = [
            [
                sg.TabGroup(
                    [[sg.Tab("Setup", tab_user),
                      sg.Tab("Output LOG", std_output_tab)
                    ]]
                )
            ]
         ]

def status_print(status):
    print(status)

def create_input_files():
    f = open("astroaccelerate_input_file.txt","w")
    f_append = open("minimal_input_file.txt", "r")
    for rows in range(number_of_ranges):
        f.write("range\t" +
                values[f'-From{rows}-'] + "\t" +
                values[f'-To{rows}-'] + "\t" +
                values[f'-DM_Step{rows}-'] + "\t" +
                values[f'-Binning{rows}-'] + "\t" +
                values[f'-Binning{rows}-'] + "\n"
        )
    f.write(f_append.read())
    f.write("file" + "\t" + values['-filterbank-'])
    f.close()
    f_append.close()
    #print('You entered ', values['from0'], values['to0'], values['dmstep0'])

def AstroAccelerate_launch():
    status = "Create AA input file"
    status_print(status)
    print("Starting AstroAccelerate")
    create_input_files()
    status = "Starting AA"
    status_print(status)
    cmd = './astro-accelerate astroaccelerate_input_file.txt' #'./astro-accelerate ska_test_file-small.txt'
    AA_return_value = os.system(cmd)
    print("\nAstroAccelerate finished with exit code: ", AA_return_value)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the Window
    window = sg.Window('AstroAccelerate -- Simple GUI -- testing ', layout).Finalize()
#   window.Maximize()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == 'Launch':
            AstroAccelerate_launch()
        if event == 'Ok':
            print("Ahoj" + values['-From0-'])
        #window['-OUTPUT-'].update("Range 0: " + values['-from0-'] +
        #        " to " + values['-to0-'] +
        #        " with DM step " + values['-dmstep0-'], text_color='red')

    window.close()


