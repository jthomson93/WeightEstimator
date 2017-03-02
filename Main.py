#----------------------------------------
# PYTHON BASED WING SIZING PROGRAMME
# Developed by James Thomson for SWIFT
#----------------------------------------

import math

#---------------------------
# Enter your variables here
#---------------------------

b = 16.995                                          # Wing Span [Perpendicular to fuselage]
cr = 6.074080                                       # Root Chord
ct = 1.4955                                         # Tip Chord
bst = 0.0                                           # Structural Wingspan [Can be left 0 and calculated internally]
c = 3.7574                                          # Average Chord
tc = 0.1175                                         # Thickness chord ratio
Lh = 27.42                                          # Sweep angle of mid-chord line
ke = 1.00                                           # Engine mounting [1.0 = Not wing mounted, 0.95 = Two wing mounted, 0.90 = Four wing mounted]
kuc = 1.0                                           # Under-carridge location
l12 = 27.42                                         # Sweep angle of mid chord line
sweep = 27.1                                        # Sweep angle of leading edge
wdes = 73315                                         # Design All-Up weight of aircraft
tc_root = 0.1515                                    # Thicnkesss chord ratio at the root

#---------------------------
# Torenbeek Constant
#---------------------------

constant = 4.58 * (10 ** -3)
flutConst = 9.06 * (10 ** -4)
nnult = 1.5 * (2.1 + (24000/(172000+10000)))        # Ultimate load factor [Initial estimation] [Described as Nult >= 1.5Bn]
kw = (6.67 * (10 ** -3))                            # Torenbeek factor of proprotionality relative to aircraft size
bref = 1.905
kb = 1.0                                            # Correction factor due to strut placement [1.0 for cantileaver]
Ww = 10.613 * (10 ** 3)

#------------------------------
# Referenced from similar ACF
#------------------------------
tr = 2.1                                            # Max thickness at root (Boeing 737 Aerofoil based on A320 chord)
S = 61.2                                           # Projected Surface Area (A320)
WG = 73315                                          # Gross weight
VD = 196                                            # Design dive speed Vd [From A320 POH] [FCB-FBC15 P 1/2 - 07 APR 11]
Wzf = 120621        # POUNDS                        # Zero Fuel Weight


lambdahalf = math.radians(l12)


def structbs():
    return (b / math.cos(lambdahalf))


def correctionfactors():

    bs = structbs()                                     # Calculating the structural wing span
    kno = (1 + math.sqrt(bref/bs))                      # Weight penalties due to skin joints
    lamb = ct/cr                                        # Taper ratio

    klamb = (1 + lamb) ** 0.4
    kst = 1 + flutConst * (((b * math.cos(math.radians(sweep))) ** 3) / wdes) * (((VD/100)/tc_root) ** 2) * math.cos(lambdahalf)
    return kno * klamb * ke * kuc * kst


def initialprediction():
    return (((kw)*(structbs()) ** 0.75) * (1 + math.sqrt(bref / structbs())) * (nnult ** 0.55) * ((structbs()/tr) / (WG/S)) ** 0.30) * WG



def guessweight():
    return (((structbs()/tr)/(WG/S)) ** 0.30)


def finalprediction():
    total = constant * correctionfactors()
    total = total * ((kb * nnult * (wdes-0.8*(initialprediction()))) ** 0.55)
    total = total * ((b ** 1.675) * (tc_root ** (-0.45)) * (math.cos(lambdahalf) **  (-1.325)))

    return total

print("The Torenbeek Indivudal is: %dkg" % finalprediction() + ", While Total is: %dkg" % (finalprediction() * 2))


def roskamWeight():
    total = 0.0017 * (Wzf) * (((b*3.28084)/math.cos(lambdahalf)) ** 0.75) * (1 + (6.3 * math.cos(lambdahalf) / (b * 3.28084)) ** 0.5) * ((nnult) ** 0.55)
    total *= (((b * 3.28084) * (S * 10.76)) / ((tr * 3.28084) * Wzf * math.cos(lambdahalf))) ** 0.30
    return (total / 2.2) * 2


print("The Roskam Total: %d kg" % roskamWeight())

