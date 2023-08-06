/// <reference path="dialog.ts" />
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
// sessions
///////////////////////////////////////
var Session = (function (_super) {
    __extends(Session, _super);
    function Session() {
        _super.apply(this, arguments);
    }
    return Session;
}(Streamable));
var LoginDialog = (function (_super) {
    __extends(LoginDialog, _super);
    function LoginDialog() {
        _super.apply(this, arguments);
    }
    LoginDialog.prototype.show = function (element) {
        this.options.fields = [
            ["username", new TextInputField("Username", true)],
            ["password", new PasswordInputField("Password", true)],
        ];
        this.options.title = "Login";
        this.options.description = "Please login by typing in your username and password below.";
        this.options.button = "Login";
        this.type = "session";
        _super.prototype.show.call(this, element);
    };
    LoginDialog.prototype.submit_values = function (values) {
        this.save_action("POST", "login", values);
    };
    LoginDialog.prototype.save_success = function (session) {
        window._session_changed.trigger(session);
        _super.prototype.save_success.call(this, session);
    };
    return LoginDialog;
}(FormDialog));
var LogoutDialog = (function (_super) {
    __extends(LogoutDialog, _super);
    function LogoutDialog() {
        _super.apply(this, arguments);
    }
    LogoutDialog.prototype.show = function (element) {
        this.options.title = "Logout";
        this.options.description = "Are you sure you want to logout?";
        this.options.button = "Logout";
        this.type = "session";
        _super.prototype.show.call(this, element);
    };
    LogoutDialog.prototype.submit_values = function (values) {
        this.save_action("POST", "logout", values);
    };
    LogoutDialog.prototype.save_success = function (session) {
        window._session_changed.trigger(session);
        _super.prototype.save_success.call(this, session);
    };
    return LogoutDialog;
}(FormDialog));
function add_viewport(viewport) {
    var cm = $("#content");
    var div = $("<div/>").appendTo(cm);
    viewport.show(div);
    return div;
}
function setup_user_tools(session) {
    var ut = $("#user-tools");
    ut.empty();
    ut.append("Welcome, ");
    if (session.user) {
        var user = session.user;
        $("<strong></strong")
            .text(user.first_name + " " + user.last_name)
            .appendTo(ut);
        ut.append(" / ");
        $("<a/>")
            .text("logout")
            .on("click", function (ev) {
            var div = $("<div/>");
            var dialog = new LogoutDialog({});
            dialog.show(div);
        })
            .appendTo(ut);
    }
    else {
        $("<strong></strong")
            .text("guest")
            .appendTo(ut);
        ut.append(" / ");
        $("<a/>")
            .text("login")
            .on("click", function (ev) {
            void ev;
            var div = $("<div/>");
            var dialog = new LoginDialog({});
            dialog.show(div);
        })
            .appendTo(ut);
    }
}
function setup_menu(session) {
    var menu = $("<ul/>")
        .addClass("menubar")
        .empty();
    $('<li/>')
        .text("Albums")
        .on('click', function (ev) {
        var criteria = { root_only: true };
        var viewport = new AlbumListViewport({ criteria: criteria });
        add_viewport(viewport);
        return false;
    })
        .appendTo(menu);
    $('<li/>')
        .text("Categories")
        .on('click', function (ev) {
        var criteria = { root_only: true };
        var viewport = new CategoryListViewport({ criteria: criteria });
        add_viewport(viewport);
        return false;
    })
        .appendTo(menu);
    $('<li/>')
        .text("Places")
        .on('click', function (ev) {
        var criteria = { root_only: true };
        var viewport = new PlaceListViewport({ criteria: criteria });
        add_viewport(viewport);
        return false;
    })
        .appendTo(menu);
    $('<li/>')
        .text("People")
        .on('click', function (ev) {
        var criteria = {};
        var viewport = new PersonListViewport({ criteria: criteria });
        add_viewport(viewport);
        return false;
    })
        .appendTo(menu);
    $('<li/>')
        .text("Photos")
        .on('click', function (ev) {
        var criteria = {};
        var viewport = new PhotoListViewport({ criteria: criteria });
        add_viewport(viewport);
        return false;
    })
        .appendTo(menu);
    $('<li/>')
        .text("Reload")
        .on('click', function (ev) {
        window._reload_all.trigger(null);
        return false;
    })
        .appendTo(menu);
    menu.menu();
    $("#menu")
        .empty()
        .append(menu);
}
window._session_changed.add_listener(null, function (session) {
    window._perms = session.perms;
    window._perms_changed.trigger(session.perms);
    setup_user_tools(session);
    setup_menu(session);
});
function setup_page(session) {
    window._session_changed.trigger(session);
    $("body").attr("onload", null);
}
