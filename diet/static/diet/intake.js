count = 0;
intake_li = [];

document.addEventListener('DOMContentLoaded', () => {

    try {
        // Add listener for add and delete button every row in form
        document.querySelector(".add-row").onclick = () => add_row(document.querySelector(".add-row").parentElement.parentElement);
        document.querySelector('.delete-row').onclick = () => delete_row(document.querySelector(".delete-row").parentElement.parentElement);
        document.querySelector('#result-view').hidden = true;

        document.querySelector('#verify-form').onclick = () => validate_form();
        document.querySelector('#submit-form').onclick = () => result_view(
            document.querySelector('#intake-form').dataset.type
        );
    } finally {}
});

function result_view(type) {
    document.querySelector('#result-view').hidden = false;
    document.querySelector('.form-view').hidden = true;
    intake_calculate(type);
}

function intake_calculate(type) {
    // Get the intake result
    fetch(`/diet/intake/calc/${type}`, {
        method: 'POST',
        body: JSON.stringify({
            intake_amt: intake_li
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        // Fill in the graph and range
        tbody = document.querySelector('#table-body');

        for (let i = 0; i < result["group_names"].length; i++) {

            // For graph
            const row = document.createElement('tr');
            row.innerHTML = `<th scope="row">${i+1}</th>\n
            <td>${intake_li[i]["name"]}</td>\n
            <td>${result["group_names"][i]}</td>\n
            <td>${result["subgroup_names"][i]}</td>\n
            <td>${intake_li[i]["amt"]}</td>`;
            tbody.append(row);
        }

        // Fill the record form
        document.querySelector('#vf').value = result["chart_list"][0];
        document.querySelector('#protein').value = result["chart_list"][1];
        document.querySelector('#grain').value = result["chart_list"][2];
        document.querySelector('#other').value = result["chart_list"][3];
        document.querySelector('#liquid').value = result["liquid_amt"];


        // Fill in the chart
        xVals = ["Vegies and Fruits", "Protein", "Whole Grain", "Others"];
        yVals = result["chart_list"];
        barColors = ["#AC92EB", "#4FC1E8", "#A0D568", "#ED5564"];

        new Chart("intakeChart", {
            type: "pie",
            data: {
                labels: xVals,
                datasets: [{
                    backgroundColor: barColors,
                    data: yVals
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Your Daily Intake"
                }
            }
        });

        // Create sample for comparison
        new Chart("sampleIntakeChart", {
            type: "pie",
            data: {
                labels: xVals,
                datasets: [{
                    backgroundColor: barColors,
                    data: [50, 25, 25, 0]
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Healthy Daily Intake Ratio Sample"
                }
            }
        });
    });
}

function validate_form() {

    // If user confirmed
    if (window.confirm("Data cannot be modified after you click the OK button.")){
        // Get the form rows
        rows = document.querySelector('#intake-form').children;
        for (let row of rows) {

            try {
                // Check for last row of buttons
                if (row.children[1].children[0].tagName === 'BUTTON') {
                } else {
                    name = row.children[0].children[0].value;
                    amt = row.children[1].children[0].value;

                    // Check the selected option
                    if (name === "default") {
                        alert('Please choose a food');
                        return false;
                    } 

                    // Check the input amount
                    if ((amt === '') || (parseInt(amt) < 0)) {
                        alert('Intake amount must be larger than 0 g');
                        return false;
                    }

                    intake_li.push({
                        'name': name,
                        'amt': amt
                    })
                }
            } catch {}

        }

        // Disable the verify button
        document.querySelector('#verify-form').classList.add('disabled', 'btn-secondary');
        document.querySelector('#verify-form').innerHTML = "Verified";

        // Enable submit button
        document.querySelector('#submit-form').classList.remove('disabled');
    } else {}

    
    
}

function add_row(current_row) {

    // Copy a row and insert under current row
    clone = current_row.cloneNode(true);
    current_row.after(clone);

    count++;

    new_row = document.querySelector("#intake-form").children[count];
    new_row.children[1].children[0].innerHTML = 0;
    add_button = new_row.children[2].children[0];
    del_button = new_row.children[2].children[1];
    del_button.classList.remove("disabled");
    add_button.onclick = () => add_row(new_row);
    del_button.onclick = () => delete_row(new_row);
    
    // Remove the buttons from current row
    current_row.querySelector('.btn-group').style.visibility = "hidden";

}

function delete_row(current_row) {


    // Set the last button-group as visible if current row is the last row
    child_index = Array.prototype.indexOf.call(current_row.parentElement.children, current_row)
    if (child_index === count) {
        last_row = document.querySelector('#intake-form').children[count-1];
        last_row.querySelector('.btn-group').style.visibility = "visible";

        // Reattach listener (Change the current_row var)
        add_button = last_row.children[2].children[0];
        del_button = last_row.children[2].children[1];
        add_button.onclick = () => add_row(last_row);
        del_button.onclick = () => delete_row(last_row);
    }

    // Disable the delete button if only two rows of the form left
    if (count === 1) {
        document.querySelector('#intake-form').children[0].children[2].children[1].classList.add('disabled');
    }

    current_row.remove();
    count--;

}