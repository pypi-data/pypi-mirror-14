(function($){
  'use strict';

  $(document).ready(function() {
    $('.file').dblclick(function() {
      var $this = $(this);
      var file = {
        id: $this.data('fileId'),
        url: $this.data('fileUrl'),
        name: $this.data('fileName'),
        file_original_name: $this.data('fileFileOriginalName'),
      };

      window.parent.dismissChooseFilePopup(window, file);
    });
  });
})(jet.jQuery);
