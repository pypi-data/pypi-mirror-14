/// <reference path="generic.ts" />
/// <reference path="DefinitelyTyped/jquery.d.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var widget_uuid = 0;
var Widget = (function () {
    // static class_name : string
    function Widget(options) {
        this.options = options;
        this.uuid = widget_uuid;
        widget_uuid = widget_uuid + 1;
    }
    Widget.prototype.get_uuid = function () {
        return this.uuid.toString();
    };
    Widget.prototype.show = function (element) {
        this.element = element;
        this.element.data('widget', this);
    };
    Widget.prototype.enable = function () {
        this.options.disabled = false;
    };
    Widget.prototype.disable = function () {
        this.options.disabled = true;
    };
    Widget.prototype.toggle = function () {
        if (this.options.disabled) {
            this.enable();
        }
        else {
            this.disable();
        }
    };
    Widget.prototype.hide = function () {
        this.element.filter(":data(widget)").each(function (key, el) {
            var widget = $(el).data("widget");
            widget.destroy();
        });
    };
    Widget.prototype.remove = function () {
        this.hide();
        this.element.remove();
    };
    Widget.prototype.destroy = function () {
        remove_all_listeners(this);
        this.disable();
        this.element.empty();
        this.element.removeData('widget');
    };
    return Widget;
}());
var Viewport = (function (_super) {
    __extends(Viewport, _super);
    function Viewport(options) {
        _super.call(this, options);
    }
    Viewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        if (this.options.id == null) {
            this.options.id = this.get_uuid();
        }
        this.element.attr("id", this.options.id);
        var header = $("<div/>")
            .addClass("viewport_header")
            .appendTo(this.element);
        this.maximize_button = $("<div/>")
            .addClass("button")
            .addClass("maximize_button")
            .text("[M]")
            .click(function (ev) {
            _this.maximize();
        })
            .appendTo(header);
        this.unmaximize_button = $("<div/>")
            .addClass("button")
            .addClass("unmaximize_button")
            .text("[R]")
            .on("click", function (ev) {
            _this.unmaximize();
        })
            .appendTo(header);
        this.set_maximize_button();
        $("<div/>")
            .addClass("button")
            .addClass("close_button")
            .text("[X]")
            .on("click", function (ev) {
            _this.remove();
            return false;
        })
            .appendTo(header);
        this.h1 = $("<h1/>")
            .on("click", function (ev) {
            _this.toggle();
        })
            .appendTo(header);
        this.element.addClass("viewport");
        if (this.options.disabled) {
            this.disable();
        }
        else {
            this.enable();
        }
        // We must set title after enabling widget, so we push new state to
        // history first.
        this.set_title(this.options.title);
        this.div = $("<div/>")
            .addClass("viewport_content")
            .appendTo(this.element);
    };
    Viewport.prototype.set_maximize_button = function () {
        var maximize = $("#content").hasClass("maximize");
        this.maximize_button.toggle(!maximize);
        this.unmaximize_button.toggle(maximize);
    };
    Viewport.prototype.maximize = function () {
        this.enable();
        $("#content").addClass("maximize");
        this.set_maximize_button();
    };
    Viewport.prototype.unmaximize = function () {
        this.enable();
        $("#content").removeClass("maximize");
        this.set_maximize_button();
    };
    Viewport.prototype._enable = function () {
        _super.prototype.enable.call(this);
        this.element.removeClass("disabled");
    };
    Viewport.prototype._disable = function () {
        _super.prototype.disable.call(this);
        this.element.addClass("disabled");
    };
    Viewport.prototype._disable_all = function () {
        $(".viewport:not(.disabled)").each(function (key, el) {
            var viewport = $(el).data('widget');
            viewport._disable();
        });
    };
    Viewport.prototype.disable_all = function () {
        this._disable_all();
        push_state();
    };
    Viewport.prototype.enable = function () {
        this._disable_all();
        this._enable();
        push_state();
    };
    Viewport.prototype.disable = function () {
        this.unmaximize();
        this._disable();
        push_state();
    };
    Viewport.prototype.remove = function () {
        _super.prototype.remove.call(this);
        var last_viewport = $(".viewport:last");
        if (last_viewport.length > 0) {
            var viewport = last_viewport.data('widget');
            viewport.enable();
        }
        else {
            push_state();
        }
    };
    Viewport.prototype.set_title = function (title) {
        this.h1.text(title);
        this.options.title = title;
        if (!this.options.disabled) {
            push_state(true);
        }
    };
    Viewport.prototype.get_title = function () {
        return this.options.title;
    };
    Viewport.prototype.get_streamable_options = function () {
        var streamable = {};
        streamable['disabled'] = this.options.disabled;
        streamable['title'] = this.options.title;
        streamable['id'] = this.options.id;
        return streamable;
    };
    return Viewport;
}(Widget));
var BaseDialog = (function (_super) {
    __extends(BaseDialog, _super);
    function BaseDialog(options) {
        _super.call(this, options);
        this.loading = false;
    }
    BaseDialog.prototype.show = function (element) {
        var _this = this;
        $.each($(".autoclose"), function (i, dialog) {
            var widget = $(dialog).data("widget");
            widget.remove();
        });
        _super.prototype.show.call(this, element);
        this.element.addClass("autoclose");
        var options = this.options;
        this.description = $("<p/>")
            .appendTo(this.element);
        this.element.data('dialog', this);
        if (options.description != null) {
            this.description
                .text(options.description);
        }
        var submit = "Continue";
        if (options.button != null) {
            submit = options.button;
        }
        var doptions = {};
        doptions.buttons = {};
        doptions.buttons[submit] = function () {
            _this.check_submit();
        };
        doptions.buttons['Cancel'] = function () {
            _this.remove();
        };
        doptions.title = options.title;
        doptions.width = 400;
        this.element.on("keypress", function (ev) {
            if (ev.which === 13 && !ev.shiftKey) {
                _this.check_submit();
                return false;
            }
        });
        doptions.close = function (ev, ui) {
            _this.remove();
        };
        this.element.dialog(doptions);
    };
    BaseDialog.prototype.check_submit = function () {
        this.disable();
        this.submit();
    };
    BaseDialog.prototype.submit = function () {
    };
    BaseDialog.prototype.set = function (values) {
    };
    BaseDialog.prototype.disable = function () {
        this.element.dialog("disable");
        _super.prototype.disable.call(this);
    };
    BaseDialog.prototype.enable = function () {
        this.element.dialog("enable");
        _super.prototype.enable.call(this);
    };
    BaseDialog.prototype.destroy = function () {
        this.element.removeClass('autoclose');
        _super.prototype.destroy.call(this);
    };
    BaseDialog.prototype.set_title = function (title) {
        this.element.parent().find(".ui-dialog-title").html(title);
    };
    BaseDialog.prototype.set_description = function (description) {
        this.description.text(description);
    };
    BaseDialog.prototype._save = function (http_type, oject_id, values) {
        var _this = this;
        var type = this.type;
        this.loading = true;
        var url;
        if (oject_id != null) {
            url = window.__api_prefix + "api/" + type + "/" + oject_id + "/";
        }
        else {
            url = window.__api_prefix + "api/" + type + "/";
        }
        this.xhr = ajax({
            url: url,
            data: values,
            type: http_type
        }, function (data) {
            _this.loading = false;
            _this.save_success(data);
        }, function (message, data) {
            _this.loading = false;
            _this.save_error(message, data);
        });
    };
    BaseDialog.prototype.save = function (http_type, object_id, values) {
        this._save(http_type, object_id.toString(), values);
    };
    BaseDialog.prototype.save_action = function (http_type, what, values) {
        this._save(http_type, what, values);
    };
    BaseDialog.prototype.save_success = function (data) {
        this.remove();
    };
    BaseDialog.prototype.save_error = function (message, data) {
        alert("Error: " + message);
        this.enable();
    };
    return BaseDialog;
}(Widget));
var ImageWidget = (function (_super) {
    __extends(ImageWidget, _super);
    function ImageWidget(options) {
        _super.call(this, options);
    }
    ImageWidget.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.element.addClass("image");
        if (this.options.photo != null) {
            this.set(this.options.photo);
        }
        else {
            this.set_none();
        }
    };
    ImageWidget.prototype.clear = function () {
        this.element.empty();
    };
    ImageWidget.prototype.set = function (photo) {
        this.clear();
        if (this.options.do_video && !$.isEmptyObject(photo.videos)) {
            var img = $("<video controls='controls'/>");
            var size = "320";
            for (var i = 0; i < photo.videos[size].length; i++) {
                var pv = photo.videos[size][i];
                var priority = pv[0];
                var video = pv[1];
                img
                    .attr("width", video.width)
                    .attr("height", video.height);
                $("<source/>")
                    .attr("src", video.url)
                    .attr("type", video.format)
                    .appendTo(img);
            }
            img.appendTo(this.element);
            this.img = img;
        }
        else {
            var image = null;
            if (photo != null) {
                image = photo.thumbs[this.options.size];
            }
            if (image != null) {
                this.img = $("<img></img>")
                    .attr('src', image.url)
                    .attr('width', image.width)
                    .attr('height', image.height)
                    .attr('alt', photo.title);
                if (this.options.include_link) {
                    this.a = photo_a(photo)
                        .empty()
                        .append(this.img)
                        .appendTo(this.element);
                }
                else {
                    this.img.appendTo(this.element);
                }
                this.width = image.width;
                this.height = image.height;
            }
            else {
                this.set_none();
            }
        }
    };
    ImageWidget.prototype.set_error = function () {
        this.clear();
        $("<img></img>")
            .attr("src", static_url("img/error.png"))
            .appendTo(this.element);
    };
    ImageWidget.prototype.set_none = function () {
        this.clear();
        this.img = $("<img></img>")
            .attr('width', 120)
            .attr("src", static_url("img/none.jpg"))
            .appendTo(this.element);
        this.width = 227;
        this.height = 222;
    };
    ImageWidget.prototype.set_loading = function () {
        this.clear();
        $("<img></img>")
            .attr("src", static_url("img/ajax-loader.gif"))
            .appendTo(this.element);
    };
    ImageWidget.prototype.resize = function (enlarge) {
        var width = this.width;
        var height = this.height;
        var img = this.img;
        var aspect = width / height;
        var innerWidth = window.innerWidth;
        var innerHeight = window.innerHeight;
        if (enlarge) {
            width = innerWidth;
            height = width / aspect;
        }
        if (width > innerWidth) {
            width = innerWidth;
            height = width / aspect;
        }
        if (height > innerHeight) {
            height = innerHeight;
            width = height * aspect;
        }
        if (enlarge) {
            img.css("padding-top", (window.innerHeight - height) / 2 + "px");
            img.css("padding-bottom", (window.innerHeight - height) / 2 + "px");
            img.css("padding-left", (window.innerWidth - width) / 2 + "px");
            img.css("padding-right", (window.innerWidth - width) / 2 + "px");
        }
        img.attr('width', width);
        img.attr('height', height);
    };
    return ImageWidget;
}(Widget));
var ListWidget = (function (_super) {
    __extends(ListWidget, _super);
    function ListWidget(options) {
        _super.call(this, options);
    }
    ListWidget.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.ul = $("<ul></ul>")
            .appendTo(this.element);
    };
    ListWidget.prototype.empty = function () {
        this.ul.empty();
        this.element.removeClass("errors");
    };
    ListWidget.prototype.append_item = function (html) {
        var li = $("<li />")
            .append(html)
            .appendTo(this.ul);
        return li;
    };
    ListWidget.prototype.clear_status = function () {
        this.element.removeClass("errors");
    };
    ListWidget.prototype.display_error = function () {
        this.empty();
        this.element.addClass("errors");
    };
    return ListWidget;
}(Widget));
var ImageListWidget = (function (_super) {
    __extends(ImageListWidget, _super);
    // private images : Array<ImageWidget>
    function ImageListWidget(options) {
        _super.call(this, options);
    }
    ImageListWidget.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.element
            .addClass("photo_list");
    };
    ImageListWidget.prototype.empty = function () {
        // for (let image of this.images) {
        //     image.remove()
        // }
        _super.prototype.empty.call(this);
    };
    ImageListWidget.prototype.create_li = function (photo, title, details, description, a) {
        a
            .data("photo", null)
            .empty();
        var div = $("<div />");
        var image = new ImageWidget({
            photo: photo,
            size: "thumb",
            do_video: false,
            include_link: false
        });
        image.show(div);
        // this.images.push(image)
        div.appendTo(a);
        $("<div class='title'></div>")
            .text(title)
            .appendTo(a);
        if (details && details.length > 0) {
            $("<div class='details'></div>")
                .append(details)
                .appendTo(a);
        }
        var li = $("<li />")
            .attr('class', "photo_item")
            .append(a)
            .on("click", function (ev) {
            a.trigger('click');
        });
        return li;
    };
    // can this get deleted?
    ImageListWidget.prototype.append_photo_deleteme = function (photo, title, details, description, a) {
        var li = this.create_li(photo, title, details, description, a)
            .appendTo(this.ul);
        return li;
    };
    return ImageListWidget;
}(ListWidget));
