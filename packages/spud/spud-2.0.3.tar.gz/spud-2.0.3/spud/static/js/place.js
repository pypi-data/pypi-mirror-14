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
window._place_created = new Signal();
window._place_changed = new Signal();
window._place_deleted = new Signal();
var PlaceStreamable = (function (_super) {
    __extends(PlaceStreamable, _super);
    function PlaceStreamable() {
        _super.apply(this, arguments);
    }
    return PlaceStreamable;
}(ObjectStreamable));
var Place = (function (_super) {
    __extends(Place, _super);
    function Place(streamable) {
        _super.call(this, streamable);
        this.address = parse_string(streamable.address);
        this.address2 = parse_string(streamable.address2);
        this.city = parse_string(streamable.city);
        this.state = parse_string(streamable.state);
        this.country = parse_string(streamable.country);
        this.postcode = parse_string(streamable.postcode);
        this.url = parse_string(streamable.url);
        this.urldesc = parse_string(streamable.urldesc);
        this.notes = parse_string(streamable.notes);
        if (streamable.ascendants != null) {
            this.ascendants = [];
            for (var i = 0; i < streamable.ascendants.length; i++) {
                this.ascendants.push(new Place(streamable.ascendants[i]));
            }
            if (streamable.ascendants.length > 0) {
                this.parent = this.ascendants[0];
            }
            else {
                this.parent = null;
            }
        }
    }
    Place.prototype.to_streamable = function () {
        var streamable = _super.prototype.to_streamable.call(this);
        streamable.address = this.address;
        streamable.address2 = this.address2;
        streamable.city = this.city;
        streamable.state = this.state;
        streamable.country = this.country;
        streamable.postcode = this.postcode;
        streamable.url = this.url;
        streamable.urldesc = this.urldesc;
        streamable.notes = this.notes;
        if (this.parent != null) {
            streamable.parent = this.parent.id;
        }
        else {
            streamable.parent = null;
        }
        return streamable;
    };
    return Place;
}(SpudObject));
var PlaceSearchDialog = (function (_super) {
    __extends(PlaceSearchDialog, _super);
    function PlaceSearchDialog(options) {
        _super.call(this, options);
    }
    PlaceSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Place", "places", false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search places";
        this.options.description = "Please search for an place.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PlaceSearchDialog;
}(ObjectSearchDialog));
var PlaceChangeDialog = (function (_super) {
    __extends(PlaceChangeDialog, _super);
    function PlaceChangeDialog(options) {
        _super.call(this, options);
        this.type = "places";
        this.type_name = "place";
    }
    PlaceChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["address", new TextInputField("Address", false)],
            ["address2", new TextInputField("Address(ctd)", false)],
            ["city", new TextInputField("City", false)],
            ["state", new TextInputField("State", false)],
            ["country", new TextInputField("Country", false)],
            ["postcode", new TextInputField("Postcode", false)],
            ["url", new TextInputField("URL", false)],
            ["urldesc", new TextInputField("URL desc", false)],
            ["notes", new PInputField("Notes", false)],
            ["parent", new AjaxSelectField("Parent", "places", false)],
        ];
        this.options.title = "Change place";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PlaceChangeDialog.prototype.save_success = function (data) {
        var place = new Place(data);
        if (this.obj.id != null) {
            window._place_changed.trigger(place);
        }
        else {
            window._place_created.trigger(place);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PlaceChangeDialog;
}(ObjectChangeDialog));
var PlaceDeleteDialog = (function (_super) {
    __extends(PlaceDeleteDialog, _super);
    function PlaceDeleteDialog(options) {
        _super.call(this, options);
        this.type = "places";
        this.type_name = "place";
    }
    PlaceDeleteDialog.prototype.save_success = function (data) {
        window._place_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PlaceDeleteDialog;
}(ObjectDeleteDialog));
var PlaceCriteriaWidget = (function (_super) {
    __extends(PlaceCriteriaWidget, _super);
    function PlaceCriteriaWidget(options) {
        _super.call(this, options);
        this.type = "places";
    }
    PlaceCriteriaWidget.prototype.set = function (input_criteria) {
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
    return PlaceCriteriaWidget;
}(ObjectCriteriaWidget));
var PlaceListWidget = (function (_super) {
    __extends(PlaceListWidget, _super);
    function PlaceListWidget(options) {
        _super.call(this, options);
        this.type = "places";
    }
    PlaceListWidget.prototype.to_object = function (streamable) {
        return new Place(streamable);
    };
    PlaceListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._place_changed.add_listener(this, function (place) {
            var li = _this.create_li_for_obj(place);
            _this.get_item(place.id).replaceWith(li);
        });
        window._place_deleted.add_listener(this, function (place_id) {
            _this.get_item(place_id).remove();
            _this.load_if_required();
        });
    };
    PlaceListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            obj: null,
            obj_id: null
        };
        var viewport;
        viewport = new PlaceDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PlaceListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        return details;
    };
    PlaceListWidget.prototype.get_description = function (obj) {
        return obj.city;
    };
    return PlaceListWidget;
}(ObjectListWidget));
var PlaceDetailInfobox = (function (_super) {
    __extends(PlaceDetailInfobox, _super);
    function PlaceDetailInfobox(options) {
        _super.call(this, options);
    }
    PlaceDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["address", new TextOutputField("Address")],
            ["address2", new TextOutputField("Address(ctd)")],
            ["city", new TextOutputField("City")],
            ["state", new TextOutputField("State")],
            ["postcode", new TextOutputField("Postcode")],
            ["country", new TextOutputField("Country")],
            // FIXME
            // ["url", new HtmlOutputField("URL")],
            ["home_of", new LinkListOutputField("Home of", "places")],
            ["work_of", new LinkListOutputField("Work of", "places")],
            ["notes", new POutputField("notes")],
            ["ascendants", new LinkListOutputField("Ascendants", "places")],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PlaceDetailInfobox.prototype.set = function (place) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, place);
        this.options.obj = place;
        this.img.set(place.cover_photo);
    };
    return PlaceDetailInfobox;
}(Infobox));
var PlaceListViewport = (function (_super) {
    __extends(PlaceListViewport, _super);
    function PlaceListViewport(options) {
        _super.call(this, options);
        this.type = "places";
        this.type_name = "Place";
    }
    PlaceListViewport.prototype.to_object = function (streamable) {
        return new Place(streamable);
    };
    PlaceListViewport.prototype.create_object_list_widget = function (options) {
        return new PlaceListWidget(options);
    };
    PlaceListViewport.prototype.create_object_criteria_widget = function (options) {
        return new PlaceCriteriaWidget(options);
    };
    PlaceListViewport.prototype.create_object_search_dialog = function (options) {
        return new PlaceSearchDialog(options);
    };
    return PlaceListViewport;
}(ObjectListViewport));
var PlaceDetailViewport = (function (_super) {
    __extends(PlaceDetailViewport, _super);
    function PlaceDetailViewport(options) {
        _super.call(this, options);
        this.type = "places";
        this.type_name = "Place";
    }
    PlaceDetailViewport.prototype.to_object = function (streamable) {
        return new Place(streamable);
    };
    PlaceDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        var mythis = this;
        window._place_changed.add_listener(this, function (obj) {
            if (obj.id === _this.options.obj_id) {
                mythis.set(obj);
            }
        });
        window._place_deleted.add_listener(this, function (obj_id) {
            if (obj_id === _this.options.obj_id) {
                mythis.remove();
            }
        });
    };
    PlaceDetailViewport.prototype.get_photo_criteria = function () {
        return {
            'place': this.options.obj_id,
            'place_descendants': true
        };
    };
    PlaceDetailViewport.prototype.create_object_list_widget = function (options) {
        return new PlaceListWidget(options);
    };
    PlaceDetailViewport.prototype.create_object_detail_infobox = function (options) {
        return new PlaceDetailInfobox(options);
    };
    PlaceDetailViewport.prototype.create_object_list_viewport = function (options) {
        return new PlaceListViewport(options);
    };
    PlaceDetailViewport.prototype.create_object_change_dialog = function (options) {
        return new PlaceChangeDialog(options);
    };
    PlaceDetailViewport.prototype.create_object_delete_dialog = function (options) {
        return new PlaceDeleteDialog(options);
    };
    return PlaceDetailViewport;
}(ObjectDetailViewport));
