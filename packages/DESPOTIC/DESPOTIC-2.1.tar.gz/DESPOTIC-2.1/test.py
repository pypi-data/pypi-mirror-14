from despotic import cloud,zonedcloud
from despotic.chemistry import NL99,NL99_GC
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as constants

column_density = 1.7e22
NZONES = 8
SFR = 20

gmc = zonedcloud(colDen = np.linspace(0.75*column_density/NZONES,0.75*column_density,NZONES))

gmc.addEmitter('c+',1.e-100)
gmc.addEmitter('c',2.e-4)
gmc.addEmitter('o', 4.e-4)
gmc.addEmitter('co',1.e-100)
gmc.Tcmb = 2.73

for nz in range(NZONES):
    gmc.comp[nz].xH2 = 0.5
    gmc.comp[nz].xHe = 0.1
    gmc.emitters[nz]['co'].extrap = True
    gmc.emitters[nz]['c+'].extrap = True
    gmc.emitters[nz]['o'].extrap = True
    gmc.emitters[nz]['c'].extrap = True

gmc.chi = SFR
gmc.rad.chi = SFR
gmc.ionRate = 1.e-17 * SFR
gmc.rad.ionRate = 1.e-17*SFR
gmc.Tg = 10
gmc.Td = 20
gmc.rad.TradDust = 20
gmc.nH = 5.e3
    
gmc.setChemEq(network=NL99_GC, evolveTemp = 'iterate', verbose=True)
gmc.setTempEq()
