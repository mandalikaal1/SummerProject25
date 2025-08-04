//global variables
var tableAttributes; 

// select view for testing - only for temporary viewing
const selectButton = document.getElementById("select");
selectButton.addEventListener('click', function () {

    const dropdown = document.getElementById("user");
    const selectedValue = dropdown.value; // Gets the value of the selected option

    //load attributes
    tableAttributes = new Array();
    loadAttributes(selectedValue);


    //load top 20 of table
    viewData(selectedValue);


});

function loadAttributes(userVal) {
    //select user role
    const selectedValue = userVal;

    // views based on user 

    if (selectedValue == "Admin") {
        tableAttributes.push("Name", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission",
            "Doctor", "Hospital", "Billing Amount", "Room Number", "Admission Type", "Discharge Date", "Medication",
            "Test Results");

    }
    else if (selectedValue == "Doctor") {
        tableAttributes.push("Name", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission",
            "Hospital", "Discharge Date", "Medication", "Test Results");


    }
    else if (selectedValue == "Patient") {
        tableAttributes.push("Name", "Date of Admission", "Doctor", "Discharge Date", "Medication", "Test Results");

    }
    else {
    }


}


function viewData(userVal) {
    fetch('/retrieve_data') // Path to JSON file
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })

        .then(data => {

           

            const contentTitle = document.getElementById('data-title');
            const contentDiv = document.getElementById('data-body');
            contentTitle.innerHTML = '';
            contentDiv.innerHTML = '';


            const row = document.createElement('tr');

            tableAttributes.forEach(item => {
                const top = document.createElement('th');
                top.textContent = item;
                top.classList.add("col");
                row.appendChild(top);


            });
            contentTitle.appendChild(row);



            const slicedData = data.patients.slice(0, 30); // Extracts the first 20 elements
            slicedData.forEach(item => {
                const row = document.createElement('tr');


                for (let i = 0; i < tableAttributes.length; i++) {
                    let nameCell = document.createElement('td');
                    if (tableAttributes[i] == "Name") {
                        let fixName = toSentenceCase(item[tableAttributes[i]]);
                        nameCell.textContent = fixName;
                    }
                    else if (tableAttributes[i] == "Billing Amount") {
                        let amount = parseFloat(item[tableAttributes[i]]);
                        nameCell.textContent = amount.toFixed(2);

                    }
                    else {
                        nameCell.textContent = item[tableAttributes[i]];

                    }

                    nameCell.classList.add("col"); //column class for css
                    nameCell.classList.add("text-nowrap");  //no-wrap

                    row.appendChild(nameCell);

                };

                contentDiv.appendChild(row);

            })

        })
}


function toSentenceCase(str) {

    if (!str) {
        return ""; // Handle empty or null strings
    }

    // Convert the entire string to lowercase first
    const lowerStr = str.toLowerCase();
    const names = lowerStr.split(' ');

    // Capitalize the first letter and concatenate with the rest of the lowercase string
    return names[0].charAt(0).toUpperCase() + names[0].slice(1) + "\n" + names[1].charAt(0).toUpperCase() + names[1].slice(1);

}
