import math
import random

kb = 1.38 * 10**-23 # Boltzman Constant

def prop(powertrans,gaint,distance,atmosloss,elloss,wavelength,bitrate,tsys,gainr,bandwidth,bitratepercent):
    return {"b":bandwidth,"pt":powertrans,"gt":gaint,"d":distance,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsys,"gr":gainr,"brper":bitratepercent}

def outputptgtcoeff(parameters):
    res = 0
    res += -parameters["gr"]
    res += -parameters["la"]
    res += -parameters["ll"]
    res += 10 * math.log10(1/((parameters["wl"]/(4 * math.pi * parameters["d"]))**2))
    res += (10 * math.log10(kb*parameters["tsys"]*parameters["rb"]))
    return res

def minptgt(parameters):
    ptgtcoff = 10**(outputptgtcoeff(parameters) /10)        # Normal units
    shnnorm = 10**(shannonlimit(parameters)/10)    # Normal Units
    res = 2 * ptgtcoff * shnnorm
    return 10 * math.log10(res)

def setrb(parameters):
    maxx = maxbitrate(parameters)
    parameters["rb"] = maxx * parameters["brper"]
    return parameters

def outputebno(parameters):
    res = 0
    res += parameters["pt"]
    res += parameters["gt"]
    res += parameters["gr"]
    res += parameters["la"]
    res += parameters["ll"]
    res += 10 * math.log10((parameters["wl"]/(4 * math.pi * parameters["d"]))**2)
    res += -1*(10 * math.log10(kb*parameters["tsys"]*parameters["rb"]))
    return res

def outputsno(parameters):
    res = 0
    res += parameters["pt"]
    res += parameters["gt"]
    res += parameters["gr"]
    res += parameters["la"]
    res += parameters["ll"]
    res += 10 * math.log10((parameters["wl"]/(4 * math.pi * parameters["d"]))**2)
    res += -1*(10 * math.log10(kb*parameters["tsys"]*parameters["b"]))
    return res


def shannonlimit(pa):
    speceff = pa["rb"]/pa["b"]
    try:
        minebno = ((2**speceff)-1)/speceff
    except:
        print(speceff)
        print(pa)
    return 10 * math.log10(minebno)

def maxbitrate(pa):
    res = pa["b"] * math.log2(1+(10**(outputsno(pa)/10)))
    return res

def speceff(pa):
    return pa["rb"]/pa["b"]

def marginofsafe(pa):
    return outputebno(pa)-shannonlimit(pa)

def transmissiontime(pa,totalpackage):
    return totalpackage/pa["rb"]
def strengthofantenna(pa):
    return pa["gt"]+pa["pt"]



def orbitinformation(info,rad):
    dmin = -1*info["dmin"]
    dmax = info["dmax"]
    centerx = (dmin+dmax)/2
    cal = centerx
    e = info["e"]
    b = math.sqrt(((cal/e)**2)-(cal**2))
    a = centerx - dmin

    maxtime = info["period"] * 60 * 60 * 24 # to seconds
    slope = maxtime/(2*3.14)
    time = rad * slope

    def ellipsexy(rad):
        tr = rad
        x = elipx(tr)
        y = elipy(tr)
        return x, y

    def ellipsedistance(rad):
        # time in seconds
        x, y = ellipsexy(rad)
        distance = math.sqrt((x**2) + (y**2))
        return distance

    def elipx(rad):
        x = centerx + (a * math.cos(rad))
        return x

    def elipy(rad):
        y = b * math.sin(rad)
        return y

    x, y = ellipsexy(rad)
    distance = ellipsedistance(rad)

    return x, y, distance, time



def otherdata(info):
    bitrate = info["packsize"]/info["mintran"] #bits/sec
    bandwidth = info["b"]
    gainr = info["gr"]
    tsys = info["tsr"]
    dmax = info["dmax"]
    dmin = info["dmin"]

    wavelength = 299792458 / info["f"]

    elloss = -3
    atmosloss = -2

    papeak = {"b":bandwidth,"pt":0,"gt":0,"d":dmax,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsys,"gr":gainr,"brper":0}
    pamin = {"b":bandwidth,"pt":0,"gt":0,"d":dmin,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsys,"gr":gainr,"brper":0}

    minptgtpa = minptgt(papeak)

    bitrate = info["uppack"]/info["uptrans"]
    tsysn = info["tst"]
    gainr = gttemp
    powerr = info["eirp"] - info["gr"]
    paupmax = {"b":bandwidth,"pt":powerr,"gt":info["gr"],"d":dmax,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsysn,"gr":gttemp,"brper":0}
    paupmin = {"b":bandwidth,"pt":powerr,"gt":info["gr"],"d":dmin,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsysn,"gr":gttemp,"brper":0}





