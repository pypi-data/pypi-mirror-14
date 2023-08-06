/**
 * GRAPPELLI AUTOCOMPLETE GENERIC
 * generic lookup with autocomplete
 */

(function($){

    var methods = {
        init: function(options) {
            options = $.extend({}, $.fn.grp_autocomplete_generic.defaults, options);
            return this.each(function() {
                var $this = $(this);
                // assign attributes
                $this.attr({
                    "tabindex": "-1",
                    "readonly": "readonly"
                }).addClass("grp-autocomplete-hidden-field");
                $this.css({
                    'position': "absolute",
                    'z-index': '0',
                    'padding': '0',
                    'width': '1px',
                    'height': '1px',
                    'font-size': '0',
                    'line-height': '0',
                    'color': 'transparent',
                    'border': '0',
                    'background': 'transparent'
                });
                // build autocomplete wrapper/
                var val = $(options.content_type).val() || $(options.content_type).find(':checked').val();
                if (val) {
                    $this.after(loader).after(lookup_link($this.attr("id"),val));
                }
                $this.parent().wrapInner("<div class='grp-autocomplete-wrapper-fk'></div>");
                $this.parent().prepend("<input id='" + $this.attr("id") + "-autocomplete' type='text' class='vTextField' readonly='readonly' value='' />");
                // defaults
                options = $.extend({
                    wrapper_autocomplete: $(this).parent(),
                    input_field: $(this).parent().find("#" + $this.attr("id") + "-autocomplete"),
                    loader: $this.nextAll("div.grp-loader").hide()
                }, $.fn.grp_autocomplete_generic.defaults, options);
                // lookup
                if (val) {
                    lookup_id($this, options);  // lookup when loading page
                }
                lookup_autocomplete($this, options);  // autocomplete-handler
                $this.bind("change focus keyup", function() {  // id-handler
                    lookup_id($this, options);
                });
                $(options.content_type).bind("change", function() {  // content-type-handler
                    update_lookup($(this), options);
                });
                // labels
                $("label[for='"+$this.attr('id')+"']").each(function() {
                    $(this).attr("for", $this.attr("id")+"-autocomplete");
                });
            });
        }
    };

    $.fn.grp_autocomplete_generic = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' +  method + ' does not exist on jQuery.grp_autocomplete_generic');
        }
        return false;
    };

    var loader = function() {
        var loader = $('<div class="grp-loader">loader</div>');
        return loader;
    };

    var lookup_link = function(id, val) {
        var lookuplink = $('<a class="related-lookup"></a>');

        lookuplink.attr('id', 'lookup_' + id);
        lookuplink.attr('href', window.ADMIN_URL + MODEL_URL_ARRAY[val].app + "/" + MODEL_URL_ARRAY[val].model + '/?');
        lookuplink.attr('onClick', 'return showRelatedObjectLookupPopup(this);');

        var obj_val = $('#' + id).val();
        if ( obj_val !== "" ) {
            lookuplink = edit_link(id,val).add(lookuplink);
        }
        return lookuplink;
    };

    var edit_link = function(id, val) {
        var lookuplink = $('<a class="related-edit changelink"></a>');
        var obj_val = $('#' + id).val();

        lookuplink.attr('id', 'edit_' + id);
        lookuplink.attr('href', window.ADMIN_URL + MODEL_URL_ARRAY[val].app + "/" + MODEL_URL_ARRAY[val].model + '/' + obj_val + '?');
        lookuplink.attr('onClick', 'return showRelatedObjectPopup(this);');
        return lookuplink;
    }

    var update_lookup = function(elem, options) {
        var obj = $(options.object_id);

        $.each(obj.parent().find(':input'), function(){
            $(this).val('');
        })

        // remove loader, a-related, related-lookup
        obj.nextAll("a.related-lookup").remove();
        obj.nextAll("a.related-edit").remove();
        obj.nextAll("div.grp-loader").remove();
        var val = $(elem).val() || $(elem).find(':checked').val();
        if (val) {
            obj.after(loader).after(lookup_link(obj.attr('id'),val));
            options.loader = obj.nextAll("div.grp-loader").hide();
        }
    };

    var lookup_autocomplete = function(elem, options) {
        options.wrapper_autocomplete.find("input:first")
            .bind("focus", function() {
                options.wrapper_autocomplete.addClass("grp-state-focus");
            })
            .bind("blur", function() {
                options.wrapper_autocomplete.removeClass("grp-state-focus");
            })
            .autocomplete({
                minLength: 1,
                autoFocus: true,
                delay: 1000,
                source: function(request, response) {
                    $.ajax({
                        url: options.autocomplete_lookup_url,
                        dataType: 'json',
                        data: "term=" + encodeURIComponent(request.term) + "&app_label=" + grappelli.get_app_label(elem) + "&model_name=" + grappelli.get_model_name(elem) + "&query_string=" + grappelli.get_query_string(elem),
                        beforeSend: function (XMLHttpRequest) {
                            var val = $(options.content_type).val() || $(options.content_type).find(':checked').val();
                            if (val) {
                                options.loader.show();
                            } else {
                                return false;
                            }
                        },
                        success: function(data){
                            response($.map(data, function(item) {
                                return {label: item.label, value: item.value};
                            }));
                        },
                        complete: function (XMLHttpRequest, textStatus) {
                            options.loader.hide();
                        }
                    });
                },
                focus: function() { // prevent value inserted on focus
                    return false;
                },
                select: function(event, ui) {
                    options.input_field.val(ui.item.label);
                    elem.val(ui.item.value);
                    elem.trigger('change');
                    return false;
                }
            })
            .data("ui-autocomplete")._renderItem = function(ul,item) {
                if (!item.value) {
                    return $("<li></li>")
                        .data( "item.autocomplete", item )
                        .append( "<span class='error'>" + item.label + "</span>")
                        .appendTo(ul);
                } else {
                    return $("<li></li>")
                        .data( "item.autocomplete", item )
                        .append( "<a>" + item.label + "</a>")
                        .appendTo(ul);
                }
            };
    };

    var set_content_type_readonly = function(options) {
        var content_type = $(options.content_type);
        if ( content_type.attr('type') !== 'hidden' ) {
            var selected = $('option:selected', content_type).text();
            var input = $('<input type="hidden" />');
            input.attr({
                'id': content_type.attr('id'),
                'name': content_type.attr('name')
            }).val(content_type.val());

            content_type.replaceWith(input);

            var content_type_proxy = $('<input type="text" class="vTextField" readonly="readonly" />');
            content_type_proxy.val(selected);
            input.after(content_type_proxy);
        }
    };

    var lookup_id = function(elem, options) {
        $.getJSON(options.lookup_url, {
            object_id: elem.val(),
            app_label: grappelli.get_app_label(elem),
            model_name: grappelli.get_model_name(elem)
        }, function(data) {
            // set_content_type_readonly(options);
            elem.parent().find('.related-lookup').remove();
            elem.parent().find('.related-edit').remove();
            $.each(data, function(index) {
                options.input_field.val(data[index].label);
            });
            var id = elem.attr('id');
            var content_type = $(options.content_type);
            var val = content_type.val() || content_type.find(':checked').val();
            elem.after(lookup_link(elem.attr('id'),val));
        });
    };

    $.fn.grp_autocomplete_generic.defaults = {
        autocomplete_lookup_url: '',
        lookup_url: '',
        content_type: '',
        object_id: ''
    };

})(grp.jQuery);
