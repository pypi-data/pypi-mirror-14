/// <reference path="session.ts" />
/// <reference path="album.ts" />
/// <reference path="category.ts" />
/// <reference path="place.ts" />
/// <reference path="person.ts" />
/// <reference path="photo.ts" />
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
var _viewport_class_dict = {
    "album_list": AlbumListViewport,
    "album_detail": AlbumDetailViewport,
    "category_list": CategoryListViewport,
    "category_detail": CategoryDetailViewport,
    "place_list": PlaceListViewport,
    "place_detail": PlaceDetailViewport,
    "person_list": PersonListViewport,
    "person_detail": PersonDetailViewport,
    "photo_list": PhotoListViewport,
    "photo_detail": PhotoDetailViewport
};
function get_state() {
    var results = [];
    $.each($(".viewport"), function (i, el) {
        var viewport = $(el).data('widget');
        var class_name;
        for (var name_1 in _viewport_class_dict) {
            var view_port_class = _viewport_class_dict[name_1];
            if (viewport.constructor == view_port_class) {
                class_name = name_1;
                break;
            }
        }
        if (class_name) {
            var streamable = viewport.get_streamable_options();
            results[i] = {
                options: streamable,
                class_name: class_name
            };
        }
    });
    return results;
}
function put_state(state) {
    window._dont_push = true;
    $("#content").empty();
    for (var _i = 0, state_1 = state; _i < state_1.length; _i++) {
        var viewport_state = state_1[_i];
        var name_2 = viewport_state.class_name;
        var options = viewport_state.options;
        var viewport_class = _viewport_class_dict[name_2];
        var viewport = new viewport_class(options);
        add_viewport(viewport);
    }
    window._dont_push = false;
}
function _get_page() {
    var title = "SPUD";
    var url = root_url();
    var active_viewport = $(".viewport:not(.disabled)").data("widget");
    if (active_viewport != null) {
        title = active_viewport.get_title();
        url = active_viewport.get_url();
    }
    return { title: title, url: url };
}
function push_state(do_replace) {
    if (window._dont_push) {
        return;
    }
    var state = get_state();
    var page = _get_page();
    var title = page.title;
    var url = page.url;
    if (window._do_replace || do_replace) {
        console.log("replace state", JSON.stringify(state), title, url);
        history.replaceState(state, title, url);
    }
    else {
        console.log("push state", JSON.stringify(state), title, url);
        history.pushState(state, title, url);
    }
    $("head title").text(title);
}
window.onpopstate = function (ev) {
    console.log("pop state", JSON.stringify(ev.state));
    if (ev.state != null) {
        put_state(ev.state);
    }
    else {
        put_state([]);
    }
    var page = _get_page();
    var title = page.title;
    $("head title").text(title);
};
