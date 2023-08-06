/// <reference path="signals.ts" />
/// <reference path="globals.ts" />
/// <reference path="base.ts" />
/// <reference path="dialog.ts" />
/// <reference path="infobox.ts" />
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
window._album_created = new Signal();
window._album_changed = new Signal();
window._album_deleted = new Signal();
var AlbumStreamable = (function (_super) {
    __extends(AlbumStreamable, _super);
    function AlbumStreamable() {
        _super.apply(this, arguments);
    }
    return AlbumStreamable;
}(ObjectStreamable));
var Album = (function (_super) {
    __extends(Album, _super);
    function Album(streamable) {
        _super.call(this, streamable);
        this.description = parse_string(streamable.description);
        this.sort_order = parse_string(streamable.sort_order);
        this.sort_name = parse_string(streamable.sort_name);
        this.revised = parse_datetimezone(streamable.revised, streamable.revised_utc_offset);
        if (streamable.ascendants != null) {
            this.ascendants = [];
            for (var i = 0; i < streamable.ascendants.length; i++) {
                this.ascendants.push(new Album(streamable.ascendants[i]));
            }
            if (streamable.ascendants.length > 0) {
                this.parent = this.ascendants[0];
            }
            else {
                this.parent = null;
            }
        }
    }
    Album.prototype.to_streamable = function () {
        var streamable = _super.prototype.to_streamable.call(this);
        streamable.description = this.description;
        streamable.sort_order = this.sort_order;
        streamable.sort_name = this.sort_name;
        streamable.revised_utc_offset = streamable_datetimezone_offset(this.revised);
        streamable.revised = streamable_datetimezone_datetime(this.revised);
        if (this.parent != null) {
            streamable.parent = this.parent.id;
        }
        else {
            streamable.parent = null;
        }
        return streamable;
    };
    Album.type = "albums";
    return Album;
}(SpudObject));
var AlbumSearchDialog = (function (_super) {
    __extends(AlbumSearchDialog, _super);
    function AlbumSearchDialog(options) {
        _super.call(this, options);
    }
    AlbumSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Album", "albums", false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
            ["needs_revision", new booleanInputField("Needs revision", false)],
        ];
        this.options.title = "Search albums";
        this.options.description = "Please search for an album.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return AlbumSearchDialog;
}(ObjectSearchDialog));
var AlbumChangeDialog = (function (_super) {
    __extends(AlbumChangeDialog, _super);
    function AlbumChangeDialog(options) {
        _super.call(this, options);
        this.type = "albums";
        this.type_name = "album";
    }
    AlbumChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["description", new PInputField("Description", false)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["sort_name", new TextInputField("Sort Name", false)],
            ["sort_order", new TextInputField("Sort Order", false)],
            ["parent", new AjaxSelectField("Parent", "albums", false)],
            ["revised", new DateTimeInputField("Revised", false)],
        ];
        this.options.title = "Change album";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    AlbumChangeDialog.prototype.save_success = function (data) {
        var album = new Album(data);
        if (this.obj.id != null) {
            window._album_changed.trigger(album);
        }
        else {
            window._album_created.trigger(album);
        }
        _super.prototype.save_success.call(this, data);
    };
    return AlbumChangeDialog;
}(ObjectChangeDialog));
var AlbumDeleteDialog = (function (_super) {
    __extends(AlbumDeleteDialog, _super);
    function AlbumDeleteDialog(options) {
        _super.call(this, options);
        this.type = "albums";
        this.type_name = "album";
    }
    AlbumDeleteDialog.prototype.save_success = function (data) {
        window._album_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return AlbumDeleteDialog;
}(ObjectDeleteDialog));
var AlbumCriteriaWidget = (function (_super) {
    __extends(AlbumCriteriaWidget, _super);
    function AlbumCriteriaWidget(options) {
        _super.call(this, options);
        this.type = "albums";
    }
    AlbumCriteriaWidget.prototype.set = function (input_criteria) {
        var mythis = this;
        mythis.element.removeClass("error");
        // this.options.criteria = criteria
        var ul = this.criteria;
        this.criteria.empty();
        var criteria = $.extend({}, input_criteria);
        var title = null;
        var mode = criteria.mode || 'children';
        delete criteria.mode;
        if (criteria.instance != null) {
            var instance = criteria.instance;
            title = instance + " / " + mode;
            $("<li/>")
                .text("instance" + " = " + instance + " (" + mode + ")")
                .appendTo(ul);
            delete criteria.instance;
        }
        else if (criteria.q != null) {
            title = "search " + criteria.q;
        }
        else if (criteria.root_only) {
            title = "root only";
        }
        else if (criteria.needs_revision) {
            title = "needs revision";
        }
        else {
            title = "All";
        }
        $.each(criteria, function (index, value) {
            $("<li/>")
                .text(index + " = " + value)
                .appendTo(ul);
        });
        this.finalize(input_criteria, title);
    };
    return AlbumCriteriaWidget;
}(ObjectCriteriaWidget));
var AlbumListWidget = (function (_super) {
    __extends(AlbumListWidget, _super);
    function AlbumListWidget(options) {
        _super.call(this, options);
        this.type = "albums";
    }
    AlbumListWidget.prototype.to_object = function (streamable) {
        return new Album(streamable);
    };
    AlbumListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._album_changed.add_listener(this, function (album) {
            var li = _this.create_li_for_obj(album);
            _this.get_item(album.id).replaceWith(li);
        });
        window._album_deleted.add_listener(this, function (album_id) {
            _this.get_item(album_id).remove();
            _this.load_if_required();
        });
    };
    AlbumListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            obj: null,
            obj_id: null
        };
        var viewport;
        viewport = new AlbumDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    AlbumListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        if (obj.sort_order || obj.sort_name) {
            details.push($("<div/>").text(obj.sort_name + " " + obj.sort_order));
        }
        return details;
    };
    AlbumListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    return AlbumListWidget;
}(ObjectListWidget));
var AlbumDetailInfobox = (function (_super) {
    __extends(AlbumDetailInfobox, _super);
    function AlbumDetailInfobox(options) {
        _super.call(this, options);
    }
    AlbumDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextOutputField("Title")],
            ["sort_name", new TextOutputField("Sort Name")],
            ["sort_order", new TextOutputField("Sort Order")],
            ["revised", new DateTimeOutputField("Revised")],
            ["description", new POutputField("Description")],
            ["ascendants", new LinkListOutputField("Ascendants", "albums")],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    AlbumDetailInfobox.prototype.set = function (album) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, album);
        this.options.obj = album;
        this.img.set(album.cover_photo);
    };
    return AlbumDetailInfobox;
}(Infobox));
var AlbumListViewport = (function (_super) {
    __extends(AlbumListViewport, _super);
    function AlbumListViewport(options) {
        _super.call(this, options);
        this.type = "albums";
        this.type_name = "Album";
    }
    AlbumListViewport.prototype.create_object_list_widget = function (options) {
        return new AlbumListWidget(options);
    };
    AlbumListViewport.prototype.create_object_criteria_widget = function (options) {
        return new AlbumCriteriaWidget(options);
    };
    AlbumListViewport.prototype.create_object_search_dialog = function (options) {
        return new AlbumSearchDialog(options);
    };
    return AlbumListViewport;
}(ObjectListViewport));
var AlbumDetailViewport = (function (_super) {
    __extends(AlbumDetailViewport, _super);
    function AlbumDetailViewport(options) {
        _super.call(this, options);
        this.type = "albums";
        this.type_name = "Album";
    }
    AlbumDetailViewport.prototype.to_object = function (streamable) {
        return new Album(streamable);
    };
    AlbumDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        var mythis = this;
        window._album_changed.add_listener(this, function (obj) {
            if (obj.id === _this.options.obj_id) {
                mythis.set(obj);
            }
        });
        window._album_deleted.add_listener(this, function (obj_id) {
            if (obj_id === _this.options.obj_id) {
                mythis.remove();
            }
        });
    };
    AlbumDetailViewport.prototype.get_photo_criteria = function () {
        return {
            'album': this.options.obj_id,
            'album_descendants': true
        };
    };
    AlbumDetailViewport.prototype.create_object_list_widget = function (options) {
        return new AlbumListWidget(options);
    };
    AlbumDetailViewport.prototype.create_object_detail_infobox = function (options) {
        return new AlbumDetailInfobox(options);
    };
    AlbumDetailViewport.prototype.create_object_list_viewport = function (options) {
        return new AlbumListViewport(options);
    };
    AlbumDetailViewport.prototype.create_object_change_dialog = function (options) {
        return new AlbumChangeDialog(options);
    };
    AlbumDetailViewport.prototype.create_object_delete_dialog = function (options) {
        return new AlbumDeleteDialog(options);
    };
    return AlbumDetailViewport;
}(ObjectDetailViewport));
