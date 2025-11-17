''' Copied from https://mceq.readthedocs.io/en/latest/examples/Simple_zenith_averaged_neutrinos.html'''
import numpy as np
import crflux.models as pm
from MCEq.core import MCEqRun


mceq_run = MCEqRun(
#provide the string of the interaction model
interaction_model='SIBYLL2.3c',
#primary cosmic ray flux model 
# 
# (so only cosmic rays? problem?) ^^
#
# support a tuple (primary model class (not instance!), arguments)

primary_model = (pm.HillasGaisser2012, "H3a"),

theta_deg=0.0, #we average so it doesnt matter
)

#Power of energy to scale the flux
mag = 3 #doesnt matter for ratio

#obtain energy grid (fixed) of the solution for the x-axis of the plots
e_grid = mceq_run.e_grid

#Dictionary for results
flux = {}

#Define equidistant grid in cos(theta)
angles = np.arccos(np.linspace(1,0,11))*180./np.pi

#Initialize empty grid
for frac in ['numu_total',
             'nue_total','nutau_total']:
    flux[frac] = np.zeros_like(e_grid)


#Sum fluxes, calculated for different angles
for theta in angles:
    mceq_run.set_theta_deg(theta)
    mceq_run.solve()

    flux['numu_total'] += (mceq_run.get_solution('total_numu', mag)
                          + mceq_run.get_solution('total_antinumu', mag))

    flux['nue_total'] += (mceq_run.get_solution('total_nue', mag)
                         + mceq_run.get_solution('total_antinue', mag))


    # since there are no conventional tau neutrinos, prompt=total
    flux['nutau_total'] += (mceq_run.get_solution('total_nutau', mag)
                        + mceq_run.get_solution('total_antinutau', mag))

log_bincenters = mceq_run.e_grid[(mceq_run.e_grid > 1) & (mceq_run.e_grid < 1e4)]

# log_bins are bin centers, so calculate bin edges for log spacing
log_binedges = np.sqrt(log_bincenters[:-1] * log_bincenters[1:])
log_binedges = np.concatenate(([log_bincenters[0] * (log_bincenters[1]/log_bincenters[0])**-0.5], log_binedges, [log_bincenters[-1] * (log_bincenters[-1]/log_bincenters[-2])**0.5]))  # extrapolate edges

#average the results
for frac in ['numu_total',
             'nue_total','nutau_total']:
    flux[frac] = flux[frac]/float(len(angles))
    flux[frac] = np.array([val for i, val in enumerate(flux[frac]) if e_grid[i] in log_bincenters and val != 0])

# save fluxes to csv
np.savetxt('mceq_zenith_averaged_fluxes.csv',
           np.column_stack((log_bincenters,
                            flux['numu_total'],
                            flux['nue_total'],
                            flux['nutau_total'])),
           delimiter=',',
           header='Energy_GeV, numu_total_flux, nue_total_flux, nutau_total_flux',
           comments='')