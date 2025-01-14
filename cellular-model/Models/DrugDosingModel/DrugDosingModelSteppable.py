# Model effect of Drug Dosing in viral replication
# Written by J. F. Gianlupi, M.Sci.
# Model parameters are specified in DrugDosingInputs.py
#
# DrugDosingModelSteppable
#   Description: implements drug dosing and viral replication rate reduction
#   Usage:
#       In ViralInfectionVTM.py, add the following
#
#           from Models.DrugDosingModel.DrugDosingModelSteppable import DrugDosingModelSteppable
#           CompuCellSetup.register_steppable(steppable=DrugDosingModelSteppable(frequency=1))


import sys
import os
from cc3d.core.PySteppables import *
import json

sys.path.append(os.path.join(os.environ["ViralInfectionVTM"], "Simulation"))
sys.path.append(os.environ["ViralInfectionVTM"])
try:
    from Simulation.ViralInfectionVTMModelInputs import s_to_mcs, vr_step_size, replicating_rate, kon, koff, \
        initial_unbound_receptors, hill_coeff_uptake_pr, rate_coeff_uptake_pr, max_ck_secrete_infect, unpacking_rate, \
        r_half, translating_rate, packing_rate, secretion_rate
except ModuleNotFoundError:
    from ViralInfectionVTMModelInputs import s_to_mcs, vr_step_size, replicating_rate, kon, koff, \
        initial_unbound_receptors, hill_coeff_uptake_pr, rate_coeff_uptake_pr, max_ck_secrete_infect, unpacking_rate, \
        r_half, translating_rate, packing_rate, secretion_rate
import ViralInfectionVTMLib
from ViralInfectionVTMSteppableBasePy import *

from ViralInfectionVTMSteppables import SimDataSteppable
from nCoVToolkit import nCoVUtils

from .DrugDosingInputs import *

from BatchRun import BatchRunLib

drug_dosing_model_key = "drug_dose_steppable"

days_2_mcs = s_to_mcs / 60 / 60 / 24
hour_2_mcs = s_to_mcs / 60 / 60


