(function() {
  'use strict';

  $.fn.multiFormHandler = function(action) {

    if (action === 'add') {
      var formToCloneClass = this.attr('data-clone-class');
      var nestedDepth = parseInt(this.attr('data-nested'), 10) || 0;
      var elemRegex = /-(\d{1,4})(-|$)/gm;
      var formToClone = $('.' + formToCloneClass).last();
      // handle destruction of select2 elements
      if (formToClone.find('.js-select2').length > 0) {
        formToClone.find('.js-select2').select2('destroy').end();
      }
      var formClone = formToClone.clone();
      var elemId = formClone.find('input,select')[0].id;
      var elemExec, elemNum, matched = -1;
      while ((elemExec = elemRegex.exec(elemId)) !== null) {
        matched++;
        if (matched === nestedDepth) elemNum = +elemExec[1] + 1;
      }
      var elemRe = new RegExp('-' + (elemNum - 1) + '(-|$)', 'gm');
      formClone.find('.alert').remove();
      formClone.find(':input').each(function() {
        var inputId = $(this).attr('id');
        var matched = -1;
        var newElemId;
        if (inputId.match(elemRe)[nestedDepth]) {
          newElemId = inputId.replace(elemRe, function(match, i, original) {
            matched++;
            if (matched === nestedDepth && match.endsWith('-')) {
              return '-' + elemNum + '-';
            } else if (matched === nestedDepth) {
              return '-' + elemNum;
            } else {
              return match;
            }
          });
        } else {
          newElemId = inputId.replace(elemRe, '-' + elemNum + '-');
        }
        $(this).attr('name', newElemId).attr('id', newElemId).val('').removeAttr("checked");
      });
      formToClone.after(formClone);
      return;
    }
    else if (action === 'remove') {
      var formToRemoveCls = this.attr('data-parent-elem-class');
      var formToRemove = this.parents('.' + formToRemoveCls);
      formToRemove.remove();
    }
  };

})();
