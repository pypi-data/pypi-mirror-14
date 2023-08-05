(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.rawButton = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
function place_raw_button() {
    var navbar = $(".navbar-default .container-fluid .navbar-right").get(0);
    $(navbar).append("<button class='btn btn-xs btn-default' id='raw-btn'>Raw</button>");
    $('#raw-btn').bind("click", function() {
        var filename = Jupyter.editor.file_path;
        var raw_path = window.location.href.replace("edit", "files");
        window.open(raw_path);
    });
}

function load_ipython_extension() {
    console.log("Loading raw-button extension...");
    place_raw_button();
}

exports.load_ipython_extension = load_ipython_extension

},{}]},{},[1])(1)
});