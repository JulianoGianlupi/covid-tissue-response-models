import sys
import os

sys.path.append(os.path.dirname(__file__))
import render_defs

# Export defs
rc_params = render_defs.rc_params_base.copy()
rc_params['figure.figsize'] = (3, 2.5)

export_fig_height = 2.5
export_fig_width = 3
params_export = ['ImmuneResp', 'MedViral', 'Uninfected', "Infected", "InfectedSecreting", "Dying", 'r_max', 'Prodrug',
                 "MedViral", "Viral", 'Active Metabolite', 'tot_RNA', 'MedCyt']
# Plot manipulators
s_to_mcs = 300.
exp_replicating_rate = 1.0 / 200.0 * 1.0 / 60.0
replicating_rate = exp_replicating_rate * s_to_mcs

days_plot = [0, 7, 14]


def manip_plot_axes(fig, ax):
    render_defs.manip_plot_axis_conv(fig, ax)
    render_defs.manip_plot_time_label(fig, ax)

    xticks = [int(x) * 24 * 60 / 5 for x in days_plot]
    ax.set_xticks(xticks)


def manip_all(fig, ax):
    manip_plot_axes(fig, ax)
    # render_defs.manip_plot_ode(fig, ax)


def manip_susceptible(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=1600)
    render_defs.manip_set_ticks(yticks=[0, 800, 1600])(fig, ax)


def manip_infected(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=500)
    render_defs.manip_set_ticks(yticks=[0, 250, 500])(fig, ax)


def manip_virus_releasing(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=1200)
    render_defs.manip_set_ticks(yticks=[0, 600, 1200])(fig, ax)


def manip_dead(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=1600)
    render_defs.manip_set_ticks(yticks=[0, 800, 1600])(fig, ax)


def manip_immune_local(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=2)(fig, ax)


def manip_immune_lymph(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=2)(fig, ax)


def manip_virus(fig, ax):
    manip_all(fig, ax)
    render_defs.manip_plot_log(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=1E4)(fig, ax)
    render_defs.manip_set_ticks(yticks=[1, 1E2, 1E4])(fig, ax)


def manip_cytokine(fig, ax):
    manip_all(fig, ax)
    render_defs.manip_plot_log(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=2)(fig, ax)


def manip_cytokine_lymph(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=2)(fig, ax)


def manip_death_virus(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=1600)
    render_defs.manip_set_ticks(yticks=[0, 800, 1600])(fig, ax)


def manip_death_contact(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=2)(fig, ax)


def manip_internal_RNA(fig, ax):
    manip_all(fig, ax)
    render_defs.plot_lim_manip(bottom=1, top=6000)(fig, ax)


def manip_drug(fig, ax):
    manip_plot_axes(fig, ax)


def manip_rmax(fig, ax):
    manip_plot_axes(fig, ax)
    render_defs.plot_lim_manip(bottom=0, top=1.1 * replicating_rate)(fig, ax)
    # render_defs.plot_lim_manip(bottom=1, top=0.025)(fig, ax)                               


from collections import defaultdict

stat_plot_manips = defaultdict(lambda: None)
stat_plot_manips['Susceptible'] = manip_susceptible
stat_plot_manips['Infected'] = manip_infected
stat_plot_manips['Virusreleasing'] = manip_virus_releasing
stat_plot_manips['Dead'] = manip_dead
stat_plot_manips['Immunelocal'] = manip_immune_local
stat_plot_manips['Immunelymphnode'] = manip_immune_lymph
stat_plot_manips['MedViral'] = manip_virus
stat_plot_manips['MedCyt'] = manip_cytokine
stat_plot_manips['MedCytL'] = manip_cytokine_lymph
stat_plot_manips['Viral'] = manip_death_virus
stat_plot_manips['Contact'] = manip_death_contact
stat_plot_manips['tot_RNA'] = manip_internal_RNA
stat_plot_manips['r_max'] = manip_rmax
stat_plot_manips['Metabolite4'] = manip_drug
stat_plot_manips['Metabolite4'] = manip_drug
