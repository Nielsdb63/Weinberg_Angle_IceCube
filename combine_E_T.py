import argparse
import os
import sys
import pandas as pd
import numpy as np


def load_and_merge(energy_csv: str, track_csv: str) -> pd.DataFrame:
	# Required fixed column names per user specification
	energy_required = ["event_no", "energy_pred", "energy"]
	track_required = ["event_no", "pid", "track_mu", "track_mu_pred", "interaction_type"]

	e_df = pd.read_csv(energy_csv, usecols=lambda c: c in energy_required)
	t_df = pd.read_csv(track_csv, usecols=lambda c: c in track_required)

	# Validate presence
	missing_e = [c for c in energy_required if c not in e_df.columns]
	missing_t = [c for c in track_required if c not in t_df.columns]
	if missing_e:
		raise KeyError(f"Energy CSV missing columns: {missing_e}")
	if missing_t:
		raise KeyError(f"Track CSV missing columns: {missing_t}")

	# Drop rows with missing required values
	e_df = e_df.dropna(subset=energy_required)
	t_df = t_df.dropna(subset=track_required)

	# Merge on event_no only (pid taken from track CSV)
	merged = pd.merge(e_df, t_df, on="event_no", how="inner", suffixes=("_E", "_T"))

	# Construct the desired output schema
	out = pd.DataFrame({
		"event_no": merged["event_no"],
		"pid": merged["pid"],
		"interaction_type": merged["interaction_type"],
		"track_mu": merged["track_mu"],
		"energy": merged["energy"],
		"track_mu_pred": merged["track_mu_pred"],
		"energy_pred": merged["energy_pred"],
	})

	# Enforce numeric types where appropriate
	for c in ("event_no", "pid", "track_mu"):
		out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")
	for c in ("energy", "track_mu_pred", "energy_pred"):
		out[c] = pd.to_numeric(out[c], errors="coerce")

	out = out.dropna(subset=["event_no", "pid", "track_mu", "energy", "track_mu_pred", "energy_pred", "interaction_type"]).copy()
	out = out[["event_no", "pid", "track_mu", "energy", "track_mu_pred", "energy_pred", "interaction_type"]]
	return out


def main():

	energy_csv = '/groups/icecube/nielsdb/GNN_ET/validation/Energy/GNN_E_val_prediction_GNN_ET_MC_2M_161125.csv'
	track_csv = '/groups/icecube/nielsdb/GNN_ET/validation/Track/GNN_T_val_prediction_GNN_ET_MC_2M_111125.csv'
	
	if not os.path.exists(energy_csv):
		print(f"Energy CSV not found: {energy_csv}", file=sys.stderr)
		sys.exit(2)
	if not os.path.exists(track_csv):
		print(f"Track CSV not found: {track_csv}", file=sys.stderr)
		sys.exit(2)

	out_df = load_and_merge(energy_csv, track_csv)
	
    #naming convention: combined_ET_val_prediction_<db_name_of_E_T>_<energy_file_id>_<track_file_id>.csv
	out_path = '/groups/icecube/nielsdb/SinTheta_Aug2025/combined_ET_val_prediction_GNN_ET_MC_2M_161125_111125.csv'

	out_df.to_csv(out_path, index=False)
	print(f"Wrote combined CSV: {out_path}  (rows: {len(out_df):,})")


if __name__ == "__main__":
	main()