def set_simple_pk_full(infusion_amount, time_of_1st_dose, dose_interval, dose_end, first_dose_doubler, observed_t1_2,
                       prophylaxis_time=0):
    # time units are H!!!
    simple_pk_str = f"""
                // Created by libAntimony v2.12.0.3
        function Rate_Law_for_Uptake_1(dose, k, duration)
          dose*k/duration;
        end
        
        Rate_Law_for_Uptake_1 is "Rate Law for Uptake_1"
        
        function Function_for_Uptake(Body, Infusion_duration, Remdes_dose_mol, k_in)
          Rate_Law_for_Uptake_1(Remdes_dose_mol, k_in, Infusion_duration)/Body;
        end
        
        Function_for_Uptake is "Function for Uptake"
        
        
        model *New_Model()
        
          // Compartments and Species:
          compartment Body;
          species GS443902 in Body, GS443902_source in Body, GS443902_sink in Body;
        
          // Rate Rules:
          GS443902_AUC' = GS443902;
        
          // Reactions:
          Uptake: GS443902_source => GS443902; Body*Function_for_Uptake(Body, Infusion_duration, Remdes_dose_mol, k_in);
          Clearance: GS443902 => GS443902_sink; Body*k_out*GS443902;
        
          // Events:
          checkTmax: at 0 after GS443902 > GS443902_Cmax: GS443902_Tmax = time+prophylaxis_time;
          checkCmax: at 0 after GS443902 > GS443902_Cmax: GS443902_Cmax = GS443902 + 1e-9;
          checkC24: at 0 after time+prophylaxis_time == 24: GS443902_C24 = GS443902;
          
          E1: at (time+prophylaxis_time - first_dose > 0): k_in = base_kin*double_first_dose, curr_infu_start = time ; // starts the first infusion
          E2: at ((time+prophylaxis_time-first_dose > dose_interval) && (time < dose_end) && sin((((time-first_dose)/dose_interval))*2*pi)>0): k_in = base_kin, curr_infu_start = time; // starts the subsequent infusions
          E3: at (time+prophylaxis_time - (one_hour + curr_infu_start) > 0): k_in = 0 ; // turns infusion off
        
          // Species initializations:
          GS443902 = 0;
          GS443902_source = Remdes_dose_mol;
          GS443902_sink = 0;
        
          // Compartment initializations:
          Body = 38.4;
          
          //input variables
          infusion_amount = {infusion_amount};
          
          first_dose = {time_of_1st_dose};
          dose_interval = {dose_interval};
          dose_end = {dose_end};

          prophylaxis_time = {prophylaxis_time};
          
          // Variable initializations:
          double_first_dose = {first_dose_doubler};
          curr_infu_start = 0; 
          one_hour = 1;
          Remdes_dose_mol = Remdes_dose_mg/1000/Remdes_MW;
          Remdes_dose_mol has unit_6;
          GS443902_Cmax = GS443902;
          GS443902_Cmax has unit_4;
          GS443902_Tmax = 0;
          GS443902_Tmax has unit_9;
          GS443902_C24 = 0;
          GS443902_C24 has unit_4;
          k_in = 0;
          base_kin = 0.5;
          k_in has unit_7;
          k_out = ln(2)/Observed_t1_2;
          k_out has unit_7;
          Observed_t1_2 = {observed_t1_2};
          Observed_t1_2 has unit_9;
          Remdes_MW = 602.585;
          Remdes_MW has unit_1;
          GS443902_AUC = 0;
          GS443902_AUC has unit_8;
          Remdes_dose_mg = infusion_amount; // 200;
          Remdes_dose_mg has unit_10;
          Infusion_duration = 1;
          Infusion_duration has unit_9;
        
          // Other declarations:
          var GS443902_Cmax, GS443902_Tmax, GS443902_C24, GS443902_AUC, k_in;
          const Body, Remdes_dose_mol, k_out, Observed_t1_2, Remdes_MW, Remdes_dose_mg;
          const Infusion_duration;
        
          // Unit definitions:
          unit substance = mole;
          unit unit_0 = 1 / 3600e2 second;
          unit unit_1 = gram / mole;
          unit unit_2 = 1 mole * 3600e2 second / litre;
          unit unit_4 = mole / litre;
          unit unit_5 = 1e-3 gram;
          unit unit_6 = mole;
          unit unit_3 = 3600e2 second;
          unit length = metre;
          unit area = metre^2;
          unit volume = litre;
          unit time_unit = 360000e2 second;
          unit unit_7 = 1 / 360000e2 second;
          unit unit_8 = 100 mole * 3600e2 second / litre;
          unit unit_9 = 360000e2 second;
          unit unit_10 = 1e-3 gram;
        
          // Display Names:
          unit_0 is "1/h";
          unit_1 is "g/mol";
          unit_2 is "mol/l*h";
          unit_4 is "mol/l";
          unit_5 is "mg";
          unit_6 is "mol";
          unit_3 is "h";
          time_unit is "time";
          unit_7 is "1/(100*h)";
          unit_8 is "100*mol*h/l";
          unit_9 is "100*h";
          unit_10 is "0.001*g";
        end
        
        New_Model is "New Model_1"


    """
    drug_dosig_model_vars = ["Remdes_dose_mol", "[GS443902]", "k_in"]
    return simple_pk_str, drug_dosig_model_vars


