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
window._person_created = new Signal();
window._person_changed = new Signal();
window._person_deleted = new Signal();
var PersonStreamable = (function (_super) {
    __extends(PersonStreamable, _super);
    function PersonStreamable() {
        _super.apply(this, arguments);
    }
    return PersonStreamable;
}(ObjectStreamable));
var Person = (function (_super) {
    __extends(Person, _super);
    function Person(streamable) {
        _super.call(this, streamable);
        this.first_name = parse_string(streamable.first_name);
        this.middle_name = parse_string(streamable.middle_name);
        this.last_name = parse_string(streamable.last_name);
        this.called = parse_string(streamable.called);
        this.sex = parse_string(streamable.sex);
        this.email = parse_string(streamable.email);
        this.dob = parse_string(streamable.dob);
        this.dod = parse_string(streamable.dod);
        this.notes = parse_string(streamable.notes);
        if (streamable.work != null) {
            this.work = new Place(streamable.work);
        }
        else {
            this.work = null;
        }
        if (streamable.home != null) {
            this.home = new Place(streamable.home);
        }
        else {
            this.home = null;
        }
        if (streamable.mother != null) {
            this.mother = new Person(streamable.mother);
        }
        else {
            this.mother = null;
        }
        if (streamable.father != null) {
            this.father = new Person(streamable.father);
        }
        else {
            this.father = null;
        }
        if (streamable.spouse != null) {
            this.spouse = new Person(streamable.spouse);
        }
        else {
            this.spouse = null;
        }
        if (streamable.grandparents != null) {
            this.grandparents = [];
            for (var i = 0; i < streamable.grandparents.length; i++) {
                this.grandparents.push(new Person(streamable.grandparents[i]));
            }
        }
        if (streamable.uncles_aunts != null) {
            this.uncles_aunts = [];
            for (var i = 0; i < streamable.uncles_aunts.length; i++) {
                this.uncles_aunts.push(new Person(streamable.uncles_aunts[i]));
            }
        }
        if (streamable.parents != null) {
            this.parents = [];
            for (var i = 0; i < streamable.parents.length; i++) {
                this.parents.push(new Person(streamable.parents[i]));
            }
        }
        if (streamable.siblings != null) {
            this.siblings = [];
            for (var i = 0; i < streamable.siblings.length; i++) {
                this.siblings.push(new Person(streamable.siblings[i]));
            }
        }
        if (streamable.cousins != null) {
            this.cousins = [];
            for (var i = 0; i < streamable.cousins.length; i++) {
                this.cousins.push(new Person(streamable.cousins[i]));
            }
        }
        if (streamable.children != null) {
            this.children = [];
            for (var i = 0; i < streamable.children.length; i++) {
                this.children.push(new Person(streamable.children[i]));
            }
        }
        if (streamable.nephews_nieces != null) {
            this.nephews_nieces = [];
            for (var i = 0; i < streamable.nephews_nieces.length; i++) {
                this.nephews_nieces.push(new Person(streamable.nephews_nieces[i]));
            }
        }
        if (streamable.grandchildren != null) {
            this.grandchildren = [];
            for (var i = 0; i < streamable.grandchildren.length; i++) {
                this.grandchildren.push(new Person(streamable.grandchildren[i]));
            }
        }
    }
    Person.prototype.to_streamable = function () {
        var streamable = _super.prototype.to_streamable.call(this);
        streamable.first_name = this.first_name;
        streamable.middle_name = this.middle_name;
        streamable.last_name = this.last_name;
        streamable.called = this.called;
        streamable.sex = this.sex;
        streamable.email = this.email;
        streamable.dob = this.dob;
        streamable.dod = this.dod;
        streamable.notes = this.notes;
        if (this.work != null) {
            streamable.work_pk = this.work.id;
        }
        else {
            streamable.work_pk = null;
        }
        if (this.home != null) {
            streamable.home_pk = this.home.id;
        }
        else {
            streamable.home_pk = null;
        }
        if (this.mother != null) {
            streamable.mother_pk = this.mother.id;
        }
        else {
            streamable.mother_pk = null;
        }
        if (this.father != null) {
            streamable.father_pk = this.father.id;
        }
        else {
            streamable.father_pk = null;
        }
        if (this.spouse != null) {
            streamable.spouse_pk = this.spouse.id;
        }
        else {
            streamable.spouse_pk = null;
        }
        return streamable;
    };
    Person.type = "persons";
    return Person;
}(SpudObject));
var PersonSearchDialog = (function (_super) {
    __extends(PersonSearchDialog, _super);
    function PersonSearchDialog(options) {
        _super.call(this, options);
    }
    PersonSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Person", "persons", false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search persons";
        this.options.description = "Please search for an person.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PersonSearchDialog;
}(ObjectSearchDialog));
var PersonChangeDialog = (function (_super) {
    __extends(PersonChangeDialog, _super);
    function PersonChangeDialog(options) {
        _super.call(this, options);
        this.type = "persons";
        this.type_name = "person";
    }
    PersonChangeDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["cover_photo", new PhotoSelectField("Photo", false)],
                    ["first_name", new TextInputField("First name", true)],
                    ["middle_name", new TextInputField("Middle name", false)],
                    ["last_name", new TextInputField("Last name", false)],
                    ["called", new TextInputField("Called", false)],
                    ["sex", new SelectInputField("Sex", [["1", "Male"], ["2", "Female"]], true)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    ["work", new AjaxSelectField("Work", "places", false)],
                    ["home", new AjaxSelectField("Home", "places", false)],
                    ["mother", new AjaxSelectField("Mother", "persons", false)],
                    ["father", new AjaxSelectField("Father", "persons", false)],
                    ["spouse", new AjaxSelectField("Spouse", "persons", false)],
                ] },
            { name: 'other', title: 'Other', fields: [
                    ["email", new TextInputField("E-Mail", false)],
                    ["dob", new DateInputField("Date of birth", false)],
                    ["dod", new DateInputField("Date of death", false)],
                    ["notes", new PInputField("Notes", false)],
                ] },
        ];
        this.options.title = "Change person";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PersonChangeDialog.prototype.save_success = function (data) {
        var person = new Person(data);
        if (this.obj.id != null) {
            window._person_changed.trigger(person);
        }
        else {
            window._person_created.trigger(person);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PersonChangeDialog;
}(ObjectChangeDialog));
var PersonDeleteDialog = (function (_super) {
    __extends(PersonDeleteDialog, _super);
    function PersonDeleteDialog(options) {
        _super.call(this, options);
        this.type = "persons";
        this.type_name = "person";
    }
    PersonDeleteDialog.prototype.save_success = function (data) {
        window._person_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PersonDeleteDialog;
}(ObjectDeleteDialog));
var PersonCriteriaWidget = (function (_super) {
    __extends(PersonCriteriaWidget, _super);
    function PersonCriteriaWidget(options) {
        _super.call(this, options);
        this.type = "persons";
    }
    PersonCriteriaWidget.prototype.set = function (input_criteria) {
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
    return PersonCriteriaWidget;
}(ObjectCriteriaWidget));
var PersonListWidget = (function (_super) {
    __extends(PersonListWidget, _super);
    function PersonListWidget(options) {
        _super.call(this, options);
        this.type = "persons";
    }
    PersonListWidget.prototype.to_object = function (streamable) {
        return new Person(streamable);
    };
    PersonListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._person_changed.add_listener(this, function (person) {
            var li = _this.create_li_for_obj(person);
            _this.get_item(person.id).replaceWith(li);
        });
        window._person_deleted.add_listener(this, function (person_id) {
            _this.get_item(person_id).remove();
            _this.load_if_required();
        });
    };
    PersonListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            obj: null,
            obj_id: null
        };
        var viewport;
        viewport = new PersonDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PersonListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        return details;
    };
    PersonListWidget.prototype.get_description = function (obj) {
        return _super.prototype.get_description.call(this, obj);
    };
    return PersonListWidget;
}(ObjectListWidget));
var PersonDetailInfobox = (function (_super) {
    __extends(PersonDetailInfobox, _super);
    function PersonDetailInfobox(options) {
        _super.call(this, options);
    }
    PersonDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["middle_name", new TextOutputField("Middle name")],
            ["last_name", new TextOutputField("Last name")],
            ["called", new TextOutputField("Called")],
            ["sex", new SelectOutputField("Sex", [["1", "Male"], ["2", "Female"]])],
            ["email", new TextOutputField("E-Mail")],
            ["dob", new TextOutputField("Date of birth")],
            ["dod", new TextOutputField("Date of death")],
            ["work", new LinkOutputField("Work", "places")],
            ["home", new LinkOutputField("Home", "places")],
            ["spouses", new LinkListOutputField("Spouses", "persons")],
            ["notes", new POutputField("Notes")],
            ["grandparents", new LinkListOutputField("Grand Parents", "persons")],
            ["uncles_aunts", new LinkListOutputField("Uncles and Aunts", "persons")],
            ["parents", new LinkListOutputField("Parents", "persons")],
            ["siblings", new LinkListOutputField("Siblings", "persons")],
            ["cousins", new LinkListOutputField("Cousins", "persons")],
            ["children", new LinkListOutputField("Children", "persons")],
            ["nephews_nieces", new LinkListOutputField("Nephews and Nieces", "persons")],
            ["grandchildren", new LinkListOutputField("Grand children", "persons")],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PersonDetailInfobox.prototype.set = function (person) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, person);
        this.options.obj = person;
        this.img.set(person.cover_photo);
    };
    return PersonDetailInfobox;
}(Infobox));
var PersonListViewport = (function (_super) {
    __extends(PersonListViewport, _super);
    function PersonListViewport(options) {
        _super.call(this, options);
        this.type = "persons";
        this.type_name = "Person";
    }
    PersonListViewport.prototype.create_object_list_widget = function (options) {
        return new PersonListWidget(options);
    };
    PersonListViewport.prototype.create_object_criteria_widget = function (options) {
        return new PersonCriteriaWidget(options);
    };
    PersonListViewport.prototype.create_object_search_dialog = function (options) {
        return new PersonSearchDialog(options);
    };
    return PersonListViewport;
}(ObjectListViewport));
var PersonDetailViewport = (function (_super) {
    __extends(PersonDetailViewport, _super);
    function PersonDetailViewport(options) {
        _super.call(this, options);
        this.type = "persons";
        this.type_name = "Person";
    }
    PersonDetailViewport.prototype.to_object = function (streamable) {
        return new Person(streamable);
    };
    PersonDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        var mythis = this;
        window._person_changed.add_listener(this, function (obj) {
            if (obj.id === _this.options.obj_id) {
                mythis.set(obj);
            }
        });
        window._person_deleted.add_listener(this, function (obj_id) {
            if (obj_id === _this.options.obj_id) {
                mythis.remove();
            }
        });
    };
    PersonDetailViewport.prototype.get_photo_criteria = function () {
        return {
            'person': this.options.obj_id
        };
    };
    PersonDetailViewport.prototype.create_object_list_widget = function (options) {
        return new PersonListWidget(options);
    };
    PersonDetailViewport.prototype.create_object_detail_infobox = function (options) {
        return new PersonDetailInfobox(options);
    };
    PersonDetailViewport.prototype.create_object_list_viewport = function (options) {
        return new PersonListViewport(options);
    };
    PersonDetailViewport.prototype.create_object_change_dialog = function (options) {
        return new PersonChangeDialog(options);
    };
    PersonDetailViewport.prototype.create_object_delete_dialog = function (options) {
        return new PersonDeleteDialog(options);
    };
    return PersonDetailViewport;
}(ObjectDetailViewport));
