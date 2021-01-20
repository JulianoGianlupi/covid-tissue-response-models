from numpy import log

__param_desc__ = {}

# remdesivir metabolites names

__param_desc__['remdesivir_name'] = 'proper molecular name, from https://doi.org/10.1111/cts.12840 '

remdesivir_name = 'RDV;  GS-5734'

__param_desc__['intermediary_metabolite_1'] = 'proper molecular name for intermediary metabolite, ' \
                                              'from https://doi.org/10.1111/cts.12840 '
intermediary_metabolite_1 = 'GS-704277'

__param_desc__['intermediary_metabolite_2'] = 'proper molecular name for intermediary metabolite, ' \
                                              'from https://doi.org/10.1111/cts.12840 '
intermediary_metabolite_2 = 'GS-441524'

__param_desc__['active_met_name'] = 'proper molecular name for active metabolite (tri-phosphate)'
active_met_name = 'GS-443902'

# Data control options
__param_desc__['plot_ddm_data_freq'] = 'Plot drug model data frequency'
plot_ddm_data_freq = 1  # Plot recovery model data frequency (disable with 0)
__param_desc__['write_ddm_data_freq'] = 'Write drug model data to simulation directory frequency'
write_ddm_data_freq = 1  # Write recovery model data to simulation directory frequency (disable with 0)

# DDM SBML model

# Treatment options

__param_desc__['constant_drug_concentration'] = 'bool flag for constant prodrug'
constant_drug_concentration = False

__param_desc__['prophylactic_treatment'] = 'bool flag for prophylactic treatment'
prophylactic_treatment = False

__param_desc__['treatment_ends'] = 'bool flag for setting a end time for treatment or not'
treatment_ends = False

__param_desc__['sanity_run'] = 'bool for shutting off drug treatment (True -> no treatment)'
sanity_run = False

__param_desc__['double_sbml_step'] = 'bool for doing 2 sbmls calls'
double_sbml_step = False

__param_desc__['double_loading_dose'] = 'bool for having the loading dose be double'
double_loading_dose = False

__param_desc__['first_dose_doubler'] = 'multiplier to double loading dose'
first_dose_doubler = 1
if double_loading_dose:
    first_dose_doubler = 2

# initial drug concentrations
__param_desc__['Drug_pls'] = 'Concentration of Drug already in plasma'
Drug_pls = 0

__param_desc__['Drug_peri'] = 'Concentration of Drug already in the periphery'
Drug_peri = 0

__param_desc__['Drug_lung'] = 'Concentration of Drug already in the lungs'
Drug_lung = 0

__param_desc__['Ala_met'] = 'Concentration of alanine metabolite already in the system'
Ala_met = 0

__param_desc__['NMP_met'] = 'Concentration of NMP metabolite already in the system'
NMP_met = 0

__param_desc__['NTP_met'] = 'Concentration of NTP metabolite already in the system'
NTP_met = 0

# rates
__param_desc__['kp'] = 'rate of remdesivir from plasma to periphery, units /day'
kp = 0.41195

__param_desc__['kpp'] = 'rate of remdesivir from periphery to plasma, units /day'
kpp = 0.36502

__param_desc__['k0'] = 'reversible lung-plasma rate, units /day'
k0 = 6.3335

__param_desc__['k12'] = 'drug -> metabolite alanine rate, units /day'
k12 = 10.0

__param_desc__['k23'] = 'metabolite alanine -> metabolite NMP rate, units /day'
k23 = 10.0

__param_desc__['k34'] = 'metabolite NMP -> metabolite NTP rate, units /day'
k34 = 10.0

__param_desc__['kE0'] = 'elimination rate of drug from plasma, units /day'
kE0 = 16.635
__param_desc__['kE1'] = 'elimination rate of drug from lungs, units /day'
kE1 = 16.635
__param_desc__['kE2'] = 'elimination rate of metabolite alanine, units /day'
kE2 = 16.635
__param_desc__['kE3'] = 'elimination rate of metabolite NMP, units /day'
kE3 = 16.635
__param_desc__['kE4'] = 'elimination rate of metabolite NTP, units /day'
kE4 = 16.635

# dosing
__param_desc__['first_dose'] = 'time of first dose in days'
first_dose = 1
if prophylactic_treatment:
    first_dose = 0

__param_desc__['prophylactic_time'] = 'Number of days of prophylactic treatment'
prophylactic_time = 1

if not prophylactic_treatment:
    prophylactic_time = 0

__param_desc__['daily_dose'] = 'how much drug is given in a DAY'
daily_dose = 1

__param_desc__['dose_interval'] = 'time interval between doses in days'
dose_interval = 1

__param_desc__['initial_dose'] = 'initial dose (arbitrary amount)'
initial_dose = daily_dose / (24. / dose_interval)  # daily_dose/(N doses/day)

__param_desc__['dose'] = 'dose of subsequent treatments (arbitrary units)'
dose = initial_dose

if sanity_run:
    initial_dose = 0
    dose = 0

__param_desc__['dose_end'] = 'time of end of treatment in days'
dose_end = 1
if not treatment_ends:
    dose_end = 1e99

# rate reduction parameters

# parameters
__param_desc__['auto_ec50'] = 'bool for auto scaling of EC50 by max(avail4) and rel_avail4_EC50'
auto_ec50 = False

__param_desc__['drug_ic50'] = 'value for drug ic50'
drug_ic50 = 1

__param_desc__['drug_2_a4_factor'] = 'factor to go from drug to max a4 for constant drug' \
                                     'concentration. obtained by fitting max(a4) vs drug'
drug_2_a4_factor = 1.5291823098746118

__param_desc__['ec50'] = 'value for ec50 in the hill equation, only used if auto_ec50 is false'
ec50 = drug_2_a4_factor * drug_ic50

__param_desc__['rel_avail4_EC50'] = 'EC50 value for rmax reduction in therms of max available 4,' \
                                    ' ie EC50 = rel_avail4_EC50 * max(available 4)'
rel_avail4_EC50 = 1

__param_desc__['hill_coef'] = 'Hill coeficient for diminishing hill function of rmax'
hill_coef = 2
