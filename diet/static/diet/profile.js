document.addEventListener('DOMContentLoaded', () => {

    // Add listener for search buttons
    try {
        document.querySelector('select').onchange = () => search_record(
            document.querySelector('select').value
        );

        document.querySelector('#chartBtn').onclick = () => load_chart();
    } catch (error) {}
});

function load_chart() {

    length = document.querySelector('tbody').children.length;
    labels = [];
    datasets = [];
    data_labels = ["Vegetables & Fruits", "Protein", "Grain", "Liquid", "Others"];
    border_colors = ['79, 0, 11', '114, 0, 38', '206, 66, 87', '255, 127, 81', '255, 155, 84'];
    data_datas = [[],[],[],[],[]]
    for (let i = 1; i <= length; i++) {
        labels.push(i);
        data_datas[0].push(document.querySelector('tbody').children[i-1].children[2].innerHTML);
        data_datas[1].push(document.querySelector('tbody').children[i-1].children[3].innerHTML);
        data_datas[2].push(document.querySelector('tbody').children[i-1].children[4].innerHTML);
        data_datas[3].push(document.querySelector('tbody').children[i-1].children[5].innerHTML);
        data_datas[4].push(document.querySelector('tbody').children[i-1].children[6].innerHTML);
    }
    for (let i = 0; i < 5; i++) {
        const data = {
            label: data_labels[i],
            data: data_datas[i],
            fill: true,
            backgroundColor: 'rgba(' + border_colors[i] + ', 0.2)',
            borderColor: 'rgb(' + border_colors[i] + ')',
            pointBackgroundColor: 'rgb(' + border_colors[i] + ')',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(' + border_colors[i] + ')'
        }
        datasets.push(data);
    }
    const data = {
        labels: labels,
        datasets: datasets
      }
    
    const config = {
    type: 'line',
    data: data,
    options: {
        elements: {
        line: {
            borderWidth: 3
            }
        }
    },
    };

    new Chart(canvas, config);
}

function search_record(val1) {

    input = document.querySelector('#searchInput').value;

    if (/^\d+$/.test(input)) {

        if (input[0] === '0') {
            input = input.substring(1, input.length);
        }

        try {
            input = parseInt(input);
        } catch (error) {
            alert("Input is not valid");
            return false;
        }

        // Check validity of data
        if (val1 === 'date') {
            if (input < 0 || input > 31) {
                alert("Date input is not valid");
                return false;
            }

            if (input < 10) {
                document.querySelector('#searchInput').value = '0' + input;
            }
        } 
        
        if (val1 === 'month') {
            if (input < 0 || input > 12) {
                alert("Month input is not valid");
                return false;
            }

            if (input < 10) {
                document.querySelector('#searchInput').value = '0' + input;
            }
        }

        if (val1 === 'year') {
            if (input < 0 || input.toString().length > 4) {
                alert("Year input is not value");
                return false;
            }
        }
    } else {
        alert("Input must contain only digits.");
        return false;
    }

    // Enable search button
    document.querySelector('#searchButton').classList.remove("disabled");
    // Fulfill form action
    document.querySelector('form').action = `/diet/profile/search?val=0&type=${val1}&searchInput=${input}&page=1`
}