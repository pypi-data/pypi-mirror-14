person_save_callback = function(item_id, lbl){
    var url =  {{edit_source}};
    $('#id_{{field_id}}').val(null);
    $('#id_select_{{field_id}}').val(lbl);
    if (item_id){
        url = {{edit_source}}+item_id;
        $('#id_{{field_id}}').val(item_id);
    }
    $("#id_select_{{field_id}}").trigger('autocompletechange');
    $.get(url , function( data ) {
        $( "#div-{{field_id}}" ).html( data );
    });
};

edit_url =  {{edit_source}};
parent_id = "{{field_id}}";

person_new_callback = function(){
    var url =  {{edit_source}};
    $('#id_{{field_id}}').val(null);
    $('#id_select_{{field_id}}').val(null);
}

$(function() {
    var $radios = $('input:radio[name=person_type]');
    if($radios.is(':checked') === false) {
        $radios.filter('[value='+ current_status +']').prop('checked', true);
    }

    $radios.change(function(){
        var loc = window.location;
        window.location = loc.protocol + '//' + loc.host + loc.pathname + "?status=" + $('input:radio[name=person_type]:checked').val();
    });

    $("#id_select_{{field_id}}").autocomplete({
        source: {{source}},
        select: function( event, ui ) {
                var url =  {{edit_source}};
                if(ui.item){
                    url = {{edit_source}}+ui.item.id;
                    $('#id_{{field_id}}').val(ui.item.id);
                    $('#id_{{field_id}}').change();
                } else {
                    $('#id_{{field_id}}').val(null);
                }
                $.get(url, function( data ) {
                    $( "#div-{{field_id}}" ).html( data );
                });
            },
        minLength: 2{% if options %},
        {{options}}
        {% endif %}
    });

    $.get( {{edit_source}}{% if selected %}+'{{selected}}'{% endif %}, function( data ) {
        $( "#div-{{field_id}}" ).html( data );
    });

    $(document).on("click", '#id_select_{{field_id}}', function(){
        $('#id_{{field_id}}').val(null);
        $('#id_select_{{field_id}}').val(null);
        $.get( {{edit_source}}, function( data ) {
            $( "#div-{{field_id}}" ).html( data );
        });
    });
});
