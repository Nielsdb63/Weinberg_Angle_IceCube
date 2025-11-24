This folder contains files trying to find the Weinberg from data gotten with Icecube.

ST_final.ipynb is the most up to date file, resulting in the findings of 4modes_3sin2t_smear_1.png

the Modes refer to the 'resampling' of the energy (E) and/or track/cascade (T). Resampling refers to the smearing of the truth into prediction and works in the following way.

First, bin the True energy into 40 bins: (40 because MCEq works with 40 bins, and thus the weights are for each of the 40 bins).

then, for each event in the bin, collect the predicted energies (by a GNN [see GNN_ET]). This these predicted values are the uncertainty of the reconstruction. So, to smear it, for each event in the bin take a random predicted energy of the collection, as the energy. Each event keeps its original weight and track_mu_pred value. That is how the energy smearing works.

The track smearing also works per true energy bin, but smears the track_mu (truth) with the track_mu_pred instead. 

That is what the sin2w=0.222 line does, as that is the true sine^w(weinberg angle). The other lines are 'What if sine2theta was this value instead'.  If s2t was smaller (bigger), there would be more (less) NC events, compared to CC events. So before the resampling the events are weighed to include this ratio change. 

The idea is to get the GNNs to be better, such that smearing is less, and to run them on data, so that we can include a data line with hopefully the same shape as the resampled MCs. Then there will be one sine2theta which is closest to the dataline, which will be the 'correct' value according to data.


All that is in ST_final.ipynb.
In order for that to run, MCEq_fluxes.py makes mceq_zenith_averaged_fluxes.csv for weighing, and combine_E_T.py takes the best GNN_E and GNN_T models (see \GNN_ET) and gets the MC data. 

ST_old.ipynb and ST_investigation.ipynb are old versions of ST_final, that only exist for refernce