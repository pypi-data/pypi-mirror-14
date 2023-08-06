"""
params.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

Contributors: salvadordura@gmail.com
"""

netParams = {}  # dictionary to store sets of network parameters
simConfig = {}  # dictionary to store sets of simulation configurations


###############################################################################
#
# MPI HH TUTORIAL PARAMS
#
###############################################################################

###############################################################################
# NETWORK PARAMETERS
###############################################################################

# Cell properties list
netParams['cellParams'] = []

netParams['delayMin'] = 5
netParams['delayMean'] = 13.0
netParams['delayVar'] = 1.4

## PYR cell properties
# cellParam = {'label': 'PYR', 'conditions': {'cellType': 'PYR'},  'sections': {}, 'pointNeuron':{}}
# cellParam['pointNeuron']['Izhi2007b'] = {'C':100, 'k':0.7, 'vr':-60, 'vt':-40, 'vpeak':35, 'a':0.03, 'b':-2, 'c':-50, 'd':100, 'celltype':1}

# soma = {'geom': {}, 'topol': {}, 'mechs': {}, 'synMechs': {}}  # soma properties
# soma['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0, 'pt3d': []}
# soma['geom']['pt3d'].append((0, 0, 0, 20))
# soma['geom']['pt3d'].append((0, 0, 20, 20))
# soma['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} 
# soma['synMechs']['NMDA'] = {'type': 'ExpSyn', 'loc': 0.5, 'tau': 0.1, 'e': 0}

# dend = {'geom': {}, 'topol': {}, 'mechs': {}, 'synMechs': {}}  # dend properties
# dend['geom'] = {'diam': 5.0, 'L': 150.0, 'Ra': 150.0, 'cm': 1, 'pt3d': []}
# dend['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}
# dend['mechs']['pas'] = {'g': 0.0000357, 'e': -70} 
# dend['synMechs']['NMDA'] = {'type': 'Exp2Syn', 'loc': 1.0, 'tau1': 0.1, 'tau2': 1, 'e': 0}

# cellProp['sections'] = {'soma': soma, 'dend': dend}  # add sections to dict
# netParams['cellProps'].append(cellProp)  # add dict to list of cell properties


