/// <reference path="globals.ts" />
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
///////////////////////////////////////
// signals
///////////////////////////////////////
window._listeners = {};
function remove_all_listeners(obj) {
    var key = "null";
    if (obj != null) {
        key = obj.get_uuid();
    }
    if (window._listeners[key] != null) {
        $.each(window._listeners[key], function (i, listener) {
            if (listener != null) {
                listener.remove_listener(obj);
            }
        });
    }
    delete window._listeners[key];
}
var Signal = (function () {
    function Signal() {
        this.on_no_listeners = null;
        this.listeners = {};
        this.objects = {};
    }
    Signal.prototype.add_listener = function (obj, listener) {
        var key = "null";
        if (obj != null) {
            key = obj.get_uuid();
        }
        if (this.listeners[key]) {
            this.remove_listener(key);
        }
        this.listeners[key] = listener;
        this.objects[key] = obj;
        if (window._listeners[key] == null) {
            window._listeners[key] = [];
        }
        window._listeners[key].push(this);
    };
    Signal.prototype.remove_listener = function (obj) {
        var key = "null";
        if (obj != null) {
            key = obj.get_uuid();
        }
        delete this.listeners[key];
        delete this.objects[key];
        if (window._listeners[key] == null) {
            var index = window._listeners[key].indexOf(this);
            if (index !== -1) {
                // Don't do this; is called from within loop in
                // remove_all_listeners
                // window._listeners[key].splice(index, 1)
                delete window._listeners[key];
            }
        }
        if (!this.is_any_listeners()) {
            if (this.on_no_listeners != null) {
                this.on_no_listeners();
            }
        }
    };
    Signal.prototype.is_any_listeners = function () {
        return !$.isEmptyObject(this.listeners);
    };
    Signal.prototype.trigger = function (arg) {
        var mythis = this;
        $.each(this.listeners, function (uuid, listener) {
            var obj = null;
            if (uuid !== "null") {
                obj = mythis.objects[uuid];
            }
            listener.call(obj, arg);
        });
    };
    return Signal;
}());
window._reload_all = new Signal();
window._perms_changed = new Signal();
window._session_changed = new Signal();
