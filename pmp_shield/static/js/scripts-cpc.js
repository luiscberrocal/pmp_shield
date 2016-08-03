
$(document).ready(function () {

    // editable input type number MirafloresLockageAcpQty
    $('.transit-time').editable({
        mode: 'inline',
        type: 'text',
        showbuttons: false,
        emptytext: 'Qty',
        emptyclass: "inline-input-empty",
        inputclass: "inline-input-number",
        validate: function (value) {
            if (isNaN(parseInt(value))) {
                return "not a valid number";
            }
        },
        success: function (request, newValue) {

            console.log("funciona");
            // ajax request
            //$.ajax({
            //    type: "PUT",
            //    url: "/Updates/SetLockageQty/",
            //    data: {
            //        sessionId: _currentSessionId,
            //        itinerarySeq: _currentSlotItiSeq,
            //        operatioAreas: lockage,
            //        lockageType: newValue
            //    },
            //    success: function () {
            //        console.log("LockageAcpQty: " + newValue + " ,save for iti: " + _currentSlotItiSeq);
            //    }
            //});
        }
    });

    //create dealy report table into a DataTable
    $('#delaysReport').DataTable( {
        "paging":   false,
        "ordering": true,
        "fixedHeader": true,
       // "autoFill": true,
        "responsive": true,
         "dom": "Bfrtip",
        "buttons": ["copy", "excel", "pdf"]
        //"info":     true
    } );


/*
var table = $('#delaysReport').DataTable( {
    buttons: [
        'copy', 'excel', 'pdf'
    ]
} );

table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );

*/

});
