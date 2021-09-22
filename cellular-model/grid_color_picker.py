# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 14:57:57 2021

@author: Juliano
"""

import os
import numpy as np
# from scipy.signal import argrelextrema, find_peaks
# from virus_area_grapher import get_sim_inputs, get_parameters_by_name, get_sets_of_param_value, get_viral_load_column
from grid_color_picker_functions import get_sim_inputs, get_parameters_by_name, get_sets_of_param_value, \
                                        determine_outcome, get_all_runs_data, pick_color
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors as pycolors
from matplotlib.lines import Line2D

import json
# from fury import colormap as fcmps
# data_list is all of the 
# data_analyzed[q][mcs] = quantile(data_list, q / 100)



if __name__ == '__main__':
    base_path = r'D:\ddm-unprocessed-data\longer-period\redone_intercell_var'
    
    # batches = ['batch_2_0', 'batch_3_0', 'batch_4_0', 'batch_5_0', 'batch_6_0', 'batch_7_0', 'batch_1_0']
    batches = ['batch_2_0', 'batch_3_0', 'batch_4_0', 'batch_1_0']
    # batches = ['batch_3_0']
    
    for b in batches:
        print(b)
        path_of_batches = os.path.join(base_path, b)
    
        inputs = get_sim_inputs(path_of_batches)
        
        
        first_dose = get_parameters_by_name('first_dose', 
                                         inputs[0]['__input_dict__'])['first_dose']
        
        sets_to_do = get_sets_of_param_value('first_dose', first_dose, inputs)
        
        runs = ['run_0', 'run_1', 'run_2', 'run_3', 'run_4', 'run_5', 'run_6', 'run_7']#, 'run_8', 'run_9',]
        file_vir = 'med_diff_data.csv'
        file_pop = 'pop_data.csv'
        file_auc = 'ddm_total_viral_production_data.csv'
        thrs_vir = 1.3
        
        chronic_thr = 1e-4
        init_infected = 5
        time_conv = 5 * 60 / 60  / 60  / 24
        # slopes = []
        log_slopes = []
        # sets_grid =np.array(sets_to_do).reshape((10,11))
        fig_vir, axs_vir = plt.subplots(nrows=10, ncols=11)
        # fig, axs = plt.subplots(2)
        
        analysis_dict = {}
        
        # cleared without 1
        # cleared with 2
        # cleared slow 3
        # chronic 4
        # runaway 5
        # colors = fcmps.distinguishable_colormap(bg=(1,1,1), nb_colors=5)
        # cmap = cm.get_cmap('plasma')
        # colors = [pycolors.to_hex(cmap(0.25*i)) for i in range(4)]
        # colors.reverse()
        # colors generated with distinctipy, using get_colors, and setting colorblind mode to Deuteranomaly 
        colors_rgb = [(0.0642696504732918, 0.8699343638031362, 0.60835656136375),
          (0, 0.5, 1),
          (0.8761702002961254, 0.5405079602880609, 0.013746543299208436),
          (0.8089037840504687, 0.013387991900796647, 0.6094183334827362)]
        colors = [pycolors.to_hex(c) for c in colors_rgb]
        colors =['#008000', '#0000FF', '#000000', '#FF0000']
        names = ['Rapid clearance', 'Slow clearance',
                 'Persistent infection', 'Runaway virus']
        analysis_dict['comment'] = [['cleared virus', 'cleared without reapearance (unused)', 'fast clearance', 
                                     'tendency (chronic, runaway, containment)'],
                                    'color',
                                    'vir thrs'
                                    'median time start',
                                    'median time start + 14']
        
        for ax_vir, s in zip(axs_vir.flat, sets_to_do):
            print(s)
            
            cleared_vir, cleared_without_reapearance, \
                cleared_fast, tendency, median_start_time = determine_outcome(s, runs, path_of_batches, file_vir,
                                                           file_pop, file_auc, time_conv, chronic_thr, first_dose)
            cleared_fast = bool(cleared_fast)
            vir_tcs = get_all_runs_data(file_vir,os.path.join(path_of_batches,s),runs)
            
            vir_median = np.median(vir_tcs, axis=1)
            # ax_vir.title.set_text(s)
            # ax_vir.plot(vir_median)
            # # print(np.max(vir_median))
            # ax_vir.hlines(thrs_vir, xmin=0, xmax=len(vir_median), colors='red')
            # ax_vir.vlines(median_start_time/time_conv, ymin=1e-3, ymax=10000, colors='blue')
            # ax_vir.vlines((median_start_time+14)/time_conv, ymin=1e-3, ymax=10000, colors='black')
            # # ax_vir.hlines(1.1*thrs_vir, xmin=0, xmax=len(vir_median), colors='blue')
            # # ax_vir.hlines(0.*thrs_vir, xmin=0, xmax=len(vir_median), colors='red')
            # ax_vir.set_ylim([1e-3, 10000])
            # ax_vir.set_yscale('log')
            analysis_dict[s] = [[bool(cleared_vir), bool(cleared_without_reapearance), 
                                 bool(cleared_fast), tendency],
                                None,
                                thrs_vir,
                                median_start_time,
                                median_start_time+14]
            analysis_dict[s][1] = pick_color(analysis_dict[s][0], colors)
            # analysis_dict[s][0] = [cleared_vir, cleared_fast, tendency]
            # break
        # for ax_vir, s in zip(axs_vir.flat, sets_to_do):
        #     for side in ['top','bottom','left','right']:
        #         ax_vir.spines[side].set_color(analysis_dict[s][1])
        #         ax_vir.spines[side].set_linewidth(5)
        #     # ax_vir.spines['top'].set_color(analysis_dict[s][1])
        #     # ax_vir.spines['right'].set_color(analysis_dict[s][1])
            # ax_vir.spines['left'].set_color(analysis_dict[s][1])
        # legend_elements = [Line2D([0], [0], color=c, lw=4, label=l) for c,l in zip(colors, names)]
        # fig_vir.legend(handles=legend_elements, loc = 'center left')
        with open(os.path.join(path_of_batches, 'set_colors.json'), 'w+') as f:
            json.dump(analysis_dict, f, indent=4)