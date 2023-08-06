/// <reference path="globals.ts" />
/// <reference path="generic.ts" />
/// <reference path="DefinitelyTyped/moment.d.ts" />
/// <reference path="DefinitelyTyped/moment-timezone.d.ts" />
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
// define input_field
var InputField = (function () {
    function InputField(title, required) {
        this.title = title;
        this.required = Boolean(required);
    }
    InputField.prototype.to_html = function (id) {
        var html = this.create(id);
        var th = $("<th/>");
        $("<label/>")
            .attr("for", "id_" + id)
            .text(this.title + ":")
            .appendTo(th)
            .toggleClass("required", this.required.toString());
        this.errors = $("<div></div>");
        var td = $("<td/>")
            .append(html)
            .append(this.errors);
        this.tr = $("<tr/>")
            .append(th)
            .append(td);
        return this.tr;
    };
    InputField.prototype.get = function () {
        var value = this.input.val();
        if (value) {
            value = value.trim();
        }
        else {
            value = null;
        }
        return value;
    };
    InputField.prototype.validate = function () {
        var value = this.input.val();
        if (this.required && !value) {
            return "This value is required";
        }
        return null;
    };
    InputField.prototype.set_error = function (error) {
        this.tr.toggleClass("errors", Boolean(error));
        this.errors.toggleClass("errornote", Boolean(error));
        if (this.input) {
            this.input.toggleClass("errors", Boolean(error));
            this.input.find("input").toggleClass("errors", Boolean(error));
        }
        if (error) {
            this.errors.text(error);
        }
        else {
            this.errors.text("");
        }
    };
    InputField.prototype.clear_error = function () {
        this.set_error(null);
    };
    InputField.prototype.destroy = function () {
        this.tr.remove();
    };
    InputField.prototype.enable = function () {
        this.input.attr('disabled', null);
    };
    InputField.prototype.disable = function () {
        this.input.attr('disabled', 'true');
    };
    return InputField;
}());
// define text_input_field
var TextInputField = (function (_super) {
    __extends(TextInputField, _super);
    function TextInputField(title, required) {
        _super.call(this, title, required);
    }
    TextInputField.prototype.create = function (id) {
        this.input = $('<input />')
            .attr('type', "text")
            .attr('name', id)
            .attr('id', "id_" + id);
        return this.input;
    };
    TextInputField.prototype.set = function (value) {
        this.input.val(value);
    };
    return TextInputField;
}(InputField));
// define datetime_input_field
var DateTimeInputField = (function (_super) {
    __extends(DateTimeInputField, _super);
    function DateTimeInputField(title, required) {
        _super.call(this, title, required);
    }
    DateTimeInputField.prototype.create = function (id) {
        this.date = $('<input />')
            .attr('id', "id_" + id + "_date")
            .attr('placeholder', 'YYYY-MM-DD')
            .datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd"
        });
        this.time = $('<input />')
            .attr('type', "text")
            .attr('placeholder', 'HH:MM:SS')
            .attr('id', "id_" + id + "_time");
        this.timezone = $('<input />')
            .attr('type', "text")
            .attr('placeholder', 'timezone')
            .attr('id', "id_" + id + "_timezonetime");
        return $("<span></span>")
            .append(this.date)
            .append(this.time)
            .append(this.timezone);
    };
    DateTimeInputField.prototype.set = function (value) {
        if (value != null) {
            var datetime = moment(value[0]);
            var utc_offset = value[1];
            datetime = datetime.zone(-utc_offset);
            this.date.datepicker("setDate", datetime.format("YYYY-MM-dd"));
            this.date.val(datetime.format("YYYY-MM-DD"));
            this.time.val(datetime.format("HH:mm:ss"));
            var hours = Math.floor(utc_offset / 60);
            var minutes = utc_offset - (hours * 60);
            var str_hours = hours.toString();
            var str_minutes = minutes.toString();
            if (hours < 10) {
                str_hours = "0" + str_hours;
            }
            if (minutes < 10) {
                str_minutes = "0" + str_minutes;
            }
            this.timezone.val(hours + ":" + minutes);
        }
        else {
            this.date.val("");
            this.time.val("");
            this.timezone.val("");
        }
    };
    DateTimeInputField.prototype.validate = function () {
        var date = this.date.val().trim();
        var time = this.time.val().trim();
        var timezone = this.timezone.val().trim();
        var a;
        if (date !== "") {
            if (!/^\d\d\d\d-\d\d-\d\d$/.test(date)) {
                return "date format not yyyy-mm-dd";
            }
            a = date.split("-");
            if (Number(a[1]) < 1 || Number(a[1]) > 12) {
                return "Month must be between 1 and 12";
            }
            if (Number(a[2]) < 1 || Number(a[2]) > 31) {
                return "date must be between 1 and 31";
            }
            if (a[3] != null) {
                return "Too many components in date";
            }
        }
        if (time !== "") {
            if (!/^\d\d:\d\d+(:\d\d+)?$/.test(time)) {
                return "date format not hh:mm[:ss]";
            }
            if (!/^\d\d:\d\d+(:\d\d+)?$/.test(time)) {
                return "time format not hh:mm[:ss]";
            }
            if (date === "") {
                return "date must be given if time is given";
            }
            a = time.split(":");
            if (Number(a[0]) < 0 || Number(a[0]) > 23) {
                return "Hour must be between 0 and 23";
            }
            if (Number(a[1]) < 0 || Number(a[1]) > 59) {
                return "Minutes must be between 0 and 59";
            }
            if (Number(a[2]) < 0 || Number(a[2]) > 59) {
                return "Seconds must be between 0 and 59";
            }
            if (a[3] != null) {
                return "Too many components in time";
            }
        }
        if (timezone !== "") {
            a = timezone.split(":");
            if (a.length > 1) {
                if (Number(a[0]) < -12 || Number(a[0]) > 12) {
                    return "Hour must be between -12 and 12";
                }
                if (Number(a[1]) < 0 || Number(a[1]) > 59) {
                    return "Minutes must be between 0 and 59";
                }
                if (a[2] != null) {
                    return "Too many components in timezone";
                }
                if (date === "") {
                    return "Specifying timezone without date wrong";
                }
            }
            else {
                if (moment.tz.zone(timezone) == null) {
                    return "Unknown timezone";
                }
            }
        }
        return null;
    };
    DateTimeInputField.prototype.get = function () {
        var date = this.date.val().trim();
        var time = this.time.val().trim();
        var timezone = this.timezone.val().trim();
        if (date === "") {
            return null;
        }
        var result = date;
        if (time !== "") {
            result = result + " " + time;
        }
        var datetime;
        var utc_offset;
        if (timezone !== "") {
            var a = timezone.split(":");
            if (a.length > 1) {
                utc_offset = Number(a[0]) * 60 + Number(a[1]);
                datetime = moment.tz(result, "YYYY-MM-DD HH:mm:ss", "UTC");
                datetime.subtract(utc_offset, 'minutes');
            }
            else {
                datetime = moment.tz(result, "YYYY-MM-DD HH:mm:ss", timezone);
                utc_offset = -datetime.zone();
                datetime.utc();
            }
        }
        else {
            datetime = moment(result, "YYYY-MM-DD HH:mm:ss");
            utc_offset = -datetime.zone();
            datetime.utc();
        }
        console.log(datetime, utc_offset);
        return [datetime, utc_offset];
    };
    DateTimeInputField.prototype.enable = function () {
        this.date.attr('disabled', null);
        this.time.attr('disabled', null);
        this.timezone.attr('disabled', null);
    };
    DateTimeInputField.prototype.disable = function () {
        this.date.attr('disabled', "true");
        this.time.attr('disabled', "true");
        this.timezone.attr('disabled', "true");
    };
    return DateTimeInputField;
}(InputField));
// define password_input_field
var PasswordInputField = (function (_super) {
    __extends(PasswordInputField, _super);
    function PasswordInputField(title, required) {
        _super.call(this, title, required);
    }
    PasswordInputField.prototype.create = function (id) {
        this.input = $('<input />')
            .attr('type', "password")
            .attr('name', id)
            .attr('id', "id_" + id);
        return this.input;
    };
    return PasswordInputField;
}(TextInputField));
// define date_input_field
var DateInputField = (function (_super) {
    __extends(DateInputField, _super);
    function DateInputField(title, required) {
        _super.call(this, title, required);
    }
    DateInputField.prototype.create = function (id) {
        this.input = $('<input />')
            .attr('id', "id_" + id)
            .datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd"
        });
        return this.input;
    };
    DateInputField.prototype.validate = function () {
        var date = this.get();
        if (date != null) {
            if (!/^\d\d\d\d-\d\d-\d\d$/.test(date)) {
                return "date format not yyyy-mm-dd";
            }
            var a = date.split("-");
            if (Number(a[1]) < 1 || Number(a[1]) > 12) {
                return "Month must be between 1 and 12";
            }
            if (Number(a[2]) < 1 || Number(a[2]) > 31) {
                return "date must be between 1 and 31";
            }
        }
        return null;
    };
    return DateInputField;
}(TextInputField));
// define p_input_field
var PInputField = (function (_super) {
    __extends(PInputField, _super);
    function PInputField(title, required) {
        _super.call(this, title, required);
    }
    PInputField.prototype.create = function (id) {
        this.input = $('<textarea />')
            .attr('rows', 10)
            .attr('cols', 40)
            .attr('name', id)
            .attr('id', "id_" + id);
        return this.input;
    };
    return PInputField;
}(TextInputField));
// define integer_input_field
var IntegerInputField = (function (_super) {
    __extends(IntegerInputField, _super);
    function IntegerInputField(title, required) {
        _super.call(this, title, required);
    }
    IntegerInputField.prototype.validate = function () {
        var value = this.get();
        var intRegex = /^\d+$/;
        if (value && !intRegex.test(value)) {
            return "Value must be integer";
        }
        return _super.prototype.validate.call(this);
    };
    return IntegerInputField;
}(TextInputField));
// define select_input_field
var SelectInputField = (function (_super) {
    __extends(SelectInputField, _super);
    function SelectInputField(title, options, required) {
        _super.call(this, title, required);
        this.options_list = options;
    }
    SelectInputField.prototype.create = function (id) {
        this.input = $('<select />')
            .attr('name', id)
            .attr('id', "id_" + id);
        this.set_options(this.options_list);
        return this.input;
    };
    SelectInputField.prototype.set_options = function (options) {
        this.input.empty();
        this.options = {};
        var null_option = "-----";
        for (var _i = 0, options_1 = options; _i < options_1.length; _i++) {
            var option = options_1[_i];
            var id = option[0];
            var value = option[1];
            if (typeof value != 'undefined') {
                this.options[id] = $('<option />')
                    .attr('value', id)
                    .text(value)
                    .appendTo(this.input);
            }
            else {
                null_option = value;
            }
        }
        if (!this.required) {
            this.options[""] = $('<option />')
                .attr('value', "")
                .text(null_option)
                .prependTo(this.input);
        }
        this.options_list = options;
    };
    SelectInputField.prototype.set = function (value) {
        this.input.val(value);
    };
    SelectInputField.prototype.validate = function () {
        var value = this.get();
        if (value == null) {
            value = "";
        }
        if (this.options[value] == null) {
            return value + " is not valid option";
        }
        return null;
    };
    return SelectInputField;
}(InputField));
// define boolean_input_field
var booleanInputField = (function (_super) {
    __extends(booleanInputField, _super);
    function booleanInputField(title, required) {
        _super.call(this, title, required);
    }
    booleanInputField.prototype.create = function (id) {
        this.input = $('<input />')
            .attr('type', 'checkbox')
            .attr('name', id)
            .attr('id', "id_" + id);
        return this.input;
    };
    booleanInputField.prototype.set = function (value) {
        if (value) {
            this.input.attr('checked', 'checked');
        }
        else {
            this.input.removeAttr('checked');
        }
    };
    booleanInputField.prototype.get = function () {
        var value = this.input.is(":checked");
        return value;
    };
    return booleanInputField;
}(InputField));
// define ajax_select_field
var AjaxSelectField = (function (_super) {
    __extends(AjaxSelectField, _super);
    function AjaxSelectField(title, type, required) {
        _super.call(this, title, required);
        this.type = type;
    }
    AjaxSelectField.prototype.create = function (id) {
        this.input = $("<span/>")
            .attr("name", id)
            .attr("id", "id_" + id);
        $.spud.ajaxautocomplete({ type: this.type }, this.input);
        return this.input;
    };
    AjaxSelectField.prototype.destroy = function () {
        this.input.ajaxautocomplete("destroy");
    };
    AjaxSelectField.prototype.set = function (value) {
        this.input.ajaxautocomplete("set", value, null);
    };
    AjaxSelectField.prototype.get = function () {
        return this.input.ajaxautocomplete("get");
    };
    AjaxSelectField.prototype.enable = function () {
        this.input.ajaxautocomplete("enable");
    };
    AjaxSelectField.prototype.disable = function () {
        this.input.ajaxautocomplete("disable");
    };
    return AjaxSelectField;
}(InputField));
// define ajax_select_multiple_field
var AjaxSelectMultipleField = (function (_super) {
    __extends(AjaxSelectMultipleField, _super);
    function AjaxSelectMultipleField(title, type, required) {
        _super.call(this, title, required);
        this.type = type;
    }
    AjaxSelectMultipleField.prototype.create = function (id) {
        this.input = $("<span/>")
            .attr("name", id)
            .attr("id", "id_" + id);
        $.spud.ajaxautocompletemultiple({ type: this.type }, this.input);
        return this.input;
    };
    AjaxSelectMultipleField.prototype.destroy = function () {
        this.input.ajaxautocompletemultiple("destroy");
    };
    AjaxSelectMultipleField.prototype.set = function (value) {
        this.input.ajaxautocompletemultiple("set", value, null);
    };
    AjaxSelectMultipleField.prototype.get = function () {
        return this.input.ajaxautocompletemultiple("get");
    };
    AjaxSelectMultipleField.prototype.enable = function () {
        this.input.ajaxautocompletemultiple("enable");
    };
    AjaxSelectMultipleField.prototype.disable = function () {
        this.input.ajaxautocompletemultiple("disable");
    };
    return AjaxSelectMultipleField;
}(InputField));
// define ajax_select_sorted_field
var AjaxSelectSortedField = (function (_super) {
    __extends(AjaxSelectSortedField, _super);
    function AjaxSelectSortedField(title, type, required) {
        _super.call(this, title, required);
        this.type = type;
    }
    AjaxSelectSortedField.prototype.create = function (id) {
        this.input = $("<span/>")
            .attr("name", id)
            .attr("id", "id_" + id);
        $.spud.ajaxautocompletesorted({ type: this.type }, this.input);
        return this.input;
    };
    AjaxSelectSortedField.prototype.destroy = function () {
        this.input.ajaxautocompletesorted("destroy");
    };
    AjaxSelectSortedField.prototype.set = function (value) {
        this.input.ajaxautocompletesorted("set", value, null);
    };
    AjaxSelectSortedField.prototype.get = function () {
        return this.input.ajaxautocompletesorted("get");
    };
    AjaxSelectSortedField.prototype.enable = function () {
        this.input.ajaxautocompletesorted("enable");
    };
    AjaxSelectSortedField.prototype.disable = function () {
        this.input.ajaxautocompletesorted("disable");
    };
    return AjaxSelectSortedField;
}(InputField));
// define photo_select_field
var PhotoSelectField = (function (_super) {
    __extends(PhotoSelectField, _super);
    function PhotoSelectField(title, required) {
        _super.call(this, title, required);
    }
    PhotoSelectField.prototype.create = function (id) {
        this.input = $("<span/>")
            .attr("name", id)
            .attr("id", "id_" + id);
        $.spud.photo_select({}, this.input);
        return this.input;
    };
    PhotoSelectField.prototype.destroy = function () {
        this.input.photo_select("destroy");
    };
    PhotoSelectField.prototype.set = function (value) {
        if (value != null) {
            this.input.photo_select("set", value, null);
        }
        else {
            this.input.photo_select("set", null, null);
        }
    };
    PhotoSelectField.prototype.get = function () {
        return this.input.photo_select("get");
    };
    PhotoSelectField.prototype.validate = function () {
        var value = this.input.photo_select("get");
        if (this.required && !value) {
            return "This value is required";
        }
        return null;
    };
    PhotoSelectField.prototype.enable = function () {
        this.input.photo_select("enable");
    };
    PhotoSelectField.prototype.disable = function () {
        this.input.photo_select("disable");
    };
    return PhotoSelectField;
}(InputField));
var FormDialog = (function (_super) {
    __extends(FormDialog, _super);
    function FormDialog(options) {
        _super.call(this, options);
    }
    FormDialog.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.f = $("<form method='get' />")
            .appendTo(this.element);
        this.fields = {};
        if (this.options.pages) {
            this.page = {};
            this.tabs = $("<div/>")
                .addClass("fields")
                .appendTo(this.f);
            var ul = $("<ul></ul>").appendTo(this.tabs);
            for (var i = 0; i < this.options.pages.length; i++) {
                var page = this.options.pages[i];
                var name_1 = page.name;
                var title = page.title;
                $("<li/>")
                    .append($("<a/>")
                    .attr("href", '#' + name_1)
                    .text(title))
                    .appendTo(ul);
                this.page[name_1] = $("<table/>")
                    .attr('id', name_1)
                    .appendTo(this.tabs);
                this.create_fields(name_1, page.fields);
            }
            this.tabs.tabs();
        }
        else {
            this.table = $("<table/>")
                .addClass("fields")
                .appendTo(this.f);
            this.create_fields(null, this.options.fields);
        }
        if (this.options.obj != null) {
            this.set(this.options.obj);
        }
    };
    FormDialog.prototype.check_submit = function () {
        var allok = true;
        for (var id in this.fields) {
            var field = this.fields[id];
            var error = field.validate();
            if (error) {
                field.set_error(error);
                allok = false;
            }
            else {
                field.clear_error();
            }
        }
        if (allok) {
            this.disable();
            this.submit();
        }
    };
    FormDialog.prototype.create_fields = function (page, fields) {
        if (fields != null) {
            this.add_fields(page, fields);
        }
    };
    FormDialog.prototype.submit = function () {
        var values = {};
        for (var id in this.fields) {
            var field = this.fields[id];
            values[id] = this.get_value(id);
        }
        this.submit_values(values);
    };
    FormDialog.prototype.disable = function () {
        for (var id in this.fields) {
            var field = this.fields[id];
            field.disable();
        }
        _super.prototype.disable.call(this);
    };
    FormDialog.prototype.enable = function () {
        for (var id in this.fields) {
            var field = this.fields[id];
            field.enable();
        }
        _super.prototype.enable.call(this);
    };
    FormDialog.prototype.submit_values = function (values) {
    };
    FormDialog.prototype.set = function (values) {
        for (var id in this.fields) {
            this.set_value(id, values[id]);
        }
    };
    FormDialog.prototype.add_field = function (page, id, field) {
        this.remove_field(id);
        var html = field.to_html(id);
        if (page == null) {
            this.table.append(html);
        }
        else {
            this.page[page].append(html);
        }
        this.fields[id] = field;
    };
    FormDialog.prototype.add_fields = function (page, fields) {
        for (var _i = 0, fields_1 = fields; _i < fields_1.length; _i++) {
            var item = fields_1[_i];
            var id = item[0];
            var field = item[1];
            this.add_field(page, id, field);
        }
    };
    FormDialog.prototype.remove_field = function (id) {
        var field = this.fields[id];
        if (field != null) {
            field.destroy();
            delete this.fields[id];
        }
    };
    FormDialog.prototype.remove_all_fields = function () {
        for (var id in this.fields) {
            this.remove_field(id);
        }
    };
    FormDialog.prototype.set_value = function (id, value) {
        var field = this.fields[id];
        field.set(value);
    };
    FormDialog.prototype.set_error = function (id, message) {
        var field = this.fields[id];
        field.set_error(message);
    };
    FormDialog.prototype.get_value = function (id) {
        var field = this.fields[id];
        return field.get();
    };
    FormDialog.prototype.destroy = function () {
        for (var id in this.fields) {
            var field = this.fields[id];
            field.destroy();
        }
        _super.prototype.destroy.call(this);
    };
    FormDialog.prototype.save_error = function (message, data) {
        if (data != null) {
            for (var id in data) {
                var error = data[id];
                if (this.fields[id] != null) {
                    this.fields[id].set_error(error);
                }
            }
        }
        _super.prototype.save_error.call(this, message, data);
    };
    return FormDialog;
}(BaseDialog));
