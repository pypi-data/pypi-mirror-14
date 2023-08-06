
/* CSRFToken management */
$.ajaxSetup({
beforeSend: function(xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
}});

/* default function to prevent undefined */
function get_next_table_id(){}
function get_previous_table_id(){}

$(document).ready(function(){
    $("#main_menu > ul > li > ul").hide();
    $("#main_menu ul ul .selected").parents().show();
    var items = new Array('file', 'operation');
    $("#current_file").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'file', value:$("#current_file").val()}
        );
    });
    $("#current_operation").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'operation', value:$("#current_operation").val()}
        );
    });
    $("#current_contextrecord").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'contextrecord', value:$("#current_contextrecord").val()}
        );
    });
    $("#current_find").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'find', value:$("#current_find").val()}
        );
    });
    if ($(document).height() < 1.5*$(window).height()){
        $('#to_bottom_arrow').hide();
        $('#to_top_arrow').hide();
    }
    $('#language_selector').change(function(){
        $('#language_form').submit();
    });
    if ($.isFunction($(".prettyPhoto a").prettyPhoto)){
        $(".prettyPhoto a").prettyPhoto({'social_tools':''});
    }
    $('#current_items select').change(function(){
        $(this).attr('class', $(this).children("option:selected").attr('class'));
    })
});

$(document).on("click", '#to_bottom_arrow', function(){
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
});

$(document).on("click", '#to_top_arrow', function(){
  $("html, body").animate({ scrollTop: 0}, 1000);
});

$(document).on("click", '.check-all', function(){
  $(this).closest('table'
        ).find('input:checkbox'
        ).attr('checked', $(this).is(':checked'));
});

$(document).on("click", '#main_menu ul li', function(){
    var current_id = $(this).attr('id');
    console.log(current_id);
    $("#main_menu ul ul").not($(this).parents('ul')).not($(this).find('ul')
                        ).hide('slow');
    $(this).find('ul').show('slow');
});

/* manage help texts */
$(document).on("click", '.help_display', function(){
    var help_text_id = $(this).attr("href") + "_help";
    $(help_text_id).toggle();
});

$(document).on("click", '#progress-content', function(){
    $('#progress').hide();
});

var last_window;

function load_window(url, speed, on_success){
    $("#progress").show();
    $.ajax({
        url: url,
        cache: false,
        success:function(html){
            $("#progress").hide();
            $("#window").append(html);
            $("#"+last_window).show();
            $("a[rel^='prettyPhoto']").prettyPhoto({'social_tools':''});
            if (on_success) on_success();
        },
        error:function(XMLHttpRequest, textStatus, errorThrows){
            $("#progress").hide();
        }
    });
}

function load_current_window(url, model_name){
    var id = $("#current_" + model_name).val();
    if (!id) return;
    url = url.split('/');
    url[url.length - 1] = id;
    url.push('');
    return load_window(url.join('/'));
}

function load_url(url){
    $("#progress").show();
    $.ajax({
        url: url,
        cache: false,
        success:function(html){
            $("#progress").hide();
        },
        error:function(XMLHttpRequest, textStatus, errorThrows){
            $("#progress").hide();
        }
    });
}

function open_window(url){
    var newwindow = window.open(url, '_blank',
                                'height=400,width=600,scrollbars=yes');
    if (window.focus) {newwindow.focus()}
    return false;
}

function save_and_close_window(name_label, name_pk, item_name, item_pk){
  var main_page = opener.document;
  jQuery(main_page).find("#"+name_label).val(item_name);
  jQuery(main_page).find("#"+name_pk).val(item_pk);
  opener.focus();
  self.close();
}

function save_and_close_window_many(name_label, name_pk, item_name, item_pk){
  var main_page = opener.document;
  var lbl_ = jQuery(main_page).find("#"+name_label);
  var val_ = jQuery(main_page).find("#"+name_pk);
  if (val_.val()){
    var v = lbl_.val();
    v = v.slice(0, v.lastIndexOf(","));
    lbl_.val(v + ", " + item_name + ", ");
    val_.val(val_.val() + ", " + item_pk);
    lbl_.change();
  } else {
    jQuery(main_page).find("#"+name_label).val(item_name);
    jQuery(main_page).find("#"+name_pk).val(item_pk);
  }
  opener.focus();
  self.close();
}

function multiRemoveItem(selItems, name, idx){
    for(id in selItems){
        if(selItems[id] == idx){
            selItems.splice(id, 1);
        }
    }
    jQuery("#selected_"+name+"_"+idx).remove();
}

function closeAllWindows(){
    jQuery("#window > div").hide("slow");
    jQuery("#window").html("");
}

function show_hide_flex(id){
    if ($(id).is(':hidden')){
        $(id).css('display', 'flex');
    } else {
        $(id).hide();
    }
}
