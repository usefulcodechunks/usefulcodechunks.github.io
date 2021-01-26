from tkinter import *
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import functions as fs

def analyze(event):
 
    count = 0
    for key in inputmapping:
        inputmapping[key] = float(entries[count].get())
        count += 1
    results, graph = fs.analysis(inputmapping)

    #outputdata = fs.otherdata(inputmapping)

    count = 0
    for fillin in resultsid:
        fillin["text"]=results[count]
        count += 1

        #[xl,yl,dl,radl,timel,mos]
        # 0  1   2  3    4    5


    plot = Figure(figsize=(5,2.7), dpi=100)

    a = plot.add_subplot(1,2,1)
    a.scatter(graph[4],graph[5],c=graph[5])
    a.set_title('Time VS DL (Color=MOS)')
    a.set_ylabel('MOS DL (dB)')
    a.set_xlabel('Time (hrs)')
    a.grid(True)


    a3 = plot.add_subplot(1,2,2)
    a3.scatter(graph[0],graph[1],c=graph[5])
    a3.set_title('Earth at 0,0 (Color=MOS)')
    #a3.set_ylim(-.003,.003)
    #a3.set_xlim(-.003,.003)


    a3.set_ylabel('Y (AU)')
    a3.set_xlabel('X (AU)')
    a3.grid(True)



    plot.tight_layout()
    canvas = FigureCanvasTkAgg(plot, f2)
    canvas.get_tk_widget().grid(row=rowcount+1, column=0,columnspan=3)


    # f3 = Frame(root, bg = "yellow")
    # f3.grid(row=0,column=2,sticky=N)
    # plot = Figure(figsize=(5,5), dpi=100)
    # a = plot.add_subplot(1,2,1)
    # a.scatter(graph[4],graph[5],c=graph[5])
    # a.set_ylabel('MOS (dB)')
    # a.set_xlabel('Time (s)')
    # a.grid(True)
    #
    # a2 = plot.add_subplot(1,2,2)
    # a2.scatter(graph[0],graph[1],c=graph[5])
    # a2.set_ylabel('Y Distance')
    # a2.set_xlabel('X Distance')
    # a2.grid(True)
    #
    #
    # canvas = FigureCanvasTkAgg(plot, f3)
    # canvas.get_tk_widget().grid(row=0, column=0)

def standardmoon(event):

    stconds = [8450000000,100000000,150,380,405400000,362600000,0.0549006,27.32200231,2123366400,86400,2123366400,86400,56.7,90]

    count = 0
    for ent in entries:
        ent.delete(0,END)
        ent.insert(0,stconds[count])
        count += 1



root = Tk()

# Inputs Frame
f = Frame(root, bg = "grey", width = 200, height = 500)
f.grid(row=0,column=0,sticky=N)

inputmapping = {"f":0,"b":0,"tsr":0,"tst":0,"dmax":0,"dmin":0,"e":0,"period":0,"packsize":0,"mintran":0,"uppack":0,"uptrans":0,"gr":0,"eirp":0}

inputs = ["Channel Information","Frequency (Hz)","Bandwidth","System Temperature","Receiver Sys Temp (K)","Transmitter Sys Temp (K)"]
inputs = inputs + ["Orbit Information","Max Distance (m)","Min Distance (m)","Eccentricity","Orbit Period (days)","Data Downlink Information","Package Downlink (bits)"]
inputs = inputs + ["Min Transmission DL Time(s)","Package Uplink (bits)","Min Transmission UP Time(s)","Receiver","Gain Receiver (dBi)","EIRP (dBW)"]
entries = []

titlecards = [0,3,6,11,16]

title  = Label(master=f,text="Inputs",foreground="black",background="#0076bf",width=48,relief=SOLID,borderwidth=0.1411764705882353)
title.grid(row=0, column=0,sticky = W,columnspan = 2)

count = 1
for textsele in inputs:
    tempspan = 1
    tempwidth = 23
    temprelief = SOLID
    tempbg = "white"
    if((count-1) in titlecards):
        tempspan = 2
        tempwidth = 48
        temprelief = FLAT
        tempbg = "#5ec1ff"

    temptext  = Label(master=f,text=textsele,foreground="black",background=tempbg,width=tempwidth,borderwidth=0.1411764705882353,relief=temprelief)
    temptext.grid(row=count, column=0,sticky = W,columnspan = tempspan)

    if(tempspan != 2):
        tempentr = Entry(master=f,fg="black",width=25)
        tempentr.grid(row=count, column=1,sticky = W)
        entries.append(tempentr)

    count += 1

exec = Button(master=f,text="Run Analysis",width=49,height=5,bg="#413e57",fg="white",borderwidth=5,relief=FLAT)
exec.grid(row=count+1, column=0,sticky = W,columnspan = 2)
dummyvals = Button(master=f,text="Set Standard Values",width=49,height=2,bg="grey",fg="white",borderwidth=5,relief=FLAT)
dummyvals.grid(row=count+2, column=0,sticky = W,columnspan = 2)

exec.bind("<Button-1>",analyze)
dummyvals.bind("<Button-1>",standardmoon)


# Plots and Performance Metrics
f2 = Frame(root, bg = "black", height=500, width = 500)
f2.grid(row=0,column=1,sticky=N)

root.update()

secondpanelwidth = int(f2.winfo_width()*.1411764705882353)


res  = Label(master=f2,text="Results Downlink",foreground="black",background="#379e00",width=secondpanelwidth+2,relief=SOLID,borderwidth=0.1411764705882353)
res.grid(row=0, column=0,sticky = W,columnspan = 3)

results = [1,2,3,4,5,6,7,8,9,10,11,12,13]
resultsid = []
rowcount = 1
colcount = 0
tempcolor = "#6fc93e"
for answer in results:
    tcs = 1

    if(answer != 7):
        templabel = Label(master=f2,text=answer,foreground="black",background=tempcolor,height = 3,width=int(secondpanelwidth/3),relief=SOLID,borderwidth=1)
        templabel.grid(row=rowcount,column=colcount)
        resultsid.append(templabel)
    else:
        res2  = Label(master=f2,text="Results Uplink",foreground="black",background="#ad0722",width=secondpanelwidth+2,relief=SOLID,borderwidth=0.1411764705882353)
        res2.grid(row=rowcount, column=0,sticky = W,columnspan = 3)
        rowcount += 1
        colcount += -1
        tempcolor = "#c93e55"

    colcount += 1
    if(colcount == 3):
        colcount = 0
        rowcount += 1


root.update()





root.mainloop()
