Antiviral Timing and Potency Effects in a Multiscale Spatial Model of an Epithelial Tissue Patch Infected by SARS-CoV-2 Repository
=========================

This is a fossilized repository for "Antiviral Timing and Potency Effects in a Multiscale Spatial Model of an Epithelial Tissue Patch Infected by SARS-CoV-2" (1) that hosts the fossilized code used in its investigation. 

To run the PK model of (1) you need COPASI and [...]

To run the same ABM investigation done in (1) you can use either your personal computer or a cluster. You need to download CompuCell3D version 4.2.3 (or newer, investigations were done in 4.2.3), https://compucell3d.org/SrcBin. For local running you have to run the python script ``cellular-model/batch_run.py``, you can define the output directory in the script. For cluster execution you need to change the output directory in ``cellular-model/batch_exec.py`` and run the script ``cellular-model/batch_exec.sh``. It is set up for slurm scheduling systems. In those files you can define the output directory (variable ``sweep_output_folder``)

All parameters varied and investigated in (1) are in ``cellular-model/investigation_dictionaries.py`` and are imported to ``batch_run.py`` and ``batch_exec.py``, to change the parameters investigated you only need to change the dictionary used as ``mult_dict`` in one of those files. E.g.

* ``mult_dict = treatment_starts_0``, parameters varied in the fine investigation with treatment starting with the infection of 10 epithelial cells
* ``mult_dict = treatment_starts_0_halved_half_life``, parameters varied in the fine investigation with treatment starting with the infection of 10 epithelial cells and with the half life of GS-443902 halved.

To enable/disable intercell metabolization variability you need to change the flag ``intercell_var`` in the file ``cellular-model/Models/DrugDosingModel/DrugDosingInputs.py`` to True/False respectively.

Shared and reproducible models
===============================

All models contributed to this repository are shared freely.
