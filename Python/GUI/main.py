# This is a sample Python script.
import PySimpleGUI as sg

#This imports for OS commands
import os
from aa_plot import *
from aa_tools import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import glob

matplotlib.use('TkAgg')

sg.theme('DarkAmber')

plot1 = None

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

###### DM survey plan Group #############
heading_ranges_labels = ['Range', 'From', 'To', 'DM_Step', 'Binning']
input_DMrow = [
    [sg.Text("Range " + str(row), pad=(1,0),size=(7,1))] +
    [sg.Input(size=(8,1), pad=(1,0),key=f'-{heading_ranges_labels[col+1]}{row}-', default_text=defaul_ranges[row][col])
     for col in range(len(heading_ranges_labels)-1)]
        for row in range(number_of_ranges)
]
#########################################

############### Component #################
aa_component = [
    [
        sg.Checkbox("Analysis", default=False, key='-com_analysis-', size=(12,1)),
        sg.Checkbox("Zero DM", default=False, key='-com_zero-', size=(12,1))
    ],
    [
        sg.Checkbox("Acceleration", default=False, key='-com_acceleration-', size=(12,1)),
        sg.Checkbox("Periodicity", default=False, key='-com_periodicity-', size=(12,1))
    ]
]

#########################################

########## user tab group
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
            [sg.Frame("Components:", aa_component)
             ],
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
            [sg.Text(key="-plot_text-",text="No analysis done. Click to Launch button.")],
#            [sg.Text(size=(40, 1), key="-TEXT-")],
            [sg.Canvas(key="-IMAGE-")]
        ]
##############################


#### plot tab #############
std_output_tab = [
#    [sg.Multiline(size=(110, 30), key="-multi-", reroute_stdout=False)],
    [sg.Canvas(key="-IMAGE2-")]
]
#############################

### user tab ###
tab_user = [[
                sg.Column(left_layout),
                sg.VSeparator(),
                sg.Column(right_layout)
]]
################

################## final layout #########################
layout = [
            [
                sg.TabGroup(
                    [[sg.Tab("Setup", tab_user),
                      sg.Tab("Graph plots", std_output_tab)
                    ]]
                )
            ]
         ]
##############################################################

def status_print(status):
    print(status)

def plot_graph(candidates):
    x = list(zip(*candidates))[0] # dm channel
    y = list(zip(*candidates))[1] # time
    z = list(zip(*candidates))[2] # SNR
    pw = list(zip(*candidates))[3] # pulse width 
    final = fig_3d.add_subplot(projection='3d')
    final.scatter(y, x, z, c = z, cmap='coolwarm')
    final.set_xlabel('Time')
    final.set_ylabel('DM Channel')
    final.set_zlabel('SNR')

    final1 = fig_all.add_subplot(241)
    final1.scatter(y, x, c = pw, cmap='coolwarm')
    final1.set_xlabel('Time')
    final1.set_ylabel('DM channel')

    final2 = fig_all.add_subplot(242)
    final2.hist(x)
    final2.set_xlabel('DM Channel')
    final2.set_ylabel('# Candidates')
#   final2.scatter(hist1)
#   final2.set_xlabel('DM Channel')

    final3 = fig_all.add_subplot(243)
    final3.scatter(x, z, c = pw, cmap='coolwarm')
    final3.set_xlabel('DM Channel')
    final3.set_ylabel('SNR')

    final4 = fig_all.add_subplot(244)
    final4.hist(z)
    final4.set_xlabel('SNR')
    final4.set_ylabel('# Candidates')

    final5 = fig_all.add_subplot(212)
    final5.scatter(y, x, c = z, cmap='coolwarm')
    final5.set_xlabel('Time')
    final5.set_ylabel('DM channel')

#    fig_all.tight_layout()

#    axs[0].set_xlabel('test')
#    axs[1].scatter(y, x, z, c = z, cmap='coolwarm')
    #fig.add_subplot(111, projection='3d').scatter(x, y, z)


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
    if (values['-com_analysis-'] == True):
        f.write("analysis" + "\n")
    f.write(f_append.read())
    f.write("file" + "\t" + values['-filterbank-'])
    f.close()
    f_append.close()
    #print('You entered ', values['from0'], values['to0'], values['dmstep0'])

def AstroAccelerate_run():
    cmd = './astro-accelerate astroaccelerate_input_file.txt' #'./astro-accelerate ska_test_file-small.txt'
    AA_return_value = os.system(cmd)
    print("\nAstroAccelerate finished with exit code: ", AA_return_value)

def AstroAccelerate_launch():
    status = "Create AA input file"
    status_print(status)
    print("Starting AstroAccelerate")
    create_input_files()
    status = "Starting AA"
    status_print(status)
#    AstroAccelerate_run()
    analysed_file_data = sorted(glob.glob("*ana*.dat"))
    candidates = read_file_analysis(analysed_file_data)
    plot_graph(candidates)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#    figure_canvas_agg.get_tk_widget().place(anchor='center')
    return figure_canvas_agg


fig_all = matplotlib.figure.Figure(figsize=(8, 5), tight_layout=True, dpi=120)
fig_3d =  matplotlib.figure.Figure(figsize=(5, 5), dpi=120)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the Window
    window = sg.Window('AstroAccelerate -- Simple GUI -- testing ', 
                        layout,
                        resizable=True,
                        element_justification="right")#.Finalize()
#    window['-multi-'].reroute_stdout_to_here()
#   window.Maximize()
#    fig_canvas_agg = draw_figure(window['-IMAGE-'].TKCanvas, fig)

    while True:
        event, values = window.read()
        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Launch':
            AstroAccelerate_launch()
            if plot1 is not None:
                print("plot  1 none")
                plot1.get_tk_widget().forget()
                plot2.get_tk_widget().forget()
#                fig3d_all.clf()
            plot1 = draw_figure(window['-IMAGE-'].TKCanvas, fig_3d)
            plot2 = draw_figure(window['-IMAGE2-'].TKCanvas, fig_all)
            window['-plot_text-'].update('Analysis done.')
        if event == 'Ok':
            print("Ahoj" + values['-From0-'])

    window.close()