class DrugDosingModelSteppable(ViralInfectionVTMSteppableBasePy):
    """
    Implements drug dosing regimen
    """

    def __init__(self, frequency=1):
        ViralInfectionVTMSteppableBasePy.__init__(self, frequency)
        import Models.DrugDosingModel.DrugDosingInputs as DrugDosingInputs
        BatchRunLib.apply_external_multipliers(__name__, DrugDosingInputs)

        self.drug_dosing_model_key = drug_dosing_model_key

        self.set_drug_model_string = set_simple_pk_full
        self.set_control_model_string = set_simple_pk_full

        self.plot_ddm_data = plot_ddm_data_freq > 0
        self.write_ddm_data = write_ddm_data_freq > 0

        self.hill_k = None

        # self.drug_model_string = None

        self.ddm_vars = None
        self.rmax = None

        self.vr_model_name = ViralInfectionVTMLib.vr_model_name

        self.ddm_rr = None

        # self.control_rr = None
        self.active_component = None

        self.alignment_not_done = True

        self.ever_infected = None

    @staticmethod
    def get_roadrunner_for_single_antimony(model):
        """
        :type model: str name of the model
        :param model:
        :return:
        """
        from cc3d.CompuCellSetup import persistent_globals as pg
        for model_name, rr in pg.free_floating_sbml_simulators.items():
            if model_name == model:
                return rr
        return None

    @staticmethod
    def get_sbml_simulator_for_cell(model_name: str, cell: object = None) -> Union[object, None]:
        """
        Returns a reference to RoadRunnerPy or None
        :param model_name: model name
        :param cell: CellG cell object
        :return {instance of RoadRunnerPy} or {None}:
        """
        try:
            dict_attrib = CompuCell.getPyAttrib(cell)
            return dict_attrib['SBMLSolver'][model_name]
        except LookupError:
            return None

    def timestep_cell_sbml(self, model_name: str, cell: object = None):
        if not cell:
            return
        rr = self.get_sbml_simulator_for_cell(model_name, cell)
        rr.timestep()

    def start(self):

        self.ever_infected = len(self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING))

        self.hill_k = active_met_ic50 * ic50_multiplier
        if use_alignment and not prophylactic_treatment:
            print(dose / (24. / dose_interval))
            self.drug_model_string, self.ddm_vars = self.set_drug_model_string(dose / (24. / dose_interval), 99,
                                                                               24 * dose_interval,
                                                                               dose_end, first_dose_doubler,
                                                                               t_half_mult * t_half)
        else:
            print(dose / (24. / dose_interval))
            self.drug_model_string, self.ddm_vars = self.set_drug_model_string(dose / (24. / dose_interval),
                                                                               24 * first_dose,
                                                                               24 * dose_interval,
                                                                               dose_end, first_dose_doubler,
                                                                               t_half_mult * t_half)
        self.active_component = '[GS443902]'
        self.add_free_floating_antimony(model_string=self.drug_model_string, step_size=hour_2_mcs,
                                        model_name='drug_dosing_control')
        self.ddm_rr = self.get_roadrunner_for_single_antimony('drug_dosing_control')
        self.in_rates = []
        self.out_rates = []
        if intercell_var:
            ids = []
        for i, cell in enumerate(self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED)):
            self.add_antimony_to_cell(model_string=self.drug_model_string,
                                      model_name='drug_metabolization',
                                      cell=cell, step_size=hour_2_mcs)
            if intercell_var:
                ids.append(cell.id)
        if intercell_var and ('rmd_in_rate' in params_to_var or 'rmd_out_rate' in params_to_var):
            np.random.shuffle(ids)
            ids1 = ids[:len(ids) // 2]
            ids2 = ids[len(ids) // 2:]
            for id1, id2 in zip(ids1, ids2):
                cell1 = self.fetch_cell_by_id(id1)
                cell2 = self.fetch_cell_by_id(id2)
                cell1.dict['rmd_in_rate'] = 1
                cell2.dict['rmd_in_rate'] = 1

                cell1.dict['rmd_out_rate'] = 1
                cell2.dict['rmd_out_rate'] = 1
                rms_model1 = getattr(cell1.sbml, 'drug_metabolization')
                rms_model2 = getattr(cell2.sbml, 'drug_metabolization')
                if 'rmd_in_rate' in params_to_var:
                    var_in = 11
                    while abs(var_in) > 1:
                        var_in = np.random.normal(0, .25)
                    cell1.dict['base_kin'] = rms_model1['base_kin'] * (1 + var_in)
                    cell1.dict['rmd_in_rate'] = cell1.dict['base_kin'] / rms_model1['base_kin']
                    rms_model1['base_kin'] = cell1.dict['base_kin']
                    self.in_rates.append((cell1.xCOM, cell1.yCOM, rms_model1['base_kin']))

                    cell2.dict['base_kin'] = rms_model2['base_kin'] * (1 - var_in)
                    cell2.dict['rmd_in_rate'] = cell2.dict['base_kin'] / rms_model2['base_kin']
                    rms_model2['base_kin'] = cell2.dict['base_kin']
                    self.in_rates.append((cell2.xCOM, cell2.yCOM, rms_model2['base_kin']))
                if 'rmd_out_rate' in params_to_var:
                    var_out = 11
                    while abs(var_out) > 1:
                        var_out = np.random.normal(0, .25)
                    cell1.dict['k_out'] = rms_model1['k_out'] * (1 + var_out)
                    cell1.dict['rmd_out_rate'] = cell1.dict['k_out'] / rms_model1['k_out']
                    rms_model1['k_out'] = cell1.dict['k_out']
                    self.out_rates.append((cell1.xCOM, cell1.yCOM, rms_model1['k_out']))

                    cell2.dict['k_out'] = rms_model2['k_out'] * (1 - var_out)
                    cell2.dict['rmd_out_rate'] = cell2.dict['k_out'] / rms_model2['k_out']
                    rms_model2['k_out'] = cell2.dict['k_out']
                    self.out_rates.append((cell2.xCOM, cell2.yCOM, rms_model2['k_out']))

        if prophylactic_treatment:
            pass

        if sanity_run:
            self.rmax = replicating_rate
        else:
            self.rmax = self.get_rmax(cell.sbml.drug_metabolization[self.active_component])

        for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED):
            vr_model = getattr(cell.sbml, self.vr_model_name)
            vr_model['replicating_rate'] = self.rmax
            cell.dict['rmax'] = self.rmax

        self.shared_steppable_vars['rmax'] = self.rmax

        # replace viral uptake function
        vim_steppable = self.shared_steppable_vars[ViralInfectionVTMLib.vim_steppable_key]

        vim_steppable.do_cell_internalization = self.do_cell_internalization_changing_rmax

        # Post reference to self
        self.shared_steppable_vars[self.drug_dosing_model_key] = self

    def get_rmax(self, avail4):
        return (1 - nCoVUtils.hill_equation(avail4, self.hill_k, 2)) * replicating_rate

    def step(self, mcs):

        if not prophylactic_treatment and use_alignment and self.alignment_not_done:

            if self.ever_infected >= alignt_at_pop:
                self.alignment_not_done = False

                start_time = 24 * first_dose + hour_2_mcs * (mcs + 1)
                print(f'@@@@\n{start_time}\n{24 * first_dose}\n{mcs}\n{start_time / hour_2_mcs}')
                fileDir = os.path.dirname(os.path.abspath(__file__))
                file_name = os.path.join(fileDir, 'treatment_start.dat')
                with open(file_name, 'w+') as f:
                    f.write('Start time (hours), start time (MCS)')
                    f.write(f'{start_time},{start_time / hour_2_mcs}')
                for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED):
                    vr_model = getattr(cell.sbml, 'drug_metabolization')
                    vr_model['first_dose'] = start_time

        # CELLULARIZATION NOTE!!!
        # For the simple pk each cell has a copy of the model running in themselves
        self.ddm_rr.timestep()
        for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED):
            self.timestep_cell_sbml('drug_metabolization', cell)
            if not sanity_run:
                cell.dict['rmax'] = self.get_rmax(cell.sbml.drug_metabolization[self.active_component])
                if cell.type != self.UNINFECTED:
                    vr_model = getattr(cell.sbml, self.vr_model_name)
                    vr_model['replicating_rate'] = cell.dict['rmax']

    def get_rna_array(self):
        return np.array([cell.dict['Replicating'] for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING,
                                                                                     self.UNINFECTED, self.DYING)])

    def do_cell_internalization_changing_rmax(self, cell, viral_amount_com):
        # WARNING!! OVERWRITES FUNCTION OF MAIN MODEL
        if cell.dict['Receptors'] == 0:
            return False, 0.0

        _k = kon * cell.volume / koff
        diss_coeff_uptake_pr = (initial_unbound_receptors / 2.0 / _k / cell.dict['Receptors']) ** \
                               (1.0 / hill_coeff_uptake_pr)
        uptake_probability = nCoVUtils.hill_equation(viral_amount_com,
                                                     diss_coeff_uptake_pr,
                                                     hill_coeff_uptake_pr)

        cell_does_uptake = np.random.rand() < uptake_probability
        uptake_amount = s_to_mcs / rate_coeff_uptake_pr * uptake_probability

        if cell_does_uptake and cell.type == self.UNINFECTED:
            cell.type = self.INFECTED
            self.ever_infected += 1
            cell.dict['ck_production'] = max_ck_secrete_infect
            self.load_viral_replication_model(cell=cell, vr_step_size=vr_step_size,
                                              unpacking_rate=unpacking_rate,
                                              # replicating_rate=replicating_rate,
                                              replicating_rate=cell.dict['rmax'],
                                              r_half=r_half,
                                              translating_rate=translating_rate,
                                              packing_rate=packing_rate,
                                              secretion_rate=secretion_rate)

        return cell_does_uptake, uptake_amount

    def finish(self):
        pass


