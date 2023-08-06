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
window._category_created = new Signal();
window._category_changed = new Signal();
window._category_deleted = new Signal();
var CategoryStreamable = (function (_super) {
    __extends(CategoryStreamable, _super);
    function CategoryStreamable() {
        _super.apply(this, arguments);
    }
    return CategoryStreamable;
}(ObjectStreamable));
var Category = (function (_super) {
    __extends(Category, _super);
    function Category(streamable) {
        _super.call(this, streamable);
        this.description = parse_string(streamable.description);
        this.sort_order = parse_string(streamable.sort_order);
        this.sort_name = parse_string(streamable.sort_name);
        if (streamable.ascendants != null) {
            this.ascendants = [];
            for (var i = 0; i < streamable.ascendants.length; i++) {
                this.ascendants.push(new Category(streamable.ascendants[i]));
            }
            if (streamable.ascendants.length > 0) {
                this.parent = this.ascendants[0];
            }
            else {
                this.parent = null;
            }
        }
    }
    Category.prototype.to_streamable = function () {
        var streamable = _super.prototype.to_streamable.call(this);
        streamable.description = this.description;
        streamable.sort_order = this.sort_order;
        streamable.sort_name = this.sort_name;
        if (this.parent != null) {
            streamable.parent = this.parent.id;
        }
        else {
            streamable.parent = null;
        }
        return streamable;
    };
    Category.type = "categorys";
    return Category;
}(SpudObject));
var CategorySearchDialog = (function (_super) {
    __extends(CategorySearchDialog, _super);
    function CategorySearchDialog(options) {
        _super.call(this, options);
    }
    CategorySearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Category", "categorys", false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search categories";
        this.options.description = "Please search for an category.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return CategorySearchDialog;
}(ObjectSearchDialog));
var CategoryChangeDialog = (function (_super) {
    __extends(CategoryChangeDialog, _super);
    function CategoryChangeDialog(options) {
        _super.call(this, options);
        this.type = "categorys";
        this.type_name = "category";
    }
    CategoryChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["description", new PInputField("Description", false)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["sort_name", new TextInputField("Sort Name", false)],
            ["sort_order", new TextInputField("Sort Order", false)],
            ["parent", new AjaxSelectField("Parent", "categorys", false)],
        ];
        this.options.title = "Change category";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    CategoryChangeDialog.prototype.save_success = function (data) {
        var category = new Category(data);
        if (this.obj.id != null) {
            window._category_changed.trigger(category);
        }
        else {
            window._category_created.trigger(category);
        }
        _super.prototype.save_success.call(this, data);
    };
    return CategoryChangeDialog;
}(ObjectChangeDialog));
var CategoryDeleteDialog = (function (_super) {
    __extends(CategoryDeleteDialog, _super);
    function CategoryDeleteDialog(options) {
        _super.call(this, options);
        this.type = "categorys";
        this.type_name = "category";
    }
    CategoryDeleteDialog.prototype.save_success = function (data) {
        window._category_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return CategoryDeleteDialog;
}(ObjectDeleteDialog));
var CategoryCriteriaWidget = (function (_super) {
    __extends(CategoryCriteriaWidget, _super);
    function CategoryCriteriaWidget(options) {
        _super.call(this, options);
        this.type = "categorys";
    }
    CategoryCriteriaWidget.prototype.set = function (input_criteria) {
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
    return CategoryCriteriaWidget;
}(ObjectCriteriaWidget));
var CategoryListWidget = (function (_super) {
    __extends(CategoryListWidget, _super);
    function CategoryListWidget(options) {
        _super.call(this, options);
        this.type = "categorys";
    }
    CategoryListWidget.prototype.to_object = function (streamable) {
        return new Category(streamable);
    };
    CategoryListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._category_changed.add_listener(this, function (category) {
            var li = _this.create_li_for_obj(category);
            _this.get_item(category.id).replaceWith(li);
        });
        window._category_deleted.add_listener(this, function (category_id) {
            _this.get_item(category_id).remove();
            _this.load_if_required();
        });
    };
    CategoryListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            obj: null,
            obj_id: null
        };
        var viewport;
        viewport = new CategoryDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    CategoryListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        if (obj.sort_order || obj.sort_name) {
            details.push($("<div/>").text(obj.sort_name + " " + obj.sort_order));
        }
        return details;
    };
    CategoryListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    return CategoryListWidget;
}(ObjectListWidget));
var CategoryDetailInfobox = (function (_super) {
    __extends(CategoryDetailInfobox, _super);
    function CategoryDetailInfobox(options) {
        _super.call(this, options);
    }
    CategoryDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextOutputField("Title")],
            ["sort_name", new TextOutputField("Sort Name")],
            ["sort_order", new TextOutputField("Sort Order")],
            ["description", new POutputField("Description")],
            ["ascendants", new LinkListOutputField("Ascendants", "categorys")],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    CategoryDetailInfobox.prototype.set = function (category) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, category);
        this.options.obj = category;
        this.img.set(category.cover_photo);
    };
    return CategoryDetailInfobox;
}(Infobox));
var CategoryListViewport = (function (_super) {
    __extends(CategoryListViewport, _super);
    function CategoryListViewport(options) {
        _super.call(this, options);
        this.type = "categorys";
        this.type_name = "Category";
    }
    CategoryListViewport.prototype.create_object_list_widget = function (options) {
        return new CategoryListWidget(options);
    };
    CategoryListViewport.prototype.create_object_criteria_widget = function (options) {
        return new CategoryCriteriaWidget(options);
    };
    CategoryListViewport.prototype.create_object_search_dialog = function (options) {
        return new CategorySearchDialog(options);
    };
    return CategoryListViewport;
}(ObjectListViewport));
var CategoryDetailViewport = (function (_super) {
    __extends(CategoryDetailViewport, _super);
    function CategoryDetailViewport(options) {
        _super.call(this, options);
        this.type = "categorys";
        this.type_name = "Category";
    }
    CategoryDetailViewport.prototype.to_object = function (streamable) {
        return new Category(streamable);
    };
    CategoryDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        var mythis = this;
        window._category_changed.add_listener(this, function (obj) {
            if (obj.id === _this.options.obj_id) {
                mythis.set(obj);
            }
        });
        window._category_deleted.add_listener(this, function (obj_id) {
            if (obj_id === _this.options.obj_id) {
                mythis.remove();
            }
        });
    };
    CategoryDetailViewport.prototype.get_photo_criteria = function () {
        return {
            'category': this.options.obj_id,
            'category_descendants': true
        };
    };
    CategoryDetailViewport.prototype.create_object_list_widget = function (options) {
        return new CategoryListWidget(options);
    };
    CategoryDetailViewport.prototype.create_object_detail_infobox = function (options) {
        return new CategoryDetailInfobox(options);
    };
    CategoryDetailViewport.prototype.create_object_list_viewport = function (options) {
        return new CategoryListViewport(options);
    };
    CategoryDetailViewport.prototype.create_object_change_dialog = function (options) {
        return new CategoryChangeDialog(options);
    };
    CategoryDetailViewport.prototype.create_object_delete_dialog = function (options) {
        return new CategoryDeleteDialog(options);
    };
    return CategoryDetailViewport;
}(ObjectDetailViewport));
