define('django_backend.ajaxdialog', ['jquery', 'django_backend.formdata', 'django_backend.dialog'], function ($, formdata, Dialog, undefined) {
  "use strict";
  
  var AjaxDialog = Dialog.subclass({
    defaults: $.extend({}, Dialog.prototype.defaults, {
      url: null
    }),

    constructor: function (element, options) {
      AjaxDialog.parent.constructor.apply(this, arguments);
      // We will keep track of the currently active URL if the user followed a
      // link.
      this.url = this.options.url;
    },

    gotNewContent: function ($content, data) {
      this.prepareDialog(data.title, $content);
    },

    prepareContent: function ($content) {
      var self = this;
      $content = AjaxDialog.parent.prepareContent.call(this, $content);

      $content.on('click', 'a', function (e) {
        var $a = $(this);
        var href = $a.attr('href');
        // Do not handle the click if it's a hash.
        if (href.match(/^#/)) {
            return true;
        }
        // Do not handle new window links
        if ($a.attr('target') == '_blank') {
            return true;
        }
        e.preventDefault();
        self.onClickLink($a);
        return false;
      });

      $content.on('submit', 'form', function (e) {
        self.onSubmit($(this));
        return false;
      });

      $content.on('click', 'button', function (e) {
        var $button = $(this);
        var $form = $button.closest('form');
        if ($form.length && $button.attr('type') == 'submit') {
          $form.append($('<input>').attr('type', 'hidden')
            .attr('name', $button.attr('name'))
            .attr('value', $button.attr('value')));
        }
      });

      return $content;
    },

    load: function (url, success) {
      var self = this;
      this.url = url;
      $.ajax(this.url, {
        cache: false,
        dataType: 'json',
        success: function () {
          success.apply(self, arguments);
        }
      });
    },

    onClickLink: function ($a) {
      var url = $a.attr('href');
      this.load(url, this.onClickLinkSuccess.bind(this));
    },

    onClickLinkSuccess: function (data) {
        this.handleDataResponse(data);
    },

    onSubmit: function ($form) {
      var self = this;
      formdata.submit($form, {
        url: $form.attr('action') || this.url,
        success: function (data) {
          self.handleDataResponse(data);
        }
      });
      this.emit('dialog-submit');
    },

    open: function () {
      this.load(this.url, this.onOpenSuccess);
    },

    onOpenSuccess: function (data) {
      this.create(
        data.title,
        this.initContent(data.html));
      this.emit('open');
    }
  });

  return AjaxDialog;
});
