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