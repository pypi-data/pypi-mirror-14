jQuery(function($) {

    /// add predelete class (only necessary in case of errors)
    $('div.inline-group').find('input[name*="DELETE"]:checked').each(function(i) {
        $(this).parents('div.inline-related').addClass('predelete');
    });

    // BUTTONS (STACKED INLINE)
    $('div.inline-stacked a.closehandler').bind("click", function(){
        $(this).parents('div.inline-stacked').addClass('collapsed');
        $(this).parents('div.inline-stacked').addClass('collapse-closed');
        $(this).parents('div.inline-stacked').removeClass('collapse-open');
        $(this).parents('div.inline-stacked').find('div.inline-related').addClass('collapsed');
        $(this).parents('div.inline-stacked').find('div.inline-related').addClass('collapse-closed');
        $(this).parents('div.inline-stacked').find('div.inline-related').removeClass('collapse-open');
    });
    $('div.inline-stacked a.openhandler').bind("click", function(){
        $(this).parents('div.inline-stacked').removeClass('collapsed');
        $(this).parents('div.inline-stacked').removeClass('collapse-closed');
        $(this).parents('div.inline-stacked').addClass('collapse-open');
        $(this).parents('div.inline-stacked').find('div.inline-related').removeClass('collapsed');
        $(this).parents('div.inline-stacked').find('div.inline-related').removeClass('collapse-closed');
        $(this).parents('div.inline-stacked').find('div.inline-related').addClass('collapse-open');
    });

    /// function for cleaning up added items
    function new_item_cleanup(new_item) {
        /// remove error-lists and error-classes
        new_item.find('ul.errorlist').remove();
        new_item.find('div[class*="errors"]').removeClass("errors");
        /// remove delete-button
        /// temporary deactivated, because reordering does not work
        /// new_item.find('a.deletelink').remove();
        /// new_item.find('a.viewsitelink').remove();
        /// tinymce
        new_item.find('span.mceEditor').each(function(e) {
            var id = this.id.split('_parent')[0];
            $(this).remove();
            new_item.find('#' + id).css('display', '');
            tinyMCE.execCommand("mceAddControl", true, id);
        });
        /// clear all form-fields (within form-cells)
        new_item.find(':input').val('');
        /// clear related/generic lookups
        new_item.find("strong").text("");
        return new_item;
    }

    /// ADDHANDLER
    $('div.inline-group a.addhandler').bind("click", function(){
        var inlinegroup = $(this).parents('div.inline-group');
        var items = inlinegroup.find('input[id*="TOTAL_FORMS"]').val();
        var max_items = inlinegroup.find('input[id*="MAX_NUM_FORMS"]').val();

        // Fix to respect the inline max_num property
        if ( parseInt(items) >= parseInt(max_items) ) return;

        //var new_item = inlinegroup.find('div.inline-related:last').clone(true).insertAfter('div.inline-related:last', inlinegroup);
        var proto = inlinegroup.find('div.inline-related:last');
        var new_item = proto.clone(true).css('display','');
        if ( new_item.hasClass('empty-form') ) {
            new_item.removeClass('empty-form');
        }
        var remove_link = $('<a href="javascript://" class="deletelink" title="Remove" />');
        remove_link.bind('click', function() {
            new_item.remove();
            var items = inlinegroup.find('input[id*="TOTAL_FORMS"]').val();
            inlinegroup.find('input[id*="TOTAL_FORMS"]').val(parseInt(items) - 1);
        });
        new_item.find('.inline-item-tools > li:last').html('').append(remove_link)

        proto.before(new_item);
        /// change header
        new_item.find('h3:first').html("<b>" + new_item.find('h3:first').text().split("#")[0] + "#" + (parseInt(items) + 1) + "</b>");
        /// set TOTAL_FORMS to number of items
        inlinegroup.find('input[id*="TOTAL_FORMS"]').val(parseInt(items) + 1);
        /// replace IDs, NAMEs, HREFs & FORs ...
        new_item.find(':input,span,table,iframe,label,a,ul,p,img').each(function() {
            if ($(this).attr('id')) {
                $(this).attr('id', $(this).attr('id').replace(/-__prefix__-/g, "-" + parseInt(items) + "-"));
            }
            if ($(this).attr('name')) {
                $(this).attr('name', $(this).attr('name').replace(/-__prefix__-/g, "-" + parseInt(items) + "-"));
            }
            if ($(this).attr('for')) {
                $(this).attr('for', $(this).attr('for').replace(/-__prefix__-/g, "-" + parseInt(items) + "-"));
            }
            if ($(this).attr('href')) {
                $(this).attr('href', $(this).attr('href').replace(/-__prefix__-/g, "-" + parseInt(items) + "-"));
            }
        });
        /// remove calendars and clocks, re-init
        if (typeof(DateTimeShortcuts)!="undefined") {
            $('a[id^="calendarlink"]').parent().remove();
            $('a[id^="clocklink"]').parent().remove();
            DateTimeShortcuts.init();
        }

        var grp_inlinegroup = grp.jQuery(inlinegroup);
        var autocomplete_fields_generic = grp_inlinegroup.data('autocomplete_fields_generic');
        if ( autocomplete_fields_generic !== undefined ) {
            var item = grp.jQuery(new_item);
            var prefix = grp_inlinegroup.data('prefix');
            var lookup_url = grp_inlinegroup.data('lookup_url');
            var autocomplete_lookup_url = grp_inlinegroup.data('autocomplete_lookup_url');
            $.each(autocomplete_fields_generic, function() {
                var content_type = this[0];
                var object_id = this[1];

                item.find("input[name^='" + prefix + "'][name$='-" + this[1] + "']")
                .each(function() {
                    var i = $(this).attr("id").match(/(?:-\d+)?(-\d+-)/);
                    if (i) {
                        var ct_id = "#id_" + prefix + i[1] + content_type,
                            obj_id = "#id_" + prefix + i[1] + object_id;
                        grp.jQuery(this).grp_autocomplete_generic({
                            content_type:ct_id,
                            object_id:obj_id,
                            lookup_url: lookup_url,
                            autocomplete_lookup_url: autocomplete_lookup_url
                        });
                    }
                });
            });
        }

        /// do cleanup
        new_item = new_item_cleanup(new_item);
    });

    /// DELETEHANDLER
    $('div.inline-group input[name*="DELETE"]').hide();
    $('div.inline-group a.deletelink').bind("click", function() {
        $(this).prev(':checkbox').attr('checked', !$(this).prev(':checkbox').attr('checked'));
        $(this).parents('div.inline-related').toggleClass('predelete');
    });

});
