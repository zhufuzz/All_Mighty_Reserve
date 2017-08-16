function checkDateTime(){
    var myDate=new Date();
    date = document.getElementById("date").value;
    myDate.setDate(date);

    var today = new Date();

    if (myDate>today) {
        alert("Today is before 9th August 2008");
    }
    else{
        alert("Today is after 9th August 2008");
    }
}


function checkName_reload(){
    var name = document.getElementById("name").value;
    if(name.trim() == ""){
        alert("name can not be empty");
// {#                location.reload();#}
    }
}

function checkName(){
    var name = document.getElementById("name").value;
    if(name.trim() == ""){
        alert("name can not be empty");
    }
}


function checkDate(){
    var dateStr = document.getElementById("date").value;
    myDate = new Date(Date.parse(dateStr))
    var today = new Date();
    if (myDate<today) {
        alert("Ivalid Input: You can only create resources start after today!!!");
// {#                location.reload();#}
    }
}


function checkTime(){
    var startTimeStr = document.getElementById("startTime").value;
    if(startTimeStr.length === 0){
        alert("startTime input is null!");
        return;
    }
    var endTimeStr = document.getElementById("endTime").value;
    if(endTimeStr.length === 0){
        alert("endTime input is null!");
        return;
    }
    var startTime = parseInt(startTimeStr.replace(':',''));
    var endTime = parseInt(endTimeStr.replace(':',''));

    if (endTime<startTime) {
        alert("Ivalid Input: Start Time should be after End Time.");
// {#                location.reload();#}
    }

}


function try_altert(){
     alert("try_altert");
}