def analysis(info):
    bitrate = info["packsize"]/info["mintran"] #bits/sec
    bandwidth = info["b"]
    gainr = info["gr"]
    tsys = info["tsr"]
    dmax = info["dmax"]
    dmin = info["dmin"]

    wavelength = 299792458 / info["f"]

    elloss = -3
    atmosloss = -2

    papeak = {"b":bandwidth,"pt":0,"gt":0,"d":dmax,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsys,"gr":gainr,"brper":0}
    pamin = {"b":bandwidth,"pt":0,"gt":0,"d":dmin,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsys,"gr":gainr,"brper":0}


    minptgtpa = minptgt(papeak)

    pttemp = random.randint(-20,int(minptgtpa))
    gttemp = minptgtpa - pttemp
    papeak["pt"] = pttemp
    papeak["gt"] = gttemp
    pamin["pt"] = pttemp
    pamin["gt"] = gttemp

    # print(papeak)

    sysp = outputebno(papeak)
    sysshnp = shannonlimit(papeak)
    mosp = sysp - sysshnp

    sysm = outputebno(pamin)
    sysshnm = shannonlimit(pamin)
    mosm = sysm - sysshnm

    # print("Min EIRP for system (dB): ",minptgtpa)
    # print("\nAt Max Distance----------------------")
    # print("Sys Max ",sysp)
    # print("Shn Max ",sysshnp)
    # print("Min MOS at max : ",mosp)
    # print("\nAt Min Distance----------------------")
    # print("Sys Max ",sysm)
    # print("Shn Max ",sysshnm)
    # print("Max MOS at min : ",mosm)

    results = ["Min EIRP (dB): "+str(round(minptgtpa,2)),"Min MOS (dB): "+str(round(mosp,2)),"Max MOS (dB): "+str(round(mosm,2))]
    results = results + ["Downlink Speed (s): "+str(round(info["mintran"],2))]
    results = results + ["Downlink Speed (days): "+str(round(info["mintran"]/(60*60*24),2))]
    results = results + ["Bit Rate (bit/s): "+str(round(bitrate,2))]


    bitrate = info["uppack"]/info["uptrans"]
    tsysn = info["tst"]
    gainr = gttemp
    powerr = info["eirp"] - info["gr"]
    paupmax = {"b":bandwidth,"pt":powerr,"gt":info["gr"],"d":dmax,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsysn,"gr":gttemp,"brper":0}
    paupmin = {"b":bandwidth,"pt":powerr,"gt":info["gr"],"d":dmin,"la":atmosloss,"ll":elloss,"wl":wavelength,"rb":bitrate,"tsys":tsysn,"gr":gttemp,"brper":0}

    sysp = outputebno(paupmax)
    sysshnp = shannonlimit(paupmax)
    mosp = sysp - sysshnp

    sysm = outputebno(paupmin)
    sysshnm = shannonlimit(paupmin)
    mosm = sysm - sysshnm

    results2 = ["EIRP (db): "+str(info["eirp"]),"Min MOS (dB): "+str(round(mosp,2)),"Max MOS (dB): "+str(round(mosm,2))]
    results2 = results2 + ["Uplink Speed (s): "+str(round(info["uptrans"],2))]
    results2 = results2 + ["Downlink Speed (days): "+str(round(info["uptrans"]/(60*60*24),2))]
    results2 = results2 + ["Bit Rate (bit/s): "+str(round(bitrate,2))]

    xl = []
    yl = []
    mosl = []
    mosul = []
    dl = []
    radl = []
    timel = []
    for t in range(100):
        rad = (2*3.14) * (t/100)
        tx, ty, td, tt = orbitinformation(info,rad)
        papeak["d"] = td
        paupmax["d"] = td
        tempmos = outputebno(papeak) - shannonlimit(papeak)
        tempmos2 = outputebno(paupmax) - shannonlimit(paupmax)
        xl.append(tx*(0.00000000000668459))
        yl.append(ty*(0.00000000000668459))
        dl.append(td*(0.00000000000668459))
        mosl.append(tempmos)
        mosul.append(tempmos2)
        timel.append(tt/(60*60))
        radl.append(rad)

    graph = [xl,yl,dl,radl,timel,mosl,mosul]

    return results + results2, graph
