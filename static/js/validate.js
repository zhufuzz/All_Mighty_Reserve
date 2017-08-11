    function checkValidations() {
        var resourceName = document.getElementById("resourceName").value;

        var d = new Date();
        var getMonth = document.getElementById("Month").value;
        var getDay = document.getElementById("Day").value;
        var getYear = document.getElementById("Year").value;
        var getsHours = document.getElementById("startHours").value;
        var getsMins = document.getElementById("startMins").value;

        var sMeridian = document.getElementById("startMeridian").value;
        var intsHours = parseInt(getsHours);

        if(sMeridian == 'PM'){
            intsHours = intsHours + 12;
            getsHours = intsHours;
        }

        if(getsHours.length == 1){
            getsHours = '0'+getsHours;
        }
        if(getsMins.length == 1){
            getsMins = '0'+getsMins;
        }

        var geteHours = document.getElementById("endHours").value;
        var eMeridian = document.getElementById("endMeridian").value;
        var inteHours = parseInt(geteHours);

        if(eMeridian == 'PM'){
            inteHours = inteHours + 12;
            geteHours = inteHours;
        }
        if(geteHours.length == 1){
            geteHours = '0'+geteHours;
        }

        var geteMins = document.getElementById("endMins").value;
        if(geteMins.length == 1){
            geteMins = '0'+geteMins;
        }

        var getStartDateString = getYear + '-' +getMonth +'-'+getDay+' '+getsHours+':'+getsMins+':00';
        var myStartDate = new Date(getStartDateString);

        var getEndDateString = getYear + '-' +getMonth +'-'+getDay+' '+geteHours+':'+geteMins+':00';
        var myEndDate = new Date(getEndDateString);
        if(myStartDate < d){
            var message = "Date should be greater than current date";
            document.getElementById("displayError").innerHTML = message;
            return false;
        }else {
            if(myEndDate < myStartDate){
            var message = "End time should be greater than Start time";

            document.getElementById("displayError").innerHTML = message;
                return false;
            }
            else {
                return true;
            }
        }
    };

    function checkReserveValidations() {
        var d = new Date();

        getStartHours = document.getElementById("rstartHours").value;
        getStartMins = document.getElementById("rstartMins").value;
        getStartMeridian = document.getElementById("rstartMeridian").value;
        intstartHours = parseInt(getStartHours);

        if(getStartMeridian == 'PM'){
            intstartHours = intstartHours + 12;
            getStartHours = intstartHours;
        }
        var splitDate = "{{resource_date}}"	;
        var splitDateArray = splitDate.split("/");

        var newResourceDate = splitDateArray[0] +"-"+ splitDateArray[1]+"-"+splitDateArray[2];

        var getDate = newResourceDate+' '+getStartHours+':'+getStartMins+':00';

        var resourceStartDate = new Date(getDate);

        if(resourceStartDate < d) {
            var message = "Start Time should be greater than current time";
            document.getElementById("durationError").innerHTML = message;
            return false;
        }

        var endHours = document.getElementById("endHours").value;
        var endMins = document.getElementById("endMins").value;

        if (endHours == "0" && endMins == '0') {
            var message = "Duration should be greater than zero";
            document.getElementById("durationError").innerHTML = message;
            return false;
        } else {
            return true;
        }

    }