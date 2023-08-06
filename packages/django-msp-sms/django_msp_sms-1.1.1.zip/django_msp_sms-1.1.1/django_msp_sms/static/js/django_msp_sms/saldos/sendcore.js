
function AjaxAsyncTask(args) {
    this.lista = args.list
    this.porcentaje = 0
    this.deferred = $.Deferred()
    this.promise = deferred.promise()
    this.index = 0
    this.indexlist = 0
    this.$progress = args.$progress
    this.url = args.url
    this.interval = args.interval
    
    if (args.onDone == undefined) 
        this.result = function(){}    
    else
        this.result = args.onDone    

    if (args.onSuccesRequest == undefined) 
        this.onSuccesRequest = function(){}    
    else
        this.onSuccesRequest = args.onSuccesRequest

    this.failed = function() {
        $progress.css({
            'background': 'red'
        });
    }

    this.inProgress = function() {
        $progress.attr('style',' width:'+porcentaje+'%')
        $progress.text(porcentaje+'%')

    }

    this.sendData = function(){
         if (porcentaje < 100) {
            var data = JSON.stringify(lista[indexlist])
            $.ajax({
                url:url, 
                type : 'get', 
                data: { 'data': data },
            }).done(function(data){
                onSuccesRequest(data)
                porcentaje = ((indexlist+1)*100)/lista.length
                deferred.notify()

                indexlist += 1
                sendData()
            })



        } else {
            this.deferred.resolve()
        }
    }

    this.uniqueRequest = function(){
        var data = JSON.stringify(lista)
        $.ajax({
            url:url, 
            type : 'get', 
            data: { 'data': data },
            success: onSuccesRequest ,
        })
        countUp()
    }

    this.countUp = function() {
        if (porcentaje < 100) {
            deferred.notify();
            porcentaje = ((index+1)*100)/lista.length
            index += 1
            setTimeout( function(){ 
                countUp();
            }, interval)
            
        } else {
            deferred.notify();
            this.deferred.resolve()
        }
    }

    this.promise.done(result)
    this.promise.fail(failed)
    this.promise.progress(inProgress)


    if (interval != undefined) {
        uniqueRequest()
    }
    else{
        sendData()
    }
}

function sendMessages(clientes_ids){
    var data = JSON.stringify(clientes_ids)
    mensajes_enviados = 0;
    $.ajax({
        url:'/sms/saldos/get_mensajes_saldos/',
        type : 'get', 
        data: { 'data': data },
    }).done(function(data){
        if (data.cargos != null) {
            if (data.cargos.length > 0){
                AjaxAsyncTask({
                    list: data.cargos,
                    $progress: $("#progreso"),
                    url:'/sms/saldos/enviar_cargo/',
                    onSuccesRequest: function(data){
                        mensajes_enviados = mensajes_enviados + 1
                        showChanges(data, mensajes_enviados)
                    },
                    onDone: function(){
                        alert("Mensajes Enviados");
                        $('#progreso').text('');
                        $('#progreso').attr('style',' width:0%');
                        $("#id_clientes-deck").text("");
                        $("#id_clientes").text("");
                        $(".yourlabs-autocomplete autocomplete-light-widget").text("");
                        $("#btnEnviar-estadosCuenta").show();
                        location.reload();
                    }
                })
            }
            else{
                alert('No hay mensajes para ninguno de los clientes seleccionados');
                $(".yourlabs-autocomplete autocomplete-light-widget").text("");
                location.reload();
            }
        }
    })
}

function showChanges(data, mensajes_enviados){
    if (data.resultado == 'Mensaje enviado') {
        $("#alert").show();
        $('#alert').attr('class','alert alert-info fade in');
        var mensaje_alerta = mensajes_enviados+" Mensajes Enviados correctamente.<br>"
        $("#alertContainer").html(mensaje_alerta);
        // if (data.clientes_sin_mensaje.length>0) {
        //     mensaje_alerta =mensaje_alerta +"<br><strong>Clientes sin cargos:</strong><br>"+data.clientes_sin_mensaje.join('<br/>');
        // }
        // if (data.clientes_con_telefono_invalido.length>0) {
        //     mensaje_alerta =mensaje_alerta +"<br><strong>Clientes con telefono invalido:</strong><br>"+data.clientes_con_telefono_invalido.join('<br/>');
        // }
        
    }
}