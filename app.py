from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET"])
def index():
    return redirect("/configuration")


@app.route('/configuration', methods=['GET', 'POST'])
def config():
    # POST request
    if request.method == 'POST':
        data = {}
        data['project_name'] = request.form.get("project-name")
        data['company-name'] = request.form.get("company-name")
        data['ciq_id'] = request.form.get("ciq-id")
        data['val_date'] = request.form.get("val-date")
        data['forecast_periods'] = request.form.get("forecast-periods")
        data['forecasting_model'] = request.form.get("forecasting-model")
        data['source_forecasts'] = request.form.get("source-forecasts")
        return render_template("download.html", message=data)

    # GET request
    else:
        # serialize and use JSON headers
        return render_template("index.html")
