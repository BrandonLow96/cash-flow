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
        return render_template("download.html", data=data)

    # GET request
    else:
        # serialize and use JSON headers
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
