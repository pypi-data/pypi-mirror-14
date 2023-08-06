# Import the despotic library and various standard python libraries
from despotic import cloud
from despotic.chemistry import NL99_GO
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as constants
import matplotlib


gmc = cloud('cloudfiles/MilkyWayGMC.desp')
gmc.addEmitter('c+', 1e-10)
gmc.addEmitter('o', 1e-4)
gmc.addEmitter('co',1.e-4)
gmc.addEmitter('13co',5.e-7)

gmc.emitters['co'].extrap = True
gmc.emitters['c+'].extrap = True
gmc.emitters['13co'].extrap = True
gmc.emitters['o'].extrap = True


gmc.setChemEq(network=NL99_GO, verbose=True)
gmc.comp.computeDerived(gmc.nH)
gmc.setVirial()


gmc.setTempEq(verbose=True,noClump=True)

