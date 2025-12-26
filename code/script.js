function calculateBill() {
    let units = parseFloat(document.getElementById("units").value);
    let type = document.getElementById("type").value;
    let bill = 0;

    if (isNaN(units) || units <= 0) {
        document.getElementById("result").innerHTML =
            "Please enter valid units.";
        return;
    }

    if (type === "domestic") {
        if (units <= 100) bill = units * 3;
        else if (units <= 200) bill = (100 * 3) + (units - 100) * 5;
        else bill = (100 * 3) + (100 * 5) + (units - 200) * 7;
    } else {
        bill = units * 8; // commercial rate
    }

    document.getElementById("result").innerHTML =
        "Estimated Electricity Bill: ₹" + bill.toFixed(2);
}
