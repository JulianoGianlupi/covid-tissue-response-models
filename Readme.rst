Antiviral Timing and Potency Effects in a Multiscale Spatial Model of an Epithelial Tissue Patch Infected by SARS-CoV-2 Repository
=========================

This is a fossilized repository for "Antiviral Timing and Potency Effects in a Multiscale Spatial Model of an Epithelial Tissue Patch Infected by SARS-CoV-2" (1) that hosts the fossilized code used in its investigation. 

How to run the PK model
=========================

Simulations were developed in COPASI version 4.30 (Build 240) and have been checked through version version 4.34 (Build 251). Below we give details for running the two models.

COPASI model file for parameter fitting
---------------------------------------

The file ``GS-443902_PBMC_PK_v03_3data_plusEurope.cps`` does the parameter estimation task based on the 
data of Humeniuk et al 2020. The data files are included in the GitHub repository.
This COPASI file is set up to do both the parameter fitting task and a basic time course simulation. Load the file in COPASI and insure that the following data files are in the same folder that contains the COPASI .cps file:

* ``Humeniuk_PK_data_Europe_Table_16.txt``
* ``Humeniuk_PK_data_Table_4_Cohort7.txt``
* ``Humeniuk_PK_data_Table_4_Cohort8.txt``

The COPASI model implements the infusion period with an event named "Infusion", which changes the variable  ``k_in`` from 1 to 0 when the model's time exceeds the length of the ``infusion_duration`` parameter (see the COPASI code). To run the parameter estimation, select "Task", "Parameter Estimation", then select an estimation method. We used the "Particle Swarm" method with the default values. In the Upper right of the COPASI window the button "Experimental Data" will open the data window. If the data files listed above are in the same directory as the .cps file then this should be populated with the data mappings for each of the three files. In the upper right of the COPASI window click the "update model" checkbox so the fitted parameters are updated into the starting values for the COPASI model. Click "Run" and the parameter are estimated and available on the sub-item "Results". The Particle Swarm should iterate down to an objective value of about 6.2E-11. The models has now been updated with the results for the terminal clearance half life and the effective compartment volume, typically 30.2 hours and 38.4 liters, respectively. A time course can be run using these parameters by selecting "Tasks", "Time Course" then "Run". This COPASI model generate several graphs, some of which are for the fitting task and some for the time course task. 
 
 COPASI model file for parameter fitting
---------------------------------------

The file ``GS-443902_PBMC_PK_v03_3data_repeatDose_Gallo.cps`` simulates repetitive doses of 200, then 100x4mg/day. Loading this model into COPASI, then "Task", "Time Course", "Run" produces output similar to what is shown in Figure A2 of the paper. Note that the maximum units in COPASI on the Y-axis are mole/liter with values near 10E-5mol/L, which corresponds to the ~10 uM values in Figure A2.

How to run the ABM model
=========================

To run the same ABM investigation done in (1) you can use either your personal computer or a cluster. You need to download CompuCell3D version 4.2.3 (or newer, investigations were done in 4.2.3), https://compucell3d.org/SrcBin. For local running you have to run the python script ``cellular-model/batch_run.py``, you can define the output directory in the script. For cluster execution you need to change the output directory in ``cellular-model/batch_exec.py`` and run the script ``cellular-model/batch_exec.sh``. It is set up for slurm scheduling systems. In those files you can define the output directory (variable ``sweep_output_folder``).

All parameters varied and investigated in (1) are in ``cellular-model/investigation_dictionaries.py`` and are imported to ``batch_run.py`` and ``batch_exec.py``, to change the parameters investigated you only need to change the dictionary used as ``mult_dict`` in one of those files. E.g.

* ``mult_dict = treatment_starts_0``, parameters varied in the fine investigation with treatment starting with the infection of 10 epithelial cells
* ``mult_dict = treatment_starts_0_halved_half_life``, parameters varied in the fine investigation with treatment starting with the infection of 10 epithelial cells and with the half life of GS-443902 halved.

To enable/disable intercell metabolization variability you need to change the flag ``intercell_var`` in the file ``cellular-model/Models/DrugDosingModel/DrugDosingInputs.py`` to True/False respectively.


All models contributed to this repository are shared freely.
