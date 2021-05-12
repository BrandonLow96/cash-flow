# Model configuration
from datetime import datetime

data = {
    "project_name": "Project Open Source",
    "company_name": "VISA",
    "ciq_id": "NYSE:V",

    "val_date": datetime(2017, 12, 18),
    "g": 0.02,
    "t": 0.25,

    "reporting_type": "LFR",
    "filing_mode": "P",
    "curr": "USD",
    "conv_mode": "H",

    "forecasting_model": 2,  # 2 : Two-period; 3 : Three-period

    "hist_data_start": datetime(2016, 12, 31),
    "forecast_date": datetime(2017, 12, 18),
    "forecast_start": datetime(2018, 12, 31),
    "forecast_periods": 4,  # minimum of 2
    "use_ciq_forecast": "Yes",

    "r_override": None,
    "rf": 0.018,
    "erp": 0.06,
    "pre_tax_rd": 0.12,
    "debt_ratio": 0.3,

    "beta_date": datetime(2019, 12, 1),
    "gearing_measure": "Net Debt",
    "beta_freq": "W",
    "index": "MSCI World",
    "index_id": "IQ2668622",

    "comps": ["IQ6477196", "IQ92001"],

    # Structural parameters
    "hist_periods": 3,  # minimum of 2
    "forecast_periods_proj": 4,  # minimum of 3
    "forecast_periods_extr": 4  # minimum of 1, excludes terminal period

}
