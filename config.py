from xlwings.constants import InsertShiftDirection
import xlwings as xw
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator

# Define functions


def update_col(sheet, col_src, col_dest, cols, cols_limit):
    if cols == cols_limit:
        sheet.range(col_src + ":" + col_src).delete(shift="left")
    else:
        for i in range(1, cols - cols_limit):
            sheet.range(col_dest + ":" + col_dest).insert(shift="right",
                                                          copy_origin="format_from_left_or_above")
            sheet.range(
                col_src + ":" + col_dest).formula = sheet.range(col_src + ":" + col_src).formula
            sheet.range(col_src + ":" + col_src).copy()
            sheet.range(col_dest + ":" + col_dest).paste("formats")


def update_comps(sheet, row_src, rows):
    for i in range(1, rows):
        sheet.range(str(row_src + i) + ":" + str(row_src + i)).insert(
            shift="down", copy_origin="format_from_left_or_above")
        sheet.range(str(row_src + i - 1) + ":" + str(row_src + i - 1)).copy()
        sheet.range(str(row_src + i) + ":" +
                    str(row_src + i)).paste("formulas")


# Model configuration
case_name = "Alpha v Beta"
expert_name = "Mark Bezant"

ciq_id = "NYSE:FCN"
val_date = datetime(2017, 12, 18)
g = 0.02
t = 0.25

reporting_type = "LFR"
filing_mode = "P"
curr = "USD"
conv_mode = "H"

hist_data_start = datetime(2016, 12, 31)

forecast_date = datetime(2017, 12, 18)
forecast_start = datetime(2018, 12, 31)
forecast_periods = 4  # minimum of 2
use_ciq_forecast = "Yes"

r_override = None
rf = 0.018
erp = 0.06
pre_tax_rd = 0.12
debt_ratio = 0.3

beta_date = datetime(2019, 12, 1)
gearing_measure = "Net Debt"
beta_freq = "W"
index = "MSCI World"
index_id = "IQ2668622"

comps = ["IQ22615883", "IQ7827924", "IQ24947391", "IQ7685249", "IQ217503",
         "IQ117027181", "IQ882187", "IQ216463", "IQ879091", "IQ8690249"]

# Structural parameters
hist_periods = 3  # minimum of 2
forecast_periods_proj = 4  # minimum of 3
forecast_periods_extr = 4  # minimum of 1, excludes terminal period


# Load workbook
wb = load_workbook("templates\dcf_model_blank.xlsx", data_only=False)

# Write title and assumptions
named_ranges = ['ciq_id', 'val_date', 'g', 't', 'beta_date', 'reporting_type',
                'filing_mode', 'curr', 'conv_mode', 'hist_data_start', 'forecast_date',
                'forecast_start', 'use_ciq_forecast', 'r_override', 'rf', 'erp', 'pre_tax_rd',
                'debt_ratio', 'gearing_measure', 'beta_freq', 'index', 'index_id']


# Initialise workbook
xw.App().visible = False

wb = xw.Book('templates\dcf_model_blank.xlsx')
asm_sht = wb.sheets['Assumptions']
dcf_sht = wb.sheets['DCF']
fcs_sht = wb.sheets['Forecasts']
is_sht = wb.sheets['IS']
bs_sht = wb.sheets['BS']
cfs_sht = wb.sheets['CFS']
beta_sht = wb.sheets['Beta']
comp_sht = wb.sheets['Comps']


# Copy title and assumptions
for name in named_ranges:
    asm_sht.range(name).value = eval(name)

for sheet in wb.sheets:
    sheet.range('B4').value = case_name
    sheet.range('B5').value = "Expert Report of " + expert_name

# Structural changes
update_col(dcf_sht, "J", "K", forecast_periods_extr, 1)
update_col(dcf_sht, "G", "H", forecast_periods_proj, 3)
update_col(fcs_sht, "G", "H", forecast_periods, 2)

for i in (is_sht, bs_sht, cfs_sht):
    update_col(i, "G", "H", hist_periods, 2)

update_comps(beta_sht, 60, len(comps))

for i in range(0, len(comps)):
    row_num = 60 + i
    beta_sht.range("C" + str(row_num)).value = comps[i]

update_comps(beta_sht, 21, len(comps))
beta_sht.range(str(21 + len(comps)) + ":" + str(21 + len(comps))).api.Delete()

update_comps(beta_sht, 97 + 2 * (len(comps) - 1), len(comps))
update_comps(beta_sht, 72 + 2 * (len(comps) - 1), len(comps))
update_comps(beta_sht, 104 + 4 * (len(comps) - 1), len(comps))

update_comps(comp_sht, 39, len(comps))

for i in range(0, len(comps)):
    row_num = 39 + i
    comp_sht.range("C" + str(row_num)).value = comps[i]

comp_sht.range(str(39 + len(comps)) + ":" + str(39 + len(comps))).api.Delete()


# Export and save
wb.save(r'U:\Day Files\Yeung, Park\2. Business development\Capital IQ BD\capiq-bd\dcf_model_output.xlsx')
wb.close()