cellProp = {'label': 'PYRrule', 'conditions': {'cellType': 'PYR'},  'sections': {}}
soma = {'geom': {}, 'topol': {}, 'mechs': {}, 'synMechs': {}}  # soma properties
soma['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}
soma['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} 
soma['synMechs']['NMDA'] = {'_type': 'Exp2Syn', '_loc': 1.0, 'tau1': 0.1, 'tau2': 1, 'e': 0}
cellProp['sections'] = {'soma': soma}  # add sections to dict
netParams['cellParams'].append(cellProp)  # add dict to list of cell properties


# Population parameters
netParams['popParams'] = []  # create list of populations - each item will contain dict with pop params
netParams['popParams'].append({'popLabel': 'S',  'cellType': 'PYR', 'cellModel': 'HH', 'ynormRange':[0.2, 0.5], 'density':'50000*ynorm'}) # add dict with params for this pop 
netParams['popParams'].append({'popLabel': 'M',  'cellType': 'PYR', 'numCells': 2, 'cellModel': 'HH'}) # add dict with params for this pop 
netParams['popParams'].append({'popLabel': 'background', 'cellModel': 'NetStim', 'rate': 100, 'noise': 0.5, 'source': 'random'})  # background inputs

netParams['popTagsCopiedToCells'] = ['popLabel', 'cellModel', 'cellType']


# Connectivity parameters
netParams['connParams'] = []  

netParams['connParams'].append(
    {'preTags': {'popLabel': 'S'}, 'postTags': {'popLabel': 'M'}, # background -> PYR (HH)
    'probability': '0.2',
    'weight': 20, 
    'synMech': 'NMDA',
    'loc': 1.0,
    'delay': 5})  

'''
netParams['connParams'].append(
    {'preTags': {'cellType': 'PYR'}, 'postTags': {'cellType': 'PYR'},
    'weight': 'gauss(10,5)',        # weight of each connection
    'delay': '50+gauss(13.0,1.4)+pre_x-post_y',
    'convergence': '0.2+gauss(13.0,1.4)+post_y', 
    'threshold': 10})       # threshold

netParams['connParams'].append(
    {'preTags': {'cellType': 'PYR'}, 'postTags': {'cellType': 'PYR'},
    'weight': 'gauss(10,5)',        # weight of each connection
    'delay': '50+gauss(13.0,1.4)+pre_x-post_y',
    'divergence': '0.2+gauss(13.0,1.4)+pre_y', 
    'threshold': 10})       # threshold

netParams['connParams'].append(
    {'preTags': {'cellType': 'PYR'}, 'postTags': {'cellType': 'PYR'},
    'weight': 0.2,        # weight of each connection
    'delay': 'delayMin + gauss(delayMean, delayVar)',
    'probability': 'exp(-dist_2D/200)', 
    'threshold': 10})       # threshold

netParams['connParams'].append(
    {'preTags': {'popLabel': 'background'}, 'postTags': {'cellType': 'PYR'}, # background -> PYR (Izhi2007b)
    'probability': 0.5,
    'delay': 'delayMin + gauss(delayMean, delayVar)',
    'weight': 10, 
    'synMech': 'NMDA'})  

netParams['connParams'].append(
    {'preTags': {'popLabel': 'background'}, 'postTags': {'cellType': 'PYR', 'cellModel': 'HH'}, # background -> PYR (HH)
    'connFunc': 'fullConn',
    'weight': 20, 
    'synMech': 'NMDA',
    'loc': 1.0,
    'delay': 5})  
'''

###############################################################################
# SIMULATION PARAMETERS
###############################################################################

simConfig = {}  # dictionary to store simConfig

# Simulation parameters
simConfig['duration'] = simConfig['tstop'] = 1*1e3 # Duration of the simulation, in ms
simConfig['dt'] = 0.025 # Internal integration timestep to use
simConfig['randseed'] = 1 # Random seed to use
simConfig['createNEURONObj'] = 1  # create HOC objects when instantiating network
simConfig['createPyStruct'] = 1  # create Python structure (simulator-independent) when instantiating network
simConfig['verbose'] = 1  # show detailed messages 


# Recording 
simConfig['recordTraces'] = {'Vsoma':{'sec':'soma','pos':0.5,'var':'v'}}
simConfig['recordStim'] = True  # record spikes of cell stims
simConfig['recordStep'] = 10 # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig['filename'] = 'example'  # Set file output name
simConfig['saveFileStep'] = 1000 # step size in ms to save data to disk
simConfig['savePickle'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveJson'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveMat'] = False # Whether or not to write spikes etc. to a .mat file
simConfig['saveTxt'] = False # save spikes and conn to txt file
simConfig['saveDpk'] = False # save to a .dpk pickled file
simConfig['saveHDF5'] = False

# Analysis and plotting 
simConfig['plotRaster'] = True # Whether or not to plot a raster
simConfig['plotTracesGids'] = [] # plot recorded traces for this list of cells
simConfig['plotPsd'] = False # plot power spectral density
simConfig['maxspikestoplot'] = 3e8 # Maximum number of spikes to plot
simConfig['plotConn'] = False # whether to plot conn matrix
simConfig['plotWeightChanges'] = False # whether to plot weight changes (shown in conn matrix)
simConfig['plot3dArch'] = False # plot 3d architecture



###############################################################################
# RUN MODEL
###############################################################################

from netpyne import framework as f

f.sim.initialize(
    simConfig = simConfig, 
    netParams = netParams)  # create network object and set cfg and net params

f.net.createPops()                  # instantiate network populations
f.net.createCells()                 # instantiate network cells based on defined populations
f.net.connectCells()                # create connections between cells based on params
f.sim.setupRecording()              # setup variables to record for each cell (spikes, V traces, etc)
f.sim.runSim()                      # run parallel Neuron simulation  
f.sim.gatherData()                  # gather spiking data and cell info from each node
f.sim.saveData()                    # save params, cell info and sim output to file (pickle,mat,txt,etc)
f.analysis.plotData()               # plot spike raster