class DrugDosingDataFieldsPlots(ViralInfectionVTMSteppableBasePy):
    """
    Responsible for plots, extra fields and data handling
    """

    def __init__(self, frequency=1):
        ViralInfectionVTMSteppableBasePy.__init__(self, frequency)

        self.track_cell_level_scalar_attribute(field_name='internal_viral_RNA', attribute_name='Replicating')
        if intercell_var:
            for p in params_to_var:
                self.track_cell_level_scalar_attribute(field_name=f'relative_{p}', attribute_name=f'{p}')

        self.mvars = None

        self.get_rna_array = None

        self.plot_ddm_data = plot_ddm_data_freq > 0
        self.write_ddm_data = write_ddm_data_freq > 0

        self.ddm_data_win = None

        self.ddm_control_plot = None

        self.rmax_data_win = None

        self.total_rna_plot = None
        self.mean_rna_plot = None
        self.tracked_cell = None

        self.total_virus_released = 0

        self.__flush_counter = 1

        self.avg_prodrug = None
        self.std_prodrug = None

        self.avg_active = None
        self.std_active = None
        self.mean_rmax = None
        self.std_rmax = None
        self.rna_list = None

        if self.write_ddm_data:
            self.data_files = {'ddm_data': 'ddm_data.dat', 'ddm_rmax_data': 'ddm_rmax_data.dat',
                               'ddm_tot_RNA_data': 'ddm_tot_RNA_data.dat', 'ddm_mean_RNA_data': 'ddm_mean_RNA_data.dat',
                               'ddm_total_viral_production_data': 'ddm_total_viral_production_data.dat',
                               'intercell_var_in_rate': 'in_rates.dat', 'intercell_var_out_rate': 'out_rates.dat'}
            self.ddm_data = {'ddm_data': {}, 'ddm_rmax_data': {}, 'ddm_tot_RNA_data': {}, 'ddm_mean_RNA_data': {},
                             'ddm_total_viral_production_data': {}, 'intercell_var_in_rate': {},
                             'intercell_var_out_rate': {}}

    def init_plots(self):
        self.ddm_data_win = self.add_new_plot_window(title='Drug dosing model',
                                                     x_axis_title='Time (hours)',
                                                     y_axis_title='Variables',
                                                     x_scale_type='linear',
                                                     y_scale_type='linear',
                                                     grid=True,
                                                     config_options={'legend': True})

        self.ddm_control_plot = self.add_new_plot_window(title='Drug dosing control plot',
                                                         x_axis_title='Time (hours)',
                                                         y_axis_title='Variables',
                                                         x_scale_type='linear',
                                                         y_scale_type='linear',
                                                         grid=True,
                                                         config_options={'legend': True})

        colors = ['blue', 'red', 'green', 'yellow', 'white', 'magenta']
        ddm_vars = self.mvars.ddm_vars
        for i, var in enumerate(ddm_vars[:-1]):
            c = colors[i]
            self.ddm_data_win.add_plot(var, style='Dots', color=c, size=5)
            self.ddm_control_plot.add_plot(var, style='Dots', color=c, size=5)

        self.rmax_data_win = self.add_new_plot_window(title='Mean r_max vs Time',
                                                      x_axis_title='Time (hours)',
                                                      y_axis_title='r_max',
                                                      x_scale_type='linear',
                                                      y_scale_type='linear',
                                                      grid=True,
                                                      config_options={'legend': True})

        self.rmax_data_win.add_plot('rmax', style='Dots', color='red', size=5)
        self.total_rna_plot = self.add_new_plot_window(title='Total internal viral RNA',
                                                       x_axis_title='Time (hours)',
                                                       y_axis_title='Variables',
                                                       x_scale_type='linear',
                                                       y_scale_type='linear',
                                                       grid=True,
                                                       config_options={'legend': True})
        self.total_rna_plot.add_plot('RNA_tot', style='Dots', color='red', size=5)
        self.mean_rna_plot = self.add_new_plot_window(title='Mean internal viral RNA',
                                                      x_axis_title='Time (hours)',
                                                      y_axis_title='Variables',
                                                      x_scale_type='linear',
                                                      y_scale_type='linear',
                                                      grid=True,
                                                      config_options={'legend': True})
        self.mean_rna_plot.add_plot('RNA_mean', style='Dots', color='red', size=5)

    def init_writes(self):
        from pathlib import Path
        for key, rel_path in self.data_files.items():
            self.data_files[key] = Path(self.output_dir).joinpath(rel_path)
            with open(self.data_files[key], 'w'):
                pass

    def choose_tracked_cell(self):

        cells = [cell for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED)]
        if len(cells):
            return cells[0]
        else:
            return None

    def start(self):
        self.mvars = self.shared_steppable_vars[drug_dosing_model_key]  # main ddm class vars
        self.get_rna_array = self.mvars.get_rna_array

        self.tracked_cell = self.choose_tracked_cell()

        if self.plot_ddm_data:
            self.init_plots()

        if self.write_ddm_data:
            self.init_writes()
        if prophylactic_treatment:

            number_of_prophylactic_steps = int(prophylactic_time / days_2_mcs)
            final_step_idx = list(range(number_of_prophylactic_steps))[-1]
            ddm_rr = self.shared_steppable_vars[drug_dosing_model_key].ddm_rr
            get_rmax = getattr(DrugDosingModelSteppable, 'get_rmax')
            for i in range(number_of_prophylactic_steps):  # let it run for prophylactic_time days

                # instead of timestepping the global sbml I'll step the cells'. This way if we do microdosimetry
                # prof code will still be the same
                for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED):
                    self.mvars.timestep_cell_sbml('drug_metabolization', cell)

                    if i == final_step_idx:
                        cell.dict['rmax'] = self.mvars.get_rmax(
                            cell.sbml.drug_metabolization[self.mvars.active_component])
                        if cell.type != self.UNINFECTED:
                            vr_model = getattr(cell.sbml, self.mvars.vr_model_name)
                            vr_model['replicating_rate'] = cell.dict['rmax']

                self.shared_steppable_vars['rmax'] = self.mvars.get_rmax(self.sbml.drug_dosing_control[
                                                                             self.mvars.active_component])

                self.shared_steppable_vars['pre_sim_time'] = number_of_prophylactic_steps - i
                if self.write_ddm_data:
                    self.do_writes(0)
                if self.plot_ddm_data:
                    self.do_plots(0)
            print(cell.sbml.drug_metabolization['time'])

            if self.write_ddm_data:
                self.flush_stored_outputs()
                self.__flush_counter -= 1

    def get_metabolite_in_cell(self, cell):
        metabolite = cell.sbml.drug_metabolization[self.mvars.ddm_vars[1]]
        return metabolite

    def get_total_metabolite_in_cells(self):

        m = []
        for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED):
            cm = self.get_metabolite_in_cell(cell)
            m.append(cm)

        return m

    def get_mean_std_rmax(self):
        rmax_list = [cell.dict['rmax'] for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING,
                                                                          self.UNINFECTED)]
        if not len(rmax_list):
            return 0, 0
        return np.mean(rmax_list), np.std(rmax_list)

    def get_mean_std_prodrug(self):
        prodrug_list = [cell.sbml.drug_metabolization['k_in'] for cell in
                        self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED)]
        if not len(prodrug_list):
            return 0, 0
        return np.mean(prodrug_list), np.std(prodrug_list)

    def get_mean_std_active(self):
        active_met_list = [cell.sbml.drug_metabolization[self.mvars.active_component] for cell in
                           self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.UNINFECTED)]
        if not len(active_met_list):
            return 0, 0
        return np.mean(active_met_list), np.std(active_met_list)

    def do_plots(self, mcs):
        """
        :parameter mcs
        :return None
        """

        if prophylactic_treatment and mcs == 0:
            time = mcs - self.shared_steppable_vars['pre_sim_time']
        else:
            time = mcs
        if time < 0:
            self.ddm_control_plot.add_data_point(self.mvars.ddm_vars[0], s_to_mcs * time / 60 / 60,
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[0]] *
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[-1]])
            self.ddm_control_plot.add_data_point(self.mvars.ddm_vars[1], s_to_mcs * time / 60 / 60,
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[1]])
            if self.tracked_cell is not None:
                infusion = self.tracked_cell.sbml.drug_metabolization[self.mvars.ddm_vars[0]] * \
                           self.tracked_cell.sbml.drug_metabolization[self.mvars.ddm_vars[-1]]
                self.ddm_data_win.add_data_point(self.mvars.ddm_vars[0], s_to_mcs * time / 60 / 60, infusion)
                self.ddm_data_win.add_data_point(self.mvars.ddm_vars[1], s_to_mcs * time / 60 / 60,
                                                 self.tracked_cell.sbml.drug_metabolization[self.mvars.ddm_vars[1]])
        if time >= 0:
            self.ddm_control_plot.add_data_point(self.mvars.ddm_vars[0], s_to_mcs * time / 60 / 60,
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[0]] *
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[-1]])
            self.ddm_control_plot.add_data_point(self.mvars.ddm_vars[1], s_to_mcs * time / 60 / 60,
                                                 self.sbml.drug_dosing_control[self.mvars.ddm_vars[1]])
            if self.tracked_cell is not None:
                infusion = self.tracked_cell.sbml.drug_metabolization[self.mvars.ddm_vars[0]] * \
                           self.tracked_cell.sbml.drug_metabolization[self.mvars.ddm_vars[-1]]

                self.ddm_data_win.add_data_point(self.mvars.ddm_vars[0], s_to_mcs * time / 60 / 60, infusion)
                self.ddm_data_win.add_data_point(self.mvars.ddm_vars[1], s_to_mcs * time / 60 / 60,
                                                 self.avg_active)

            if time > first_dose / days_2_mcs or constant_drug_concentration:
                self.rmax_data_win.add_data_point('rmax', s_to_mcs * mcs / 60 / 60, self.mean_rmax)

            self.total_rna_plot.add_data_point('RNA_tot', s_to_mcs * mcs / 60 / 60, np.sum(self.rna_list))
            self.mean_rna_plot.add_data_point('RNA_mean', s_to_mcs * mcs / 60 / 60, np.mean(self.rna_list))

    def get_ddm_data_list(self):

        d = [self.sbml.drug_dosing_model[x] for x in self.mvars.ddm_vars[:3]]

        total_mets = self.get_total_metabolite_in_cells()
        for m in total_mets:
            d.append(np.sum(m))
        return d

    def do_writes(self, mcs):

        if prophylactic_treatment and mcs == 0:
            time = mcs - self.shared_steppable_vars['pre_sim_time']
        else:
            time = mcs

        if time == 0:
            self.ddm_data['intercell_var_in_rate'][mcs] = self.mvars.in_rates
            self.ddm_data['intercell_var_out_rate'][mcs] = self.mvars.out_rates

        if time < 0:
            self.avg_active, _ = self.get_mean_std_active()
            self.avg_prodrug, _ = self.get_mean_std_prodrug()
            self.ddm_data['ddm_data'][time] = [self.avg_prodrug,
                                               self.avg_active]

            self.ddm_data['ddm_rmax_data'][time] = [0]

            self.ddm_data['ddm_tot_RNA_data'][mcs] = [0]
            self.ddm_data['ddm_mean_RNA_data'][mcs] = [0]
            self.ddm_data['ddm_total_viral_production_data'][mcs] = [0]

        if time >= 0:
            self.ddm_data['ddm_data'][time] = [self.avg_prodrug,
                                               self.avg_active]

            mean, _ = self.get_mean_std_rmax()
            self.ddm_data['ddm_rmax_data'][time] = [mean]

            rna_list = self.get_rna_array()

            self.ddm_data['ddm_tot_RNA_data'][mcs] = [np.sum(rna_list)]
            self.ddm_data['ddm_mean_RNA_data'][mcs] = [np.mean(rna_list)]

            self.ddm_data['ddm_total_viral_production_data'][mcs] = [self.total_virus_released]

        if mcs >= int(self.simulator.getNumSteps() / 4 * self.__flush_counter):
            self.flush_stored_outputs()

    def flush_stored_outputs(self):
        """
        Write stored outputs to file and clear output storage
        :return: None
        """
        # Each tuple contains the necessary information for writing a set of data to file
        #   1. Boolean for whether we're writing to file at all
        #   2. The path to write the data to
        #   3. The data to write
        out_info = [(self.write_ddm_data, self.data_files[x], self.ddm_data[x]) for x in self.ddm_data.keys()]
        for write_data, data_path, data in out_info:
            if write_data:
                with open(data_path, 'a') as fout:
                    fout.write(SimDataSteppable.data_output_string(self, data))
                    data.clear()
        self.__flush_counter += 1

    def step(self, mcs):

        if self.tracked_cell is None or self.tracked_cell.type == self.DYING:
            self.tracked_cell = self.choose_tracked_cell()

        self.total_virus_released += self.shared_steppable_vars['total_virus_release_this_mcs']

        calculated_stuff = False
        if self.plot_ddm_data and mcs % plot_ddm_data_freq == 0:
            if not calculated_stuff:
                self.avg_active, self.std_active = self.get_mean_std_active()
                self.avg_prodrug, self.std_prodrug = self.get_mean_std_prodrug()
                self.mean_rmax, self.std_rmax = self.get_mean_std_rmax()
                self.rna_list = self.get_rna_array()
                calculated_stuff = True
            self.do_plots(mcs)
        if self.write_ddm_data and mcs % write_ddm_data_freq == 0:
            if not calculated_stuff:
                self.avg_prodrug, self.std_prodrug = self.get_mean_std_prodrug()
                self.avg_active, self.std_active = self.get_mean_std_active()
                self.mean_rmax, self.std_rmax = self.get_mean_std_rmax()
                self.rna_list = self.get_rna_array()
                calculated_stuff = True
            self.do_writes(mcs)

    def save_per_cell_met_rates_time_of_death_and_viral_auc(self):

        data_dict = {'cell_id': [],
                     'relative_in_rate': [],
                     'time_of_infection': [],
                     'time_of_virus_release': [],
                     'relative_out_rate': [],
                     'time_of_death': [],
                     'virus_auc': []
                     }
        for cell in self.cell_list_by_type(self.INFECTED, self.VIRUSRELEASING, self.DYING):
            data_dict['cell_id'].append(cell.id)
            if intercell_var:
                data_dict['relative_in_rate'].append(cell.dict['rmd_in_rate'])
                data_dict['relative_out_rate'].append(cell.dict['rmd_out_rate'])
            data_dict['time_of_infection'].append(cell.dict['time_of_infection'])
            data_dict['time_of_virus_release'].append(cell.dict['time_of_virus_release'])
            data_dict['time_of_death'].append(cell.dict['time_of_death'])
            data_dict['virus_auc'].append(cell.dict['virus_released'])
            pass

        path_json = Path(self.output_dir).joinpath('per_cell_viral_production.json')

        with open(path_json, 'w+') as outf:
            json.dump(data_dict, outf)

    def on_stop(self):
        self.finish()

    def finish(self):
        if self.write_ddm_data:
            self.save_per_cell_met_rates_time_of_death_and_viral_auc()
            self.flush_stored_outputs()
