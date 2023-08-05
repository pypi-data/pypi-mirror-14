/**
**/
jQuery(document).ready(function() {

  horizon.modals.addModalInitFunction(function (modal) {

    var $textarea = $('#id_text').closest("form").attr("action");

    if (typeof $textarea !== "undefined" && $textarea.indexOf('markuptext') > 0) {

        (function (){

          var initFn = function () {

            $(modal).find(":text, select, textarea").filter(":visible:first").focus().css({'display': 'none'}).wrap("<div id='epiceditor'></div>");

            var markdown_type = $("#id_text_markup_type").val();

            $("#id_text_markup_type").on("change", function (e) {
                markdown_type = $(this).val();
            });

            $(modal).find('textarea').each(function(index) {
                var opts = {
                  textarea: 'id_text',
                  basePath: STATIC_URL + 'lib',
                  clientSideStorage: true,
                  localStorageName: 'epiceditor',
                  useNativeFullscreen: true,
                  parser: function (str) {
                    if (str !== "TEST") {

                        if (markdown_type === "restructuredtext" || markdown_type === "markdown") {

                            var response = $.ajax({
                              url: "/epiceditor/",
                              method: 'POST',
                              data: {
                                text: str,
                                type: markdown_type
                              },
                              async: false,
                              success: function( data ) {
                                if (data.hasOwnProperty('text')) {
                                    return data.text;
                                } else {
                                    return str;
                                }

                              }
                              });
                            if (response.hasOwnProperty('responseJSON') && response.responseJSON.hasOwnProperty('text')) {
                                return response.responseJSON.text
                            } else {
                                return str
                            }

                        } else if (markdown_type === "html") {
                            return str
                        } else if (markdown_type === "plain") {
                            return str
                        }

                  } else {return str}

                  },
                  file: {
                    name: 'epiceditor',
                    defaultContent: '',
                    autoSave: 100
                  },
                  theme: {
                    base: '/themes/base/epiceditor.css',
                    preview: '/themes/preview/preview-dark.css',
                    editor: '/themes/editor/epic-dark.css'
                  },
                  button: {
                    preview: true,
                    fullscreen: true,
                    bar: "auto"
                  },
                  focusOnLoad: false,
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
                  autogrow: false
                }
                
                var editor = new EpicEditor(opts).load();
            });
          }

          loadResource({src: STATIC_URL + "lib/js/epiceditor.min.js", callback: initFn});

        }());

    }
  });
});