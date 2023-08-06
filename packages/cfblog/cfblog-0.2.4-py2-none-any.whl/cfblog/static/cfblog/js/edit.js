/**
 * Created by vinay on 8/24/15.
 */

if (typeof namespace_delimiter == 'undefined') {
    var namespace_delimiter = '>'
}

var getNamespace = function (elem) {
    var namespace_parents = $(elem).parents("[data-cms-namespace], [data-cms-content]") || [];
    var namespace = '';
    if (namespace_parents.length != 0) {
        namespace_parents.each(function (index, parent) {
            var parent_namespace = $(parent).attr('data-cms-namespace');
            if (!parent_namespace) {
                parent_namespace = $(parent).attr('data-cms-content');
                if (parent_namespace.indexOf('md:') === 0) {
                    parent_namespace = parent_namespace.slice(3);
                }
            }
            if (namespace) {
                namespace =  parent_namespace + namespace_delimiter + namespace;
            } else {
                namespace = parent_namespace;
            }
        });
    }
    return namespace;
};

var showTooltip = function (t) {
    t.stopPropagation();
    var context = t.currentTarget;
    var attrs = context.attributes;
    var span = $(".cms_tooltip span");
    if (attrs.hasOwnProperty('data-cms-content')) {
        var key = attrs['data-cms-content'].value;
        if (key.indexOf('md:') === 0) {
            key = key.slice(3);
        }
    } else if (attrs.hasOwnProperty('data-cms-attr')) {
        var value = attrs['data-cms-attr'].value.split('|');
        key = value[0].slice(value[0].indexOf(':') + 1);
    }
    var namespace = getNamespace(context);
    if (namespace) {
        key = namespace + namespace_delimiter + key;
    }
    span.html(key);
    var n = $(".cms_tooltip");
    n.css("visibility", "visible").show();
    var e = 20;
    i = t.pageX - $(n).offsetParent().offset().left;
    s = t.pageY - $(n).offsetParent().offset().top;
    r = $(n).offsetParent().width();
    a = i + n.outerWidth(!0) + e;
    n.css({left: a >= r ? i - n.outerWidth(!0) - e : i + e, top: s})
};

var hideTooltip = function () {
    var t = $(".cms_tooltip");
    t.css("visibility", "hidden").hide();
};

var editables = $('[data-cms-attr],[data-cms-content]');
editables.on('mousemove', showTooltip);
editables.on('mouseout', hideTooltip);
editables.on('click', function (e) {
    e.preventDefault();
    var key = $(".cms_tooltip span").html();
    $('[class="editable"][id="'+key+'"]').click();
});

$('#cms_toolbar_hide').on('click', function () {
    $('.cms_toolbar').css("visibility", "hidden").hide();
    $('.cms_toolbar_snippet').css("visibility", "visible").show();
});

$('.cms_toolbar_snippet').on('click', function (e) {
    e.preventDefault();
    $(this).css("visibility", "hidden").hide();
    $('.cms_toolbar').css("visibility", "visible").show();
});

var default_opts = {
    basePath: static_url,
    clientSideStorage: true,
    localStorageName: local_storage_name,
    useNativeFullscreen: true,
    parser: marked,
    file: {
        name: 'epiceditor',
        defaultContent: '',
        autoSave: 100
    },
    theme: {
        base: 'themes/base/epiceditor.css',
        preview: 'themes/preview/bartik.css',
        editor: 'themes/editor/epic-dark.css'
    },
    button: {
        preview: true,
        fullscreen: true,
        bar: "auto"
    },
    focusOnLoad: true,
    shortcut: {
        modifier: 18,
        fullscreen: 70,
        preview: 80
    },
    string: {
        togglePreview: 'Toggle Preview Mode',
        toggleEdit: 'Toggle Edit Mode',
        toggleFullscreen: 'Enter Fullscreen'
    },
    autogrow: true
};

$(document).ready(function () {
    var local_storage_name = window.local_storage_name;
    var local_storage = window.localStorage;
    var local_data = {};
    if (local_storage && local_storage_name in local_storage) {
        var draft_data = JSON.parse(local_storage[local_storage_name]);
        for (var key in draft_data) {
            if (draft_data.hasOwnProperty(key)) {
                local_data[key] = draft_data[key]['content'];
                date_in_draft = draft_data[key]['modified'];
                if(modified_on > date_in_draft){
                  local_storage.removeItem(local_storage_name);
                  local_data = {};
                  alert("Draft data was out of date and has been cleared.");
                  break;  
                }
            }
        }
    }

    editables.each(function (index, elem) {
        var namespace = getNamespace(elem);
        if (elem.hasAttribute('data-cms-content')) {
            var md = false;
            var content_key = $(elem).attr('data-cms-content');
            if (content_key.indexOf('md:') === 0) {
                md = true;
                content_key = content_key.slice(3)
            }

            if (namespace) {
                content_key = namespace + namespace_delimiter + content_key;
            }

            var a = $('<li/>');
            var text = content_key;
            if (md) {
                text = '*' + content_key;
            }
            $('<div/>', {
                id: content_key,
                markdown: md,
                text: text
            }).addClass('editable').appendTo(a);
            $('<textarea/>', {
                id: content_key+'_content',
                text: local_data[content_key+'_editor'] || cms_data[content_key] || elem.innerHTML,
                hidden: 'hidden'
            }).appendTo(a);
            a.appendTo($('.cms_toolbar_list'));
            $('<div/>', {
                id: content_key+'_editor',
                hidden: 'hidden'
            }).appendTo($('.cms_editor #editors'));
        }

        if (elem.hasAttribute('data-cms-attr')) {
            $(elem).attr('data-cms-attr').split('|').forEach(function (attribute) {
                var key = attribute.slice(attribute.indexOf(':') + 1);
                var attr_name = attribute.slice(0, attribute.indexOf(':'));
                var a = $('<li/>');

                if (namespace) {
                    key = namespace + namespace_delimiter + key;
                }

                $('<div/>', {
                    id: key,
                    text: key,
                    markdown: false
                }).addClass('editable').appendTo(a);
                $('<textarea/>', {
                    id: key+'_content',
                    text: cms_data[key] || $(elem).attr(attr_name),
                    hidden: 'hidden'
                }).appendTo(a);
                a.appendTo($('.cms_toolbar_list'));
                $('<div/>', {
                    id: key+'_editor',
                    hidden: 'hidden'
                }).appendTo($('.cms_editor #editors'));
            });
        }
    });

    var editor = null;
    var id = null;

    var closeEditors = function () {
        $('.cms_editor').css('visibility', 'hidden').hide();
            $('.cms_toolbar_list li').removeClass('cms_highlight');
            $('[id$="_editor"]').css('visibility', 'hidden').hide();
            if (editor && editor.is('loaded')) {
                editor.unload();
            }
    };
    $('.cms_close').on('click', closeEditors);

    $('.editable').on('click', function (e) {
        id = e.target.id;
        var editor_id = id + '_editor';
        console.log(id);
        if ($('#'+editor_id).css('visibility') != 'visible') {
            closeEditors();
            $(this).parent().addClass('cms_highlight');
            var opts = default_opts;
            opts.container = editor_id;
            opts.textarea = id + '_content';
            opts.file.name = editor_id;
            $('.cms_editor').css('visibility', 'visible').show();
            $('#'+editor_id).css('visibility', 'visible').show();
            editor = new EpicEditor(opts);
            editor.load(function () {
                $('div#' + editor_id).show();
            });
        }
    });

    /* Saving content by retrieving from localstorage rather than using DOM html content */
    var get_content = function () {
        var content = {};
        var data = editor._getFileStore();
        for (var key in data) {
            if (key && key.endsWith('_editor')) {
                content[key.replace('_editor', '')] = _sanitizeRawContent(data[key]['content']);
            }
        }
        return content
    };

    /* Copied from epiceditor as this function is not exposed via api */
    /**
     * Converts the 'raw' format of a file's contents into plaintext
     * @param   {string} content Contents of the file
     * @returns {string} the sanitized content
     */
    function _sanitizeRawContent(content) {
        // Get this, 2 spaces in a content editable actually converts to:
        // 0020 00a0, meaning, "space no-break space". So, manually convert
        // no-break spaces to spaces again before handing to marked.
        // Also, WebKit converts no-break to unicode equivalent and FF HTML.
        return content.replace(/\u00a0/g, ' ').replace(/&nbsp;/g, ' ');
    }

    $('#save_content').on('click', function (e) {
        e.preventDefault();
        $(this).prop('disabled', true);
        if ($.isEmptyObject(editor)) {
            alert('You changed nothing\n\n' +
                    'Jon Snow');
        } else {
            post_content(draft_url, get_content());
        }
        $(this).prop('disabled', false);
    });

    $('#publish').on('click', function (e) {
        e.preventDefault();
        $(this).prop('disabled', true);
        var content = {};
        if (!($.isEmptyObject(editor))) {
            content = get_content();
        }
        post_content(publish_url, content);
        $(this).prop('disabled', false);
    });

    function post_content(url, content) {
        if (local_storage && local_storage_name in local_storage) {
            var draft_data = JSON.parse(local_storage[local_storage_name]);
            for (var key in draft_data) {
                if (draft_data.hasOwnProperty(key)) {
                    tmp = draft_data[key]['modified'];
                    if(typeof min_dt === 'undefined'){
                        var min_dt = tmp;
                    }
                    if(tmp < min_dt){
                        min_dt = tmp;
                    }
                    console.log(min_dt);
                }
            }
        }
        var post_data = {
            'auth_data': JSON.stringify(content),
            'csrfmiddlewaretoken': CSRF_TOKEN,
            'draft_modified': typeof min_dt === 'undefined'?"":min_dt.toString(),
            'cms_page_id': cms_page_id
        };
        $.post(url, post_data, function (data) {
            if (data.success) {
                local_storage.removeItem(local_storage_name);
                location.reload(true);
            } else {
                console.log(data.message_in_detail);
                alert(data.message);
                if(data.draft_error || data.success == null){
                    location.reload(true);
                    local_storage.removeItem(local_storage_name);
                }
            }
        }, 'json');
    }
});
