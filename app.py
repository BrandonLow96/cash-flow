from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import json
import config_data as cfd
from xlwings.constants import InsertShiftDirection
import xlwings as xw
from datetime import date

app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'ADs85gWZUB8pE2vdhoknSsG7xEtPk6Pt'


@app.route("/", methods=["GET"])
def index():
    return redirect("/configuration")


@app.route('/configuration', methods=['GET', 'POST'])
def config():
    # POST request
    if request.method == 'POST':
        data = {
            "project_name": request.form.get("project-name"),
            "project_name": request.form.get("project-name"),
            "company-name": request.form.get("company-name"),
            "ciq_id": request.form.get("ciq-id"),
            "val_date": request.form.get("val-date"),
            "forecast_periods": request.form.get("forecast-periods"),
            "forecasting_model": request.form.get("forecasting-model"),
            "source_forecasts": request.form.get("source-forecasts")
        }

        return redirect(url_for('.download', data=json.dumps(data)))

    # GET request
    else:
        # serialize and use JSON headers
        return render_template('index.html')


@app.route('/download', methods=['GET'])
def download():
    json_string = request.args.get('data')
    data = json.loads(json_string)
    data = cfd.data  # To delete once wired

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
            sheet.range(str(row_src + i - 1) + ":" +
                        str(row_src + i - 1)).copy()
            sheet.range(str(row_src + i) + ":" +
                        str(row_src + i)).paste("formulas")

    def create_model(data):

        # Write title and assumptions
        named_ranges = ['ciq_id', 'val_date', 'g', 't', 'beta_date', 'reporting_type',
                        'filing_mode', 'curr', 'conv_mode', 'hist_data_start', 'forecast_date',
                        'forecast_start', 'use_ciq_forecast', 'r_override', 'rf', 'erp', 'pre_tax_rd',
                        'debt_ratio', 'gearing_measure', 'beta_freq', 'index', 'index_id']

        # Initialise workbook
        # xw.App().visible = False

        if data["forecasting_model"] == 2:
            model_template = 'templates\dcf_model_2p_blank.xlsx'
        else:
            model_template = 'templates\dcf_model_3p_blank.xlsx'

        wb = xw.Book(model_template)
        asm_sht = wb.sheets['Assumptions']
        dcf_sht = wb.sheets['DCF']
        fcs_sht = wb.sheets['Forecasts']
        is_sht = wb.sheets['IS']
        bs_sht = wb.sheets['BS']
        cfs_sht = wb.sheets['CFS']
        beta_sht = wb.sheets['Beta']
        comp_sht = wb.sheets['Comps']

        print("Initialised workbook...")

        # Copy title and assumptions
        for name in named_ranges:
            asm_sht.range(name).value = data[name]

        for sheet in wb.sheets:
            sheet.range('B4').value = data["project_name"]
            sheet.range('B5').value = "Valuation of " + data["company_name"]
            sheet.range('B7').value = "Date: " + \
                date.today().strftime("%d %B %Y")

        print("Copied titles and assumptions...")

        # Structural changes
        if data["forecasting_model"] == 3:
            update_col(dcf_sht, "J", "K", data["forecast_periods_extr"], 1)
            update_col(dcf_sht, "G", "H", data["forecast_periods_proj"], 3)
        else:
            update_col(dcf_sht, "G", "H", data["forecast_periods"], 3)
            dcf_sht.range("53:54").delete(shift="up")
            dcf_sht.range("16:20").delete(shift="up")

        print("Configured DCF sheet...")

        update_col(fcs_sht, "G", "H", data["forecast_periods"], 2)

        for i in (is_sht, bs_sht, cfs_sht):
            update_col(i, "G", "H", data["hist_periods"], 2)

        print("Configured data input sheets...")

        update_comps(beta_sht, 60, len(data["comps"]))

        for i in range(0, len(data["comps"])):
            row_num = 60 + i
            beta_sht.range("C" + str(row_num)).value = data["comps"][i]

        update_comps(beta_sht, 21, len(data["comps"]))
        beta_sht.range(str(21 + len(data["comps"])) + ":" +
                       str(21 + len(data["comps"]))).api.Delete()

        update_comps(beta_sht, 97 + 2 *
                     (len(data["comps"]) - 1), len(data["comps"]))
        update_comps(beta_sht, 72 + 2 *
                     (len(data["comps"]) - 1), len(data["comps"]))
        update_comps(beta_sht, 104 + 4 *
                     (len(data["comps"]) - 1), len(data["comps"]))

        print("Configured beta...")

        update_comps(comp_sht, 39, len(data["comps"]))

        for i in range(0, len(data["comps"])):
            row_num = 39 + i
            comp_sht.range("C" + str(row_num)).value = data["comps"][i]

        comp_sht.range(str(39 + len(data["comps"])) + ":" +
                       str(39 + len(data["comps"]))).api.Delete()

        print("Configured comps...")

        # Export and save
        wb.save(r'dcf_model_output.xlsx')
        wb.close()

        print("Done!")

    create_model(data)

    return render_template('download.html')


if __name__ == "__main__":
    app.run()
