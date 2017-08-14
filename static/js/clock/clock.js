 $('.form_datetime').datetimepicker({
        //language:  'fr',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
    });
	$('.form_date').datetimepicker({
        language:  'fr',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
    });
	$('.form_time').datetimepicker({
        language:  'fr',
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 1,
		minView: 0,
		maxView: 1,
		forceParse: 0
    });



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