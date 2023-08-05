/**
 * Adapted from bootstrap-growl (https://github.com/ifightcrime/bootstrap-growl)
 */

((function (root, factory) {

    // CommonJS
    if (typeof exports === 'object') {
        module.exports = factory(require('jquery', 'bootstrap'));
    }
    // AMD module
    else if (typeof define === 'function' && define.amd) {
        define(['jquery', 'bootstrap'], factory);
    }

})(this, function ($) {
    $.bootstrapGrowl = function (message, options) {
        var $alert, css, offsetAmount;

        options = $.extend({}, $.bootstrapGrowl.default_options, options);
        $alert = $("<div>");
        $alert.attr("class", "bootstrap-growl alert");
        if (options.type) {
            $alert.addClass("alert-" + options.type);
        }
        if (options.allow_dismiss) {
            $alert.append('<a class="close" data-dismiss="alert" href="#">&times;</a>');
        }
        $alert.append(message);

        var mobile = $(window).width() <= 767;

        if (mobile) {
            offsetAmount = 63;
        } else {
            offsetAmount = -10;
        }
        $(".bootstrap-growl").each(function() {
            return offsetAmount = Math.max(offsetAmount, parseInt($(this).css('top')) + $(this).outerHeight() + options.stackup_spacing);
        });
        css = {
            "position": mobile ? "fixed" : "absolute",
            "margin": "0",
            "z-index": 9999,
            "display": "none",
            "width": options.width,
            "max-width": $(window).width() - 50,
            "top": offsetAmount + "px",
            "right": "25px"
        };
        $alert.css(css);
        $(options.ele).append($alert);
        $alert.fadeIn();
        if (options.delay > 0) {
            return $alert.delay(options.delay).fadeOut(function () {
                return $(this).remove();
            });
        }
    };

    $.bootstrapGrowl.default_options = {
        ele: "body",
        type: null,
        align: "right",
        width: "100%",
        delay: 4000,
        allow_dismiss: true,
        stackup_spacing: 10
    };

}));
