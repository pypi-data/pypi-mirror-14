(function() {
  loadResource(STATIC_URL + "ckeditor/ckeditor/ckeditor.js");
  var djangoJQuery;
  if (typeof jQuery == 'undefined' && typeof django == 'undefined') {
    console.error('ERROR django-ckeditor missing jQuery. Set CKEDITOR_JQUERY_URL or provide jQuery in the template.');
  } else if (typeof django != 'undefined') {
    djangoJQuery = django.jQuery;
  }


  var $ = jQuery || djangoJQuery;
  $(function() {

    /* inicialize in modal */
    horizon.modals.addModalInitFunction(function (modal) {
      initialiseCKEditor();
    });

    initialiseCKEditor();
    initialiseCKEditorInInlinedForms();

    function initialiseCKEditorInInlinedForms() {
      try {
        $(document).on("click", ".add-row a, .grp-add-handler", function () {
          initialiseCKEditor();
          return true;
        });
      } catch (e) {
        $(document).delegate(".add-row a, .grp-add-handler", "click",  function () {
          initialiseCKEditor();
          return true;
        });
      }
    }

    function initialiseCKEditor() {
      $('textarea[data-type=ckeditortype]').each(function(){
        if ($(this).closest("div[id*='markup']").length == 0) {
          if($(this).data('processed') == "0" && $(this).attr('id').indexOf('__prefix__') == -1){
            $(this).data('processed',"1");
            $($(this).data('external-plugin-resources')).each(function(){
                CKEDITOR.plugins.addExternal(this[0], this[1], this[2]);
            });
            CKEDITOR.replace($(this).attr('id'), $(this).data('config'));
          }
        } else {
          $(this).width($(this).data('config').width);
          $(this).height($(this).data('config').height);
        }
      });
    }
  });
}());