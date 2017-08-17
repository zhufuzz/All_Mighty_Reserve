
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

function checkResourceDuratation() {
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

//
// function checkReservationStartDateTime(resourceStartDateTime, resourceEndDateTime) {
//     var reservationStartTimeStr = document.getElementById("reservationStartTime").value;
//
//     reservationStartTime = new Date(Date.parse(reservationStartTimeStr));
//     // var today = new Date();
//
//     if (reservationStartTime < resourceStartDateTime) {
//         document.getElementById("reservationStartTime").value = null;
//         alert("Ivalid Input: Reservation must start after resource start time!!!");
//     }
//
//     if (reservationStartTime > resourceEndDateTime) {
//         document.getElementById("reservationStartTime").value = null;
//         alert("Ivalid Input: Reservation must end before resource end time!!!");
//     }
// }


function checkReservationStartDateTime(resourceStartDateTimeStr, resourceEndDateTimeStr) {
    var reservationStartTimeStr = document.getElementById("reservationStartTime").value;

    reservationStartTime = new Date(Date.parse(reservationStartTimeStr));

    resourceStartDateTime = new Date(Date.parse(resourceStartDateTimeStr));
    resourceEndDateTime = new Date(Date.parse(resourceEndDateTimeStr));

    // var today = new Date();

    if (reservationStartTime < resourceStartDateTime) {
        document.getElementById("reservationStartTime").value = null;
        alert("Ivalid Input: Reservation must start after resource start time!!!");
    }

    if (reservationStartTime > resourceEndDateTime) {
        document.getElementById("reservationStartTime").value = null;
        alert("Ivalid Input: Reservation must end before resource end time!!!");
    }
}

function checkReservationEndDateTime(resourceStartDateTimeStr, resourceEndDateTimeStr) {
    var reservationEndTimeStr = document.getElementById("reservationEndTime").value;

    reservationEndTime = new Date(Date.parse(reservationEndTimeStr));

    resourceStartDateTime = new Date(Date.parse(resourceStartDateTimeStr));
    resourceEndDateTime = new Date(Date.parse(resourceEndDateTimeStr));

    if (reservationEndTime < resourceStartDateTime) {
        document.getElementById("reservationEndTime").value = null;
        alert("Ivalid Input: Reservation must start after resource start time!!!");
    }

    if (reservationEndTime > resourceEndDateTime) {
        document.getElementById("reservationEndTime").value = null;
        alert("Ivalid Input: Reservation must end before resource end time!!!");
    }
}





