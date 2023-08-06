var current_status = 'corporation';

$(function() {
    var $radios = $('input:radio[name=person_type]');
    if($radios.is(':checked') === false) {
        $radios.filter('[value='+ current_status +']').prop('checked', true);
    }

    $radios.change(function(){
        var loc = window.location;
        window.location = loc.protocol + '//' + loc.host + loc.pathname + "?status=" + $('input:radio[name=person_type]:checked').val();
    });
    $("#corporation_div").show();
});
