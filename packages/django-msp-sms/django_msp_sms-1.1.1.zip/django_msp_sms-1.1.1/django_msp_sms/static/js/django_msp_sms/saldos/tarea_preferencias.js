
$("#id_period_start_datetime, #id_period_end_datetime").datetimepicker({'dateFormat':'yy-mm-dd'});

if ($("#id_next_execution").val() === ""){
    $("#id_siguiente_ejecucion_alert").hide();
}

$("#id_btnshow_modal").on("click", function(){
    $("#id_modal_seguro").modal();
});

setInterval(function () {
    var fecha_inicio = new Date($("#id_period_start_datetime").val());
    var fecha_fin = new Date($("#id_period_end_datetime").val());
    var units = $("#id_period_quantity").val();
    var interval = $("#id_period_unit option:selected").val();
	var next_execution =  new Date($("#id_next_execution").val());

    var text = TaskCountDown(fecha_inicio, fecha_fin, units, interval, next_execution);
    $("#id_siguiente_ejecucion_text, .info_guardar_preview").html(text);
    
}, 1000);
