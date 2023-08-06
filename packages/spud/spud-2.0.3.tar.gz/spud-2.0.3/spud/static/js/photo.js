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
window._photo_created = new Signal();
window._photo_changed = new Signal();
window._photo_deleted = new Signal();
var PhotoThumbStreamable = (function (_super) {
    __extends(PhotoThumbStreamable, _super);
    function PhotoThumbStreamable() {
        _super.apply(this, arguments);
    }
    return PhotoThumbStreamable;
}(Streamable));
var PhotoVideoStreamable = (function (_super) {
    __extends(PhotoVideoStreamable, _super);
    function PhotoVideoStreamable() {
        _super.apply(this, arguments);
    }
    return PhotoVideoStreamable;
}(Streamable));
var PriorityPhotoVideoStreamable = (function () {
    function PriorityPhotoVideoStreamable() {
    }
    return PriorityPhotoVideoStreamable;
}());
var PhotoStreamable = (function (_super) {
    __extends(PhotoStreamable, _super);
    function PhotoStreamable() {
        _super.apply(this, arguments);
    }
    return PhotoStreamable;
}(ObjectStreamable));
var PhotoThumb = (function () {
    function PhotoThumb() {
    }
    return PhotoThumb;
}());
var PhotoVideo = (function () {
    function PhotoVideo() {
    }
    return PhotoVideo;
}());
var PriorityPhotoVideo = (function () {
    function PriorityPhotoVideo() {
    }
    return PriorityPhotoVideo;
}());
var Photo = (function (_super) {
    __extends(Photo, _super);
    function Photo(streamable) {
        _super.call(this, streamable);
        this.action = parse_string(streamable.action);
        this.datetime = parse_datetimezone(streamable.datetime, streamable.datetime_utc_offset);
        this.description = parse_string(streamable.description);
        this.camera_make = parse_string(streamable.camera_make);
        this.camera_model = parse_string(streamable.camera_model);
        this.flash_used = parse_string(streamable.flash_used);
        this.focal_length = parse_string(streamable.focal_length);
        this.exposure = parse_string(streamable.exposure);
        this.aperture = parse_string(streamable.aperture);
        this.iso_equiv = parse_string(streamable.iso_equiv);
        this.metering_mode = parse_string(streamable.metering_mode);
        if (streamable.albums != null) {
            this.albums = [];
            for (var i = 0; i < streamable.albums.length; i++) {
                var album = streamable.albums[i];
                this.albums.push(new Album(album));
            }
        }
        if (streamable.categorys != null) {
            this.categorys = [];
            for (var i = 0; i < streamable.categorys.length; i++) {
                var category = streamable.categorys[i];
                this.categorys.push(new Category(category));
            }
        }
        if (streamable.persons != null) {
            this.persons = [];
            for (var i = 0; i < streamable.persons.length; i++) {
                var person = streamable.persons[i];
                this.persons.push(new Person(person));
            }
        }
        if (streamable.photographer != null) {
            this.photographer = new Person(streamable.photographer);
        }
        if (streamable.place != null) {
            this.place = new Place(streamable.place);
        }
        this.orig_url = streamable.orig_url;
        this.thumbs = {};
        for (var size in streamable.thumbs) {
            var thumb = new PhotoThumb();
            thumb.width = parse_number(streamable.thumbs[size].width);
            thumb.height = parse_number(streamable.thumbs[size].height);
            thumb.url = parse_string(streamable.thumbs[size].url);
            this.thumbs[size] = thumb;
        }
        this.videos = {};
        for (var size in streamable.videos) {
            this.videos[size] = [];
            for (var i = 0; i < streamable.videos[size].length; i++) {
                var pv = streamable.videos[size][i];
                var priority = parse_number(pv[0]);
                var svideo = pv[1];
                var video = new PhotoVideo();
                video.width = parse_number(svideo.width);
                video.height = parse_number(svideo.height);
                video.url = parse_string(svideo.url);
                video.format = parse_string(svideo.format);
                this.videos[size].push([priority, video]);
            }
        }
    }
    Photo.prototype.to_streamable = function () {
        var streamable = _super.prototype.to_streamable.call(this);
        streamable.action = this.action;
        streamable.datetime_utc_offset = streamable_datetimezone_offset(this.datetime);
        streamable.datetime = streamable_datetimezone_datetime(this.datetime);
        streamable.description = this.description;
        streamable.camera_make = this.camera_make;
        streamable.camera_model = this.camera_model;
        streamable.flash_used = this.flash_used;
        streamable.focal_length = this.focal_length;
        streamable.exposure = this.exposure;
        streamable.aperture = this.aperture;
        streamable.iso_equiv = this.iso_equiv;
        streamable.metering_mode = this.metering_mode;
        streamable.albums_pk = [];
        for (var i = 0; i < this.albums.length; i++) {
            streamable.albums_pk.push(this.albums[i].id);
        }
        streamable.categorys_pk = [];
        for (var i = 0; i < this.categorys.length; i++) {
            streamable.categorys_pk.push(this.categorys[i].id);
        }
        streamable.persons_pk = [];
        for (var i = 0; i < this.persons.length; i++) {
            streamable.persons_pk.push(this.persons[i].id);
        }
        streamable.photographer_pk = null;
        if (this.photographer != null) {
            streamable.photographer_pk = this.photographer.id;
        }
        streamable.place_pk = null;
        if (this.place != null) {
            streamable.place_pk = this.place.id;
        }
        return streamable;
    };
    return Photo;
}(SpudObject));
var PhotoSearchDialog = (function (_super) {
    __extends(PhotoSearchDialog, _super);
    function PhotoSearchDialog(options) {
        _super.call(this, options);
    }
    PhotoSearchDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["q", new TextInputField("Search for", false)],
                    ["first_datetime", new DateTimeInputField("First date", false)],
                    ["last_datetime", new DateTimeInputField("Last date", false)],
                    ["lower_rating", new IntegerInputField("Upper rating", false)],
                    ["upper_rating", new IntegerInputField("Lower rating", false)],
                    ["title", new TextInputField("Title", false)],
                    ["photographer", new AjaxSelectField("Photographer", "persons", false)],
                    ["path", new TextInputField("Path", false)],
                    ["name", new TextInputField("Name", false)],
                    ["first_id", new IntegerInputField("First id", false)],
                    ["last_id", new IntegerInputField("Last id", false)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    ["album", new AjaxSelectField("Album", "albums", false)],
                    ["album_descendants", new booleanInputField("Descend albums", false)],
                    ["album_none", new booleanInputField("No albums", false)],
                    ["category", new AjaxSelectField("Category", "categorys", false)],
                    ["category_descendants", new booleanInputField("Descend categories", false)],
                    ["category_none", new booleanInputField("No categories", false)],
                    ["place", new AjaxSelectField("Place", "places", false)],
                    ["place_descendants", new booleanInputField("Descend places", false)],
                    ["place_none", new booleanInputField("No places", false)],
                    ["person", new AjaxSelectField("Person", "persons", false)],
                    ["person_none", new booleanInputField("No people", false)],
                    ["person_descendants", new booleanInputField("Descend people", false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Search photos";
        this.options.description = "Please search for an photo.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PhotoSearchDialog;
}(ObjectSearchDialog));
var PhotoChangeDialog = (function (_super) {
    __extends(PhotoChangeDialog, _super);
    function PhotoChangeDialog(options) {
        _super.call(this, options);
        this.type = "photos";
        this.type_name = "photo";
    }
    PhotoChangeDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["datetime", new DateTimeInputField("Date", true)],
                    ["title", new TextInputField("Title", true)],
                    ["photographer", new AjaxSelectField("Photographer", "persons", false)],
                    ["action", new SelectInputField("Action", [
                            ["", "no action"],
                            ["D", "delete"],
                            ["R", "regenerate thumbnails & video"],
                            ["M", "move photo"],
                            ["auto", "rotate automatic"],
                            ["90", "rotate 90 degrees clockwise"],
                            ["180", "rotate 180 degrees clockwise"],
                            ["270", "rotate 270 degrees clockwise"],
                        ], false)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    ["albums", new AjaxSelectMultipleField("Album", "albums", false)],
                    ["categorys", new AjaxSelectMultipleField("Category", "categorys", false)],
                    ["place", new AjaxSelectField("Place", "places", false)],
                    ["persons", new AjaxSelectSortedField("Person", "persons", false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Change photo";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PhotoChangeDialog.prototype.save_success = function (data) {
        var photo = new Photo(data);
        if (this.obj.id != null) {
            window._photo_changed.trigger(photo);
        }
        else {
            window._photo_created.trigger(photo);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PhotoChangeDialog;
}(ObjectChangeDialog));
var PhotoBulkUpdateDialog = (function (_super) {
    __extends(PhotoBulkUpdateDialog, _super);
    function PhotoBulkUpdateDialog(options) {
        _super.call(this, options);
        this.type = "photos";
    }
    PhotoBulkUpdateDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["datetime", new DateTimeInputField("Date", false)],
                    ["title", new TextInputField("Title", false)],
                    ["photographer", new AjaxSelectField("Photographer", "persons", false)],
                    ["place", new AjaxSelectField("Place", "places", false)],
                    ["action", new SelectInputField("Action", [
                            ["none", "no action"],
                            ["D", "delete"],
                            ["R", "regenerate thumbnails & video"],
                            ["M", "move photo"],
                            ["auto", "rotate automatic"],
                            ["90", "rotate 90 degrees clockwise"],
                            ["180", "rotate 180 degrees clockwise"],
                            ["270", "rotate 270 degrees clockwise"],
                        ], false)],
                ] },
            { name: 'add', title: 'Add', fields: [
                    ["add_albums", new AjaxSelectMultipleField("Album", "albums", false)],
                    ["add_categorys", new AjaxSelectMultipleField("Category", "categorys", false)],
                    ["add_persons", new AjaxSelectSortedField("Person", "persons", false)],
                ] },
            { name: 'rem', title: 'Remove', fields: [
                    ["rem_albums", new AjaxSelectMultipleField("Album", "albums", false)],
                    ["rem_categorys", new AjaxSelectMultipleField("Category", "categorys", false)],
                    ["rem_persons", new AjaxSelectSortedField("Person", "persons", false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Bulk photo update";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PhotoBulkUpdateDialog.prototype.set = function (photo) {
        _super.prototype.set.call(this, photo);
    };
    PhotoBulkUpdateDialog.prototype.submit_values = function (values) {
        var data = {};
        if (values["datetime"] != null) {
            data.datetime = values["datetime"];
        }
        if (values["title"] != null) {
            data.title = values["title"];
        }
        if (values["photographer"] != null) {
            data.photographer_pk = values["photographer"].id;
        }
        if (values["place"] != null) {
            data.place_pk = values["place"].id;
        }
        if (values["action"] != null) {
            data.action = null;
            if (values["action"] != "none") {
                data.action = values["action"];
            }
        }
        data.add_albums_pk = [];
        for (var i = 0; i < values["add_albums"].length; i++) {
            data.add_albums_pk.push(values["add_albums"][i].id);
        }
        data.rem_albums_pk = [];
        for (var i = 0; i < values["rem_albums"].length; i++) {
            data.rem_albums_pk.push(values["rem_albums"][i].id);
        }
        data.add_categorys_pk = [];
        for (var i = 0; i < values["add_categorys"].length; i++) {
            data.add_categorys_pk.push(values["add_categorys"][i].id);
        }
        data.rem_categorys_pk = [];
        for (var i = 0; i < values["rem_categorys"].length; i++) {
            data.rem_categorys_pk.push(values["rem_categorys"][i].id);
        }
        data.add_persons_pk = [];
        for (var i = 0; i < values["add_persons"].length; i++) {
            data.add_persons_pk.push(values["add_persons"][i].id);
        }
        data.rem_persons_pk = [];
        for (var i = 0; i < values["rem_persons"].length; i++) {
            data.rem_persons_pk.push(values["rem_persons"][i].id);
        }
        if (values["camera_make"] != null) {
            data.camera_make = values["camera_make"];
        }
        if (values["camera_model"] != null) {
            data.camera_model = values["camera_model"];
        }
        this.data = data;
        this.element.hide();
        var params = {
            criteria: this.options.criteria,
            obj: data,
            on_proceed: $.proxy(this.proceed, this),
            on_cancel: $.proxy(this.cancel, this)
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkConfirmDialog(params);
        dialog.show(div);
    };
    PhotoBulkUpdateDialog.prototype.proceed = function () {
        this.remove();
        var params = {
            criteria: this.options.criteria,
            obj: this.data
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkProceedDialog(params);
        dialog.show(div);
    };
    PhotoBulkUpdateDialog.prototype.cancel = function () {
        this.element.show();
        this.enable();
    };
    return PhotoBulkUpdateDialog;
}(FormDialog));
var PhotoBulkConfirmDialog = (function (_super) {
    __extends(PhotoBulkConfirmDialog, _super);
    function PhotoBulkConfirmDialog(options) {
        options.title = "Confirm bulk update";
        options.button = "Confirm";
        _super.call(this, options);
        this.proceed = false;
        this.type = "photos";
    }
    PhotoBulkConfirmDialog.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.ul = $("<ul/>").appendTo(this.element);
        this.ol = $("<div/>").appendTo(this.element);
        var options = {};
        this.photo_list = new PhotoListWidget(options);
        this.photo_list.show(this.ol);
        this.set(this.options.criteria);
    };
    PhotoBulkConfirmDialog.prototype.set = function (values) {
        var _this = this;
        this.ul.empty();
        $.each(values, function (key, value) {
            $("<li/>").text(key + " = " + value)
                .appendTo(_this.ul);
        });
        this.photo_list.filter(this.options.criteria);
    };
    PhotoBulkConfirmDialog.prototype.disable = function () {
        this.photo_list.disable();
        _super.prototype.disable.call(this);
    };
    PhotoBulkConfirmDialog.prototype.enable = function () {
        this.photo_list.enable();
        _super.prototype.enable.call(this);
    };
    PhotoBulkConfirmDialog.prototype.submit = function () {
        this.proceed = true;
        this.remove();
    };
    PhotoBulkConfirmDialog.prototype.destroy = function () {
        _super.prototype.destroy.call(this);
        if (this.proceed) {
            this.options.on_proceed();
        }
        else {
            this.options.on_cancel();
        }
    };
    return PhotoBulkConfirmDialog;
}(BaseDialog));
var PhotoBulkProceedDialog = (function (_super) {
    __extends(PhotoBulkProceedDialog, _super);
    function PhotoBulkProceedDialog(options) {
        options.title = "Bulk update";
        options.button = "Retry";
        _super.call(this, options);
        this.type = "photos";
    }
    PhotoBulkProceedDialog.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.pb = $("<div/>").appendTo(this.element);
        this.pb.progressbar({ value: false });
        this.status = $("<div/>")
            .text("Please wait")
            .appendTo(this.element);
        this.set(this.options.obj);
    };
    PhotoBulkProceedDialog.prototype.set = function (values) {
        this.values = values;
        this.check_submit();
    };
    PhotoBulkProceedDialog.prototype.submit = function () {
        var data = {
            'criteria': this.options.criteria,
            'values': this.values
        };
        this._save("PATCH", null, data);
    };
    PhotoBulkProceedDialog.prototype.save_success = function (data) {
        //        $.each(data.results, function(photo) {
        //            window._photo_changed.trigger(photo)
        //        })
        window._reload_all.trigger(null);
        _super.prototype.save_success.call(this, data);
    };
    PhotoBulkProceedDialog.prototype.destroy = function () {
        _super.prototype.destroy.call(this);
    };
    return PhotoBulkProceedDialog;
}(BaseDialog));
var PhotoDeleteDialog = (function (_super) {
    __extends(PhotoDeleteDialog, _super);
    function PhotoDeleteDialog(options) {
        _super.call(this, options);
        this.type = "photos";
        this.type_name = "photo";
    }
    PhotoDeleteDialog.prototype.save_success = function (data) {
        window._photo_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PhotoDeleteDialog;
}(ObjectDeleteDialog));
var PhotoCriteriaWidget = (function (_super) {
    __extends(PhotoCriteriaWidget, _super);
    function PhotoCriteriaWidget(options) {
        _super.call(this, options);
        this.type = "photos";
        this.load_attributes = [
            { name: 'album', type: 'albums' },
            { name: 'category', type: 'categorys' },
            { name: 'place', type: 'places' },
            { name: 'person', type: 'persons' },
            { name: 'instance', type: 'photos' },
        ];
    }
    PhotoCriteriaWidget.prototype.set = function (input_criteria) {
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
        else if (criteria.album != null) {
            title = "album " + criteria.album;
        }
        else if (criteria.category != null) {
            title = "category " + criteria.category;
        }
        else if (criteria.place != null) {
            title = "place " + criteria.place;
        }
        else if (criteria.person != null) {
            title = "person " + criteria.person;
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
    return PhotoCriteriaWidget;
}(ObjectCriteriaWidget));
var PhotoListWidget = (function (_super) {
    __extends(PhotoListWidget, _super);
    function PhotoListWidget(options) {
        _super.call(this, options);
        this.type = "photos";
    }
    PhotoListWidget.prototype.add_selection = function (photo) {
        var selection = this.options.selection;
        if (selection.indexOf(photo.id) === -1) {
            selection.push(photo.id);
            push_state(true);
        }
    };
    PhotoListWidget.prototype.del_selection = function (photo) {
        var selection = this.options.selection;
        var index = selection.indexOf(photo.id);
        if (index !== -1) {
            selection.splice(index, 1);
            push_state(true);
        }
    };
    PhotoListWidget.prototype.get_selection = function () {
        return this.options.selection;
    };
    PhotoListWidget.prototype.is_photo_selected = function (photo) {
        var selection = this.options.selection;
        var index = selection.indexOf(photo.id);
        return index !== -1;
    };
    PhotoListWidget.prototype.to_object = function (streamable) {
        return new Photo(streamable);
    };
    PhotoListWidget.prototype.show = function (element) {
        var _this = this;
        if (this.options.selection == null) {
            this.options.selection = [];
        }
        _super.prototype.show.call(this, element);
        var options = {
            filter: "li",
            selected: function (event, ui) {
                _this.add_selection($(ui.selected).data('item'));
            },
            unselected: function (event, ui) {
                _this.del_selection($(ui.unselected).data('item'));
            }
        };
        $.spud.myselectable(options, this.ul);
        window._photo_changed.add_listener(this, function (photo) {
            var li = _this.create_li_for_obj(photo);
            _this.get_item(photo.id).replaceWith(li);
        });
        window._photo_deleted.add_listener(this, function (photo_id) {
            _this.get_item(photo_id).remove();
            _this.load_if_required();
        });
    };
    PhotoListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            obj: null,
            obj_id: null
        };
        var viewport;
        viewport = new PhotoDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PhotoListWidget.prototype.get_photo = function (obj) {
        return obj;
    };
    PhotoListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        var datetime = moment(obj.datetime[0]);
        datetime.zone(-obj.datetime[1]);
        var datetime_str = datetime.format("YYYY-MM-DD hh:mm");
        details.push($("<div/>").text(datetime_str));
        if (obj.place != null) {
            details.push($("<div/>").text(obj.place.title));
        }
        return details;
    };
    PhotoListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    PhotoListWidget.prototype.create_li = function (photo, title, details, description, a) {
        var li = _super.prototype.create_li.call(this, photo, title, details, description, a);
        li.data("item", photo);
        li.toggleClass("removed", photo.action === "D");
        li.toggleClass("regenerate", photo.action != null && photo.action !== "D");
        li.toggleClass("ui-selected", this.is_photo_selected(photo));
        return li;
    };
    PhotoListWidget.prototype.bulk_update = function () {
        var criteria = this.options.criteria;
        if (this.options.selection.length > 0) {
            criteria = $.extend({}, criteria);
            criteria.photos = this.options.selection;
        }
        var params = {
            criteria: criteria
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkUpdateDialog(params);
        dialog.show(div);
    };
    return PhotoListWidget;
}(ObjectListWidget));
var PhotoDetailInfobox = (function (_super) {
    __extends(PhotoDetailInfobox, _super);
    function PhotoDetailInfobox(options) {
        _super.call(this, options);
    }
    PhotoDetailInfobox.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["title", new TextOutputField("Title")],
                    ["description", new POutputField("Description")],
                    ["view", new POutputField("View")],
                    ["comment", new POutputField("Comment")],
                    ["name", new TextOutputField("File")],
                    ["albums", new LinkListOutputField("Albums", "albums")],
                    ["categorys", new LinkListOutputField("Categories", "categorys")],
                    ["place", new LinkOutputField("Place", "places")],
                    ["persons", new LinkListOutputField("People", "persons")],
                    ["datetime", new DateTimeOutputField("Date & time")],
                    ["photographer", new LinkOutputField("Photographer", "persons")],
                    ["rating", new TextOutputField("Rating")],
                    //                ["videos", new HtmlOutputField("Videos")],
                    //                ["related", new HtmlListOutputField("Related")],
                    ["action", new TextOutputField("Action")],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextOutputField("Camera make")],
                    ["camera_model", new TextOutputField("Camera model")],
                    ["flash_used", new TextOutputField("Flash")],
                    ["focal_length", new TextOutputField("Focal Length")],
                    ["exposure", new TextOutputField("Exposure")],
                    ["aperture", new TextOutputField("Aperture")],
                    ["iso_equiv", new TextOutputField("ISO")],
                    ["metering_mode", new TextOutputField("Metering mode")],
                ] },
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: false });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PhotoDetailInfobox.prototype.set = function (photo) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, photo);
        this.options.obj = photo;
        this.img.set(photo);
    };
    return PhotoDetailInfobox;
}(Infobox));
var PhotoListViewport = (function (_super) {
    __extends(PhotoListViewport, _super);
    function PhotoListViewport(options) {
        _super.call(this, options);
        this.type = "photos";
        this.type_name = "Photo";
    }
    PhotoListViewport.prototype.setup_menu = function (menu) {
        _super.prototype.setup_menu.call(this, menu);
        var mythis = this;
        menu.append($("<li/>")
            .text("Update")
            .on("click", function (ev) {
            void ev;
            var instance = mythis.ol;
            instance.bulk_update();
        }));
    };
    PhotoListViewport.prototype.get_streamable_options = function () {
        var options = _super.prototype.get_streamable_options.call(this);
        if (this.ol != null) {
            var instance = this.ol;
            options['object_list_options'] = {
                selection: instance.get_selection()
            };
        }
        return options;
    };
    PhotoListViewport.prototype.create_object_list_widget = function (options) {
        return new PhotoListWidget(options);
    };
    PhotoListViewport.prototype.create_object_criteria_widget = function (options) {
        return new PhotoCriteriaWidget(options);
    };
    PhotoListViewport.prototype.create_object_search_dialog = function (options) {
        return new PhotoSearchDialog(options);
    };
    return PhotoListViewport;
}(ObjectListViewport));
var PhotoDetailViewport = (function (_super) {
    __extends(PhotoDetailViewport, _super);
    function PhotoDetailViewport(options) {
        _super.call(this, options);
        this.type = "photos";
        this.type_name = "Photo";
    }
    PhotoDetailViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        _super.prototype.setup_menu.call(this, menu);
        this.orig = $("<li/>")
            .text("Original")
            .on("click", function (ev) {
            void ev;
            if (_this.options.obj.orig_url != null) {
                window.open(_this.options.obj.orig_url);
            }
        })
            .hide()
            .appendTo(menu);
    };
    PhotoDetailViewport.prototype.to_object = function (streamable) {
        return new Photo(streamable);
    };
    PhotoDetailViewport.prototype.loaded = function (obj) {
        this.orig.toggle(obj.orig_url != null);
        this.div
            .toggleClass("removed", obj.action === "D")
            .toggleClass("regenerate", obj.action != null && obj.action !== "D");
        _super.prototype.loaded.call(this, obj);
    };
    PhotoDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        var mythis = this;
        window._photo_changed.add_listener(this, function (obj) {
            if (obj.id === _this.options.obj_id) {
                mythis.set(obj);
            }
        });
        window._photo_deleted.add_listener(this, function (obj_id) {
            if (obj_id === _this.options.obj_id) {
                mythis.remove();
            }
        });
    };
    PhotoDetailViewport.prototype.get_photo_criteria = function () {
        return null;
    };
    PhotoDetailViewport.prototype.create_object_list_widget = function (options) {
        return new PhotoListWidget(options);
    };
    PhotoDetailViewport.prototype.create_object_detail_infobox = function (options) {
        return new PhotoDetailInfobox(options);
    };
    PhotoDetailViewport.prototype.create_object_list_viewport = function (options) {
        return new PhotoListViewport(options);
    };
    PhotoDetailViewport.prototype.create_object_change_dialog = function (options) {
        return new PhotoChangeDialog(options);
    };
    PhotoDetailViewport.prototype.create_object_delete_dialog = function (options) {
        return new PhotoDeleteDialog(options);
    };
    return PhotoDetailViewport;
}(ObjectDetailViewport));
