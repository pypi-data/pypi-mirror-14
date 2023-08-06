{% load replace_underscore %}
function split( val ) {
    return val.split( /,\s*/ );
}

function extractLast( term ) {
    return split( term ).pop();
}

var {{field_id|replace_underscore}}_values = $('#id_{{field_id}}').val().split(',');
if(!{{field_id|replace_underscore}}_values){
    {{field_id|replace_underscore}}_values = new Array();
}
var {{field_id|replace_underscore}}_ctext = "";

$("#id_select_{{field_id}}")
    // don't navigate away from the field on tab when selecting an item
      .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
           $( this ).data( "ui-autocomplete" ).menu.active ) {
            event.preventDefault();
        } else if (event.keyCode === $.ui.keyCode.DELETE ||
                   event.keyCode === $.ui.keyCode.BACKSPACE){
            {{field_id|replace_underscore}}_ctext =
                                $("#id_select_{{field_id}}").val().split(',');
        }
      })
      .bind( "keyup", function( event ) {
        if (event.keyCode === $.ui.keyCode.DELETE ||
            event.keyCode === $.ui.keyCode.BACKSPACE){
            var new_val = $("#id_select_{{field_id}}").val().split(',');
            var length = {{field_id|replace_underscore}}_ctext.length;
            for (idx=0;idx<length;idx++){
                if(idx >= new_val.length ||
                   {{field_id|replace_underscore}}_ctext[idx] != new_val[idx]){
                    if (idx == (length - 1) && length > 1){
                        if ({{field_id|replace_underscore}}_ctext[idx].trim() == ""){
                            idx = idx - 1;
                        } else {
                            return;
                        }
                    }
                    {{field_id|replace_underscore}}_ctext.splice(idx, 1);
                    // remove value
                    if (idx < {{field_id|replace_underscore}}_values.length){
                        {{field_id|replace_underscore}}_values.splice(idx, 1);
                        $('#id_{{field_id}}').val({{field_id|replace_underscore}}_values);
                    }
                    if ({{field_id|replace_underscore}}_ctext.length > 0 &&
                        {{field_id|replace_underscore}}_ctext[0].length){
                        // remove leading space
                        if ({{field_id|replace_underscore}}_ctext[0][0] == ' '){
                            {{field_id|replace_underscore}}_ctext[0] =
                                    {{field_id|replace_underscore}}_ctext[0].trim();
                        }
                        // remove trailing space
                        var last = {{field_id|replace_underscore}}_ctext.length -1;
                        {{field_id|replace_underscore}}_ctext[last] =
                            {{field_id|replace_underscore}}_ctext[last].trim();
                    }
                    this.value = {{field_id|replace_underscore}}_ctext.join(", ");
                    return
                }
            }
        }
    }).autocomplete({
     source:  function( request, response ) {
        $.getJSON({{source}}, {
            term: extractLast( request.term )
        }, response );
     },
     focus: function() {
        // prevent value inserted on focus
        return false;
     },
     select: function( event, ui ) {
        var terms = split( this.value );
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push( ui.item.value );
        {{field_id|replace_underscore}}_values.push(ui.item.id);
        // add placeholder to get the comma-and-space at the end
        $('#id_{{field_id}}').val({{field_id|replace_underscore}}_values);
        terms.push( "" );
        this.value = terms.join( ", " );
        return false;
     },
     minLength: 2{% if options %},
     {{options}}
     {% endif %}
});
