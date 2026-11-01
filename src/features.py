TARGET = "koi_disposition"
POSITIVE_LABEL = "CONFIRMED"
NEGATIVE_LABEL = "FALSE POSITIVE"
GROUP = "kepid"

#core features and their units which all exist before any vetting decision
FEATURE_UNITS = {
    "koi_period": "days",
    "koi_duration": "hours",
    "koi_depth": "ppm",
    "koi_impact": "dimensionless",
    "koi_model_snr": "dimensionless",
    "koi_num_transits": "count",
    "koi_prad": "Earth radii",
    "koi_teq": "K",
    "koi_insol": "Earth flux",
    "koi_steff": "K",
    "koi_slogg": "log10(cm/s^2)",
    "koi_srad": "Solar radii",
    "koi_kepmag": "mag",
}
CORE_FEATURES = list(FEATURE_UNITS)

#already on a log scale so they are not log transformed
LINEAR_FEATURES = ["koi_slogg", "koi_kepmag"]

#kept out of the main model and tested separately
SENSITIVITY_FEATURES = ["koi_count"]

#vetting outputs or values only known after vetting
LEAKY_COLUMNS = {
    "koi_pdisposition": "Kepler pipeline disposition (vetting output)",
    "koi_score": "disposition score (vetting output)",
    "koi_fpflag_nt": "false-positive flag (vetting output)",
    "koi_fpflag_ss": "false-positive flag (vetting output)",
    "koi_fpflag_co": "false-positive flag (vetting output)",
    "koi_fpflag_ec": "false-positive flag (vetting output)",
    "koi_comment": "vetting comment text",
    "koi_disp_prov": "disposition provenance",
    "koi_vet_stat": "vetting status",
    "koi_vet_date": "vetting date",
    "kepler_name": "only assigned once a planet is confirmed",
}

#every column starting with one of these is dropped
LEAKY_PREFIXES = {
    "koi_steff_err": "stellar uncertainty reflects follow-up effort",
    "koi_smass_err": "stellar uncertainty reflects follow-up effort",
    "koi_smet": "metallicity mostly measured during follow-up",
    "koi_dikco_": "centroid diagnostic (feeds koi_fpflag_co)",
    "koi_dicco_": "centroid diagnostic (feeds koi_fpflag_co)",
    "koi_fwm_": "centroid diagnostic (feeds koi_fpflag_co)",
}

ID_COLUMNS = ["kepid", "kepoi_name", "ra_str", "dec_str"]


#true if a column is on the leakage drop list by name or prefix
def is_leaky(column):
    return column in LEAKY_COLUMNS or column.startswith(tuple(LEAKY_PREFIXES))
