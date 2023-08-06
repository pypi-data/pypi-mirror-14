/// <reference path="signals.ts" />)
/// <reference path="globals.ts" />
/// <reference path="base.ts" />
/// <reference path="urls.ts" />
/// <reference path="dialog.ts" />
/// <reference path="widgets.ts" />
/// <reference path="session.ts" />
/// <reference path="state.ts" />
/// <reference path="DefinitelyTyped/jquery.d.ts" />
/// <reference path="DefinitelyTyped/jqueryui.d.ts" />
/*
spud - keep track of photos
Copyright (C) 2008-2013 Brian May

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
"use strict";
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
///////////////////////////////////////
// object_loader
///////////////////////////////////////
var ObjectLoader = (function () {
    function ObjectLoader(type, obj_id) {
        this.type = type;
        this.obj_id = obj_id;
        this.loading = false;
        this.finished = false;
        this.loaded_item = new Signal();
        this.on_error = new Signal();
    }
    ObjectLoader.prototype.load = function () {
        var _this = this;
        if (this.loading) {
            return;
        }
        if (this.finished) {
            return;
        }
        var mythis = this;
        var criteria = this.criteria;
        var page = this.page;
        var params = $.extend({}, criteria, { 'page': page });
        console.log("loading object", this.type, this.obj_id);
        this.loading = true;
        this.xhr = ajax({
            url: window.__api_prefix + "api/" + this.type + "/" + this.obj_id + "/",
            data: params
        }, function (data) {
            console.log("got object", mythis.type, mythis.obj_id);
            _this.loading = false;
            _this.finished = true;
            mythis.got_item(data);
        }, function (message, data) {
            _this.loading = false;
            console.log("error loading", mythis.type, mythis.obj_id, message);
            _this.on_error.trigger(null);
        });
    };
    ObjectLoader.prototype.abort = function () {
        if (this.loading) {
            this.xhr.abort();
        }
    };
    ObjectLoader.prototype.got_item = function (obj) {
        this.loaded_item.trigger(obj);
    };
    ObjectLoader.prototype.check_for_listeners = function () {
        if (this.loaded_item.is_any_listeners()) {
            return;
        }
        this.abort();
    };
    return ObjectLoader;
}());
function create_object_loader(type, obj_id) {
    return new ObjectLoader(type, obj_id);
}
var ObjectListLoader = (function () {
    function ObjectListLoader(type, criteria) {
        var _this = this;
        this.type = type;
        this.criteria = criteria;
        this.page = 1;
        this.n = 0;
        this.loading = false;
        this.finished = false;
        this.loaded_item = new Signal();
        this.loaded_item.on_no_listeners = function () { _this.check_for_listeners(); };
        this.loaded_list = new Signal();
        this.loaded_list.on_no_listeners = function () { _this.check_for_listeners(); };
        this.on_error = new Signal();
    }
    ObjectListLoader.prototype.load_next_page = function () {
        var _this = this;
        if (this.loading) {
            return true;
        }
        if (this.finished) {
            return false;
        }
        var mythis = this;
        var criteria = this.criteria;
        var page = this.page;
        var params = $.extend({}, criteria, { 'page': page });
        console.log("loading list", this.type, criteria, page);
        this.loading = true;
        this.xhr = ajax({
            url: window.__api_prefix + "api/" + this.type + "/",
            data: params
        }, function (data) {
            console.log("got list", mythis.type, criteria, page);
            _this.loading = false;
            _this.page = page + 1;
            if (!data['next']) {
                console.log("finished list", mythis.type, criteria, page);
                mythis.finished = true;
            }
            _this.got_list(data['results'], parse_number(data['count']));
        }, function (message, data) {
            _this.loading = false;
            console.log("error loading", mythis.type, criteria, message);
            _this.on_error.trigger(null);
        });
        return true;
    };
    ObjectListLoader.prototype.abort = function () {
        if (this.loading) {
            this.xhr.abort();
        }
    };
    ObjectListLoader.prototype.got_list = function (object_list, count) {
        for (var _i = 0, object_list_1 = object_list; _i < object_list_1.length; _i++) {
            var obj = object_list_1[_i];
            this.got_item(obj, count, this.n);
            this.n = this.n + 1;
        }
        // we trigger the object_list *after* all objects have been processed.
        var notification = {
            list: object_list,
            count: count
        };
        this.loaded_list.trigger(notification);
    };
    ObjectListLoader.prototype.got_item = function (obj, count, i) {
        var notification = {
            obj: obj,
            count: count,
            i: i
        };
        this.loaded_item.trigger(notification);
    };
    ObjectListLoader.prototype.check_for_listeners = function () {
        if (this.loaded_list.is_any_listeners()) {
            return;
        }
        if (this.loaded_item.is_any_listeners()) {
            return;
        }
        this.abort();
    };
    return ObjectListLoader;
}());
function create_object_list_loader(type, criteria) {
    return new ObjectListLoader(type, criteria);
}
var TrackedObjectListLoader = (function (_super) {
    __extends(TrackedObjectListLoader, _super);
    function TrackedObjectListLoader(type, criteria) {
        _super.call(this, type, criteria);
        this._last_id = null;
        this._idmap = {};
    }
    TrackedObjectListLoader.prototype.got_item = function (obj, count, n) {
        _super.prototype.got_item.call(this, obj, count, n);
        var id = obj.id;
        if (id != null) {
            this._idmap[id] = Object();
            if (this._last_id) {
                this._idmap[this._last_id].next = id;
                this._idmap[id].prev = this._last_id;
            }
            this._last_id = id;
        }
    };
    TrackedObjectListLoader.prototype.get_meta = function (obj_id) {
        var meta = this._idmap[obj_id];
        if (!meta) {
            return null;
        }
        if (!meta.next) {
            this.load_next_page();
        }
        return meta;
    };
    return TrackedObjectListLoader;
}(ObjectListLoader));
function create_tracked_object_list_loader(type, criteria) {
    return new TrackedObjectListLoader(type, criteria);
}
var ObjectSearchDialog = (function (_super) {
    __extends(ObjectSearchDialog, _super);
    function ObjectSearchDialog(options) {
        _super.call(this, options);
    }
    ObjectSearchDialog.prototype.submit_values = function (values) {
        var criteria = {};
        $.each(values, function (key, el) {
            if (el != null && el !== false) {
                criteria[key] = el;
            }
        });
        if (this.options.on_success(criteria)) {
            this.remove();
        }
    };
    return ObjectSearchDialog;
}(FormDialog));
var ObjectChangeDialog = (function (_super) {
    __extends(ObjectChangeDialog, _super);
    function ObjectChangeDialog(options) {
        _super.call(this, options);
    }
    ObjectChangeDialog.prototype.set = function (obj) {
        this.obj = obj;
        if (obj.id != null) {
            this.set_title("Change " + this.type_name);
            this.set_description("Please change " + this.type_name + " " + obj.title + ".");
        }
        else {
            this.set_title("Add new album");
            this.set_description("Please add new album.");
        }
        _super.prototype.set.call(this, obj);
    };
    ObjectChangeDialog.prototype.submit_values = function (values) {
        for (var key in values) {
            this.obj[key] = values[key];
        }
        var updates = this.obj.to_streamable();
        if (this.obj.id != null) {
            this.save("PATCH", this.obj.id, updates);
        }
        else {
            this.save("POST", null, updates);
        }
    };
    return ObjectChangeDialog;
}(FormDialog));
var ObjectDeleteDialog = (function (_super) {
    __extends(ObjectDeleteDialog, _super);
    function ObjectDeleteDialog(options) {
        _super.call(this, options);
    }
    ObjectDeleteDialog.prototype.show = function (element) {
        this.options.title = "Delete " + this.type_name;
        this.options.button = "Delete";
        _super.prototype.show.call(this, element);
    };
    ObjectDeleteDialog.prototype.set = function (obj) {
        this.obj_id = obj.id;
        this.set_description("Are you absolutely positively sure you really want to delete " +
            obj.title + "? Go ahead join the dark side. There are cookies.");
    };
    ObjectDeleteDialog.prototype.submit_values = function (values) {
        this.save("DELETE", this.obj_id, {});
    };
    return ObjectDeleteDialog;
}(FormDialog));
var ObjectCriteriaWidget = (function (_super) {
    __extends(ObjectCriteriaWidget, _super);
    function ObjectCriteriaWidget(options) {
        _super.call(this, options);
    }
    ObjectCriteriaWidget.prototype.show = function (element) {
        if (this.load_attributes == null) {
            this.load_attributes = [
                { name: 'instance', type: this.type }
            ];
        }
        _super.prototype.show.call(this, element);
        this.element.data('object_criteria', this);
        this.loaders = [];
        this.criteria = $("<ul/>")
            .addClass("criteria")
            .appendTo(this.element);
        if (this.options.obj) {
            this.load(this.options.obj);
        }
    };
    ObjectCriteriaWidget.prototype.finalize = function (criteria, title) {
        if (this.options.on_load != null) {
            this.options.on_load(criteria, title);
        }
    };
    ObjectCriteriaWidget.prototype.cancel_loaders = function () {
        var mythis = this;
        $.each(this.loaders, function (i, loader) {
            loader.loaded_item.remove_listener(mythis);
            loader.on_error.remove_listener(mythis);
        });
    };
    ObjectCriteriaWidget.prototype.load = function (criteria) {
        var _this = this;
        var mythis = this;
        this.cancel_loaders();
        this.set(criteria);
        var clone = $.extend({}, criteria);
        for (var id in this.load_attributes) {
            var value = this.load_attributes[id];
            if (criteria[value.name] == null) {
                continue;
            }
            var loader = create_object_loader(value.type, criteria[value.name]);
            loader.loaded_item.add_listener(mythis, function (obj) {
                clone[value.name] = obj.title;
                _this.set(clone);
            });
            loader.on_error.add_listener(this, function () {
                _this.element.addClass("error");
            });
            loader.load();
            this.loaders.push(loader);
        }
    };
    return ObjectCriteriaWidget;
}(Widget));
var ObjectListWidget = (function (_super) {
    __extends(ObjectListWidget, _super);
    function ObjectListWidget(options) {
        _super.call(this, options);
    }
    ObjectListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        this.element.data('object_list', this);
        this.page = 1;
        if (this.options.disabled) {
            this.element.addClass("disabled");
        }
        if (this.options.criteria != null) {
            this.filter(this.options.criteria);
        }
        this.element.scroll(function () {
            _this.load_if_required();
        });
        window._reload_all.add_listener(this, function () {
            _this.empty();
            _this.filter(_this.options.criteria);
        });
    };
    ObjectListWidget.prototype.get_item = function (obj_id) {
        return this.ul.find("[data-id=" + obj_id + "]");
    };
    ObjectListWidget.prototype.add_item = function (notification) {
        var obj = this.to_object(notification.obj);
        var li = this.create_li_for_obj(obj);
        li.appendTo(this.ul);
    };
    ObjectListWidget.prototype.add_list = function (notification) {
        this.element.toggleClass("hidden", notification.count === 0);
        this.load_if_required();
    };
    ObjectListWidget.prototype.load_if_required = function () {
        // if element is not displayed, we can't tell the scroll position,
        // so we must wait for element to be displayed before we can continue
        // loading
        if (!this.options.disabled && this.loader) {
            if (this.element.prop('scrollHeight') <
                this.element.scrollTop() + this.element.height() + 200) {
                this.loader.load_next_page();
            }
        }
    };
    ObjectListWidget.prototype.filter = function (criteria) {
        var _this = this;
        this.empty();
        this.options.criteria = criteria;
        this.loader = create_tracked_object_list_loader(this.type, criteria);
        this.loader.loaded_item.add_listener(this, this.add_item);
        this.loader.loaded_list.add_listener(this, this.add_list);
        this.loader.on_error.add_listener(this, function () {
            _this.element.addClass("error");
        });
        this.loader.load_next_page();
    };
    ObjectListWidget.prototype.empty = function () {
        this.page = 1;
        _super.prototype.empty.call(this);
        this.element.removeClass("error");
        if (this.loader) {
            this.loader.loaded_item.remove_listener(this);
            this.loader.loaded_list.remove_listener(this);
            this.loader.on_error.remove_listener(this);
            this.loader = null;
        }
    };
    ObjectListWidget.prototype.enable = function () {
        this.element.removeClass("disabled");
        this.load_if_required();
        _super.prototype.enable.call(this);
    };
    ObjectListWidget.prototype.disable = function () {
        this.element.addClass("disabled");
        _super.prototype.disable.call(this);
    };
    ObjectListWidget.prototype.get_child_viewport = function () {
        var child_id = this.options.child_id;
        if (child_id != null) {
            var child = $(document.getElementById(child_id));
            if (child.length > 0) {
                var viewport = child.data('widget');
                return viewport;
            }
        }
        return null;
    };
    ObjectListWidget.prototype.get_or_create_child_viewport = function () {
        var viewport = this.get_child_viewport();
        if (viewport != null) {
            return viewport;
        }
        viewport = this.create_child_viewport();
        return viewport;
    };
    ObjectListWidget.prototype.obj_a = function (obj) {
        var _this = this;
        var mythis = this;
        var album_list_loader = this.loader;
        var title = obj.title;
        var a = $('<a/>')
            .attr('href', root_url() + this.type + "/" + obj.id + "/")
            .on('click', function () {
            if (mythis.options.disabled) {
                return false;
            }
            var viewport = _this.get_or_create_child_viewport();
            viewport.set_loader(album_list_loader);
            // We cannot use set(obj) here as required attributes may be
            // missing from list view for detail view
            viewport.load(obj.id);
            return false;
        })
            .data('photo', obj.cover_photo)
            .text(title);
        return a;
    };
    ObjectListWidget.prototype.get_photo = function (obj) {
        return obj.cover_photo;
    };
    ObjectListWidget.prototype.get_details = function (obj) {
        var details = [];
        return details;
    };
    ObjectListWidget.prototype.get_description = function (obj) {
        return null;
    };
    ObjectListWidget.prototype.create_li_for_obj = function (obj) {
        var photo = this.get_photo(obj);
        var details = this.get_details(obj);
        var description = this.get_description(obj);
        var a = this.obj_a(obj);
        var li = this.create_li(photo, obj.title, details, description, a);
        li.attr('data-id', obj.id);
        return li;
    };
    return ObjectListWidget;
}(ImageListWidget));
var ObjectListViewport = (function (_super) {
    __extends(ObjectListViewport, _super);
    function ObjectListViewport(options) {
        _super.call(this, options);
    }
    ObjectListViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        var mythis = this;
        menu.append($("<li/>")
            .text("Filter")
            .on("click", function (ev) {
            void ev;
            var params = {
                obj: mythis.options.criteria,
                on_success: function (criteria) {
                    mythis.filter(criteria);
                    return true;
                }
            };
            var div = $("<div/>");
            var dialog = _this.create_object_search_dialog(params);
            dialog.show(div);
        }));
    };
    ObjectListViewport.prototype.show = function (element) {
        var mythis = this;
        if (!this.options.criteria) {
            this.options.criteria = {};
        }
        this.options.title = this.type_name + " list";
        _super.prototype.show.call(this, element);
        var menu = $("<ul/>")
            .addClass("menubar");
        this.setup_menu(menu);
        menu.menu()
            .appendTo(this.div);
        var oc_params = {
            'obj': this.options.criteria,
            'on_load': function (criteria, title) {
                mythis.set_title(mythis.type_name + " list: " + title);
            }
        };
        this.criteria = $("<div/>").appendTo(this.div);
        var oc = this.create_object_criteria_widget(oc_params);
        oc.show(this.criteria);
        var ol_params = {
            'child_id': this.options.id + ".child",
            'criteria': this.options.criteria,
            'disabled': this.options.disabled
        };
        if (this.options.object_list_options != null) {
            ol_params = $.extend({}, this.options.object_list_options, ol_params);
        }
        this.ol = this.create_object_list_widget(ol_params);
        $("<div/>")
            .set_widget(this.ol)
            .appendTo(this.div);
    };
    ObjectListViewport.prototype.filter = function (value) {
        this.options.criteria = value;
        push_state();
        var instance = this.criteria.data('object_criteria');
        instance.load(value);
        this.ol.filter(value);
    };
    ObjectListViewport.prototype._enable = function () {
        _super.prototype._enable.call(this);
        if (this.ol != null) {
            this.ol.enable();
        }
    };
    ObjectListViewport.prototype._disable = function () {
        _super.prototype._disable.call(this);
        if (this.ol != null) {
            this.ol.disable();
        }
    };
    ObjectListViewport.prototype.get_url = function () {
        var params = "";
        if (!$.isEmptyObject(this.options.criteria)) {
            params = "?" + $.param(this.options.criteria);
        }
        return root_url() + this.type + "/" + params;
    };
    ObjectListViewport.prototype.get_streamable_options = function () {
        var streamable = _super.prototype.get_streamable_options.call(this);
        streamable['criteria'] = this.options.criteria;
        return streamable;
    };
    ;
    return ObjectListViewport;
}(Viewport));
var ObjectDetailViewport = (function (_super) {
    __extends(ObjectDetailViewport, _super);
    function ObjectDetailViewport(options) {
        _super.call(this, options);
        this.display_photo_list_link = true;
    }
    ObjectDetailViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        var mythis = this;
        menu.append($("<li/>")
            .text("Children")
            .on("click", function (ev) {
            var options = {
                criteria: mythis.get_children_criteria()
            };
            var viewport = mythis.create_object_list_viewport(options);
            add_viewport(viewport);
        }));
        if (this.display_photo_list_link) {
            menu.append($("<li/>")
                .text("Photos")
                .on("click", function (ev) {
                var options = {
                    criteria: mythis.get_photo_criteria()
                };
                var viewport = mythis.get_photo_list_viewport(options);
                add_viewport(viewport);
            }));
        }
        this.create_item = $("<li/>")
            .text("Create")
            .on("click", function (ev) {
            void ev;
            if (mythis.options.obj != null) {
                var obj = {
                    parent: mythis.options.obj.id
                };
                var params = {
                    obj: obj
                };
                var div = $("<div/>");
                var dialog = _this.create_object_change_dialog(params);
                dialog.show(div);
            }
        })
            .appendTo(menu);
        this.change_item = $("<li/>")
            .text("Change")
            .on("click", function (ev) {
            if (mythis.options.obj != null) {
                var params = {
                    obj: mythis.options.obj
                };
                var div = $("<div/>");
                var dialog = _this.create_object_change_dialog(params);
                dialog.show(div);
            }
        })
            .appendTo(menu);
        this.delete_item = $("<li/>")
            .text("Delete")
            .on("click", function (ev) {
            if (mythis.options.obj != null) {
                var params = {
                    obj: mythis.options.obj
                };
                var div = $("<div/>");
                var dialog = _this.create_object_delete_dialog(params);
                dialog.show(div);
            }
        })
            .appendTo(menu);
    };
    ObjectDetailViewport.prototype.show = function (element) {
        var _this = this;
        var mythis = this;
        this.options.title = this.type_name + " Detail";
        if (this.options.obj != null) {
            var tmp_obj = this.options.obj;
            this.options.obj_id = tmp_obj.id;
            this.options.title = this.type_name + ": " + tmp_obj.title;
        }
        _super.prototype.show.call(this, element);
        var menu = $("<ul/>")
            .addClass("menubar");
        this.setup_menu(menu);
        menu
            .menu()
            .appendTo(this.div);
        var button_div = $("<div/>").appendTo(this.div);
        this.prev_button = $("<input/>")
            .attr('type', 'submit')
            .attr('value', '<<')
            .click(function () {
            var oll = mythis.options.object_list_loader;
            var meta = oll.get_meta(mythis.options.obj_id);
            var obj_id = meta.prev;
            if (obj_id) {
                mythis.load(obj_id);
            }
            push_state();
        })
            .button()
            .appendTo(button_div);
        this.next_button = $("<input/>")
            .attr('type', 'submit')
            .attr('value', '>>')
            .click(function () {
            var oll = mythis.options.object_list_loader;
            var meta = oll.get_meta(mythis.options.obj_id);
            var obj_id = meta.next;
            if (obj_id) {
                mythis.load(obj_id);
            }
            push_state();
        })
            .button()
            .appendTo(button_div);
        this.setup_loader();
        this.setup_buttons();
        this.od = this.create_object_detail_infobox({});
        $("<div/>")
            .set_widget(this.od)
            .appendTo(this.div);
        var params = {
            'criteria': {},
            'child_id': this.options.id + ".child",
            'disabled': this.options.disabled
        };
        this.ol = this.create_object_list_widget(params);
        $("<div/>")
            .set_widget(this.ol)
            .appendTo(this.div);
        if (this.options.obj != null) {
            this.set(this.options.obj);
        }
        else if (this.options.obj_id != null) {
            this.load(this.options.obj_id);
        }
        this.setup_perms(window._perms);
        window._perms_changed.add_listener(this, this.setup_perms);
        window._reload_all.add_listener(this, function () {
            mythis.load(_this.options.obj_id);
        });
    };
    ObjectDetailViewport.prototype.get_children_criteria = function () {
        return {
            'instance': this.options.obj_id,
            'mode': 'children'
        };
    };
    ObjectDetailViewport.prototype.setup_loader = function () {
        var mythis = this;
        if (this.options.object_list_loader != null) {
            var oll = this.options.object_list_loader;
            oll.loaded_list.add_listener(this, function (notification) {
                mythis.setup_buttons();
            });
        }
    };
    ObjectDetailViewport.prototype.setup_perms = function (perms) {
        var can_create = false;
        var can_change = false;
        var can_delete = false;
        if (perms[this.type] != null) {
            var perms_for_type = perms[this.type];
            can_create = perms_for_type.can_create;
            can_change = perms_for_type.can_change;
            can_delete = perms_for_type.can_delete;
        }
        this.create_item.toggle(can_create);
        this.change_item.toggle(can_change);
        this.delete_item.toggle(can_delete);
        if (this.options.obj_id != null) {
            this.load(this.options.obj_id);
        }
    };
    ObjectDetailViewport.prototype.setup_buttons = function () {
        if (this.options.object_list_loader) {
            var oll = this.options.object_list_loader;
            var meta = null;
            if (this.options.obj_id) {
                meta = oll.get_meta(this.options.obj_id);
            }
            this.prev_button.show();
            this.next_button.show();
            if (meta != null && meta.prev) {
                this.prev_button.button("enable");
            }
            else {
                this.prev_button.button("disable");
            }
            if (meta && meta.next) {
                this.next_button.button("enable");
            }
            else {
                this.next_button.button("disable");
            }
        }
        else {
            this.prev_button.hide();
            this.next_button.hide();
        }
    };
    ObjectDetailViewport.prototype.set = function (obj) {
        this.options.obj = obj;
        this.options.obj_id = obj.id;
        this.od.set(obj);
        this.loaded(obj);
    };
    ObjectDetailViewport.prototype.load = function (obj_id) {
        var _this = this;
        this.options.obj = null;
        this.options.obj_id = obj_id;
        if (this.loader != null) {
            this.loader.loaded_item.remove_listener(this);
        }
        this.loader = create_object_loader(this.type, obj_id);
        this.loader.loaded_item.add_listener(this, function (obj) {
            _this.loader = null;
            _this.loaded(_this.to_object(obj));
        });
        this.loader.on_error.add_listener(this, function () {
            _this.element.addClass("error");
            _this.loader = null;
            _this.loaded_error();
        });
        this.loader.load();
    };
    ObjectDetailViewport.prototype.loaded = function (obj) {
        this.element.removeClass("error");
        this.options.obj = obj;
        this.options.obj_id = obj.id;
        this.set_title(this.type + ": " + obj.title);
        this.setup_buttons();
        this.od.set(obj);
        this.ol.filter(this.get_children_criteria());
    };
    ObjectDetailViewport.prototype.loaded_error = function () {
        this.element.addClass("error");
    };
    ObjectDetailViewport.prototype.set_loader = function (oll) {
        var old_loader = this.options.object_list_loader;
        if (old_loader != null) {
            old_loader.loaded_list.remove_listener(this);
        }
        this.options.object_list_loader = oll;
        this.setup_loader();
        this.setup_buttons();
    };
    ObjectDetailViewport.prototype._enable = function () {
        _super.prototype._enable.call(this);
        if (this.ol) {
            this.ol.enable();
        }
    };
    ObjectDetailViewport.prototype._disable = function () {
        _super.prototype._disable.call(this);
        if (this.ol) {
            this.ol.disable();
        }
    };
    ObjectDetailViewport.prototype.get_url = function () {
        return root_url() + this.type + "/" + this.options.obj_id + "/";
    };
    ObjectDetailViewport.prototype.get_photo_list_viewport = function (options) {
        return new PhotoListViewport(options);
    };
    ObjectDetailViewport.prototype.get_streamable_options = function () {
        var streamable = _super.prototype.get_streamable_options.call(this);
        streamable['obj_id'] = this.options.obj_id;
        return streamable;
    };
    ;
    return ObjectDetailViewport;
}(Viewport));
