
function checkResourceStartDateTime() {
    var dateStr = document.getElementById("startDateTime").value;
    myDate = new Date(Date.parse(dateStr));
    var today = new Date();
    if (myDate < today) {
        document.getElementById("startDateTime").value = null;
        alert("Ivalid Input: You can only create resources start later than now!!!");
    }
}

function checkResourceEndDateTime() {
    var dateStr = document.getElementById("endDateTime").value;
    myDate = new Date(Date.parse(dateStr));
    var today = new Date();
    if (myDate < today) {
        document.getElementById("endDateTime").value = null;
        alert("Ivalid Input: You can only create resources start later than now!!!");
    }
}

function checkDuratation() {
    var startStr = document.getElementById("startDateTime").value;
    var endStr = document.getElementById("endDateTime").value;
    start = new Date(Date.parse(startStr));
    end = new Date(Date.parse(endStr));
    if (end - start <= 0) {
        document.getElementById("endDateTime").value = null;
        alert("Ivalid Input: End Time should be after Start Time.");
    }
}

function checkInt(){
    var intInput = document.getElementById("intInput").value;

    if(!Number.isInteger(parseInt(intInput)) || parseInt(intInput) <= 0){
        document.getElementById("intInput").value = null;
        alert("Ivalid Input: Input must be Integer larger than 0.");
    }
}



