/// <reference path="photo.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var Streamable = (function () {
    function Streamable() {
    }
    return Streamable;
}());
var GenericStreamable = (function () {
    function GenericStreamable() {
    }
    return GenericStreamable;
}());
var StreamableList = (function () {
    function StreamableList() {
    }
    return StreamableList;
}());
var ObjectStreamable = (function (_super) {
    __extends(ObjectStreamable, _super);
    function ObjectStreamable() {
        _super.apply(this, arguments);
    }
    return ObjectStreamable;
}(Streamable));
var SpudObject = (function () {
    function SpudObject(streamable) {
        this.id = parse_number(streamable.id);
        this.title = parse_string(streamable.title);
        if (streamable.cover_photo != null) {
            this.cover_photo = new Photo(streamable.cover_photo);
        }
    }
    SpudObject.prototype.to_streamable = function () {
        var streamable = new ObjectStreamable;
        streamable['id'] = this.id;
        streamable['title'] = this.title;
        if (this.cover_photo != null) {
            streamable['cover_photo_pk'] = this.cover_photo.id;
        }
        return streamable;
    };
    SpudObject.type = null;
    return SpudObject;
}());
