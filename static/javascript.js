// Format Javascript Date as YYYY-MM-DD
function formatDate(date) {
    var d = new Date(date),
        month = "" + (d.getMonth() + 1),
        day = "" + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;

    return [year, month, day].join("-");
}

// Disable year input for financial-year-end
var year = 9999;
document.getElementById("financial-year-end").setAttribute("min", year + "-01-01");
document.getElementById("financial-year-end").setAttribute("max", year + "-12-31");

// Copy financial year-end date and month to historical period start / end
document.getElementById("financial-year-end").onchange = function () {
    var date = new Date(this.value);

    var periodEnd = new Date(document.getElementById("historical-period-end").value);
    periodEnd.setMonth(date.getMonth());
    periodEnd.setDate(date.getDate());
    document.getElementById("historical-period-end").value = formatDate(periodEnd);

    date.setDate(date.getDate() + 1);

    var periodStart = new Date(document.getElementById("historical-period-start").value);
    periodStart.setMonth(date.getMonth());
    periodStart.setDate(date.getDate());
    document.getElementById("historical-period-start").value = formatDate(periodStart);
};

document.getElementById("historical-period-start").onchange = function () {
    var date = new Date(document.getElementById("financial-year-end").value);
    date.setDate(date.getDate() + 1);

    var periodStart = new Date(this.value);
    periodStart.setMonth(date.getMonth());
    periodStart.setDate(date.getDate());
    this.value = formatDate(periodStart);
};

document.getElementById("historical-period-end").onchange = function () {
    var date = new Date(document.getElementById("financial-year-end").value);

    var periodEnd = new Date(this.value);
    periodEnd.setMonth(date.getMonth());
    periodEnd.setDate(date.getDate());
    this.value = formatDate(periodEnd);
};