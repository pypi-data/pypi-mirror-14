{% load replace_underscore %}
var base_source_{{field_id|replace_underscore}} = {{source}};
var source_{{field_id|replace_underscore}} = base_source_{{field_id|replace_underscore}};

$(function() {
    $("#id_select_{{field_id}}").autocomplete({
        source: source_{{field_id|replace_underscore}},
        select: function( event, ui ) {
                if(ui.item){
                    $('#id_{{field_id}}').val(ui.item.id);
                    $('#id_{{field_id}}').change();
                } else {
                    $('#id_{{field_id}}').val(null);
                }
            },
        minLength: 2{% if options %},
        {{options}}
        {% endif %}
    });

    $(document).on("click", '#id_select_{{field_id}}', function(){
        $('#id_{{field_id}}').val(null);
        $('#id_select_{{field_id}}').val(null);
    });


    {% if dynamic_limit %}{% for item_id in dynamic_limit %}
    $('#{{item_id}}').change(function(){
        $("#id_select_{{field_id}}").autocomplete( "option", "source",
            base_source_{{field_id|replace_underscore}} + $('#{{item_id}}').val()
            + '/');
        if ($('#{{item_id}}').val()){
            $("#id_select_{{field_id}}").prop("disabled", false);
        } else {
            $("#id_select_{{field_id}}").prop("disabled", true);
        }
    });
    $('#{{item_id}}').change();
    {% endfor %}{% endif %}
});
