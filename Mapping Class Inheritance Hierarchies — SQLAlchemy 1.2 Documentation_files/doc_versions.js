

var doc_versions = [
  {
    "version": "Version 1.2",
    "slug": "rel_1_2"
    
  },
  {
    "version": "Version 1.1",
    "slug": "rel_1_1"
    
  },
  {
    "version": "Version 1.0",
    "slug": "rel_1_0"
    ,"latest_warning": true
  },
  {
    "version": "Version 0.9",
    "slug": "rel_0_9"
    ,"latest_warning": true
  }
];

var _version_lookup = {};
for (var key in doc_versions) {
    version = doc_versions[key];
    _version_lookup[version.slug] = version;
}

function renderDocVersions() {

    $('#version_menu,.version-listing').empty();
    for (var key in doc_versions) {
        obj = doc_versions[key];
        current_url = docs_base + "/en/" + obj.slug + "/";
        $("#version_menu,.version-listing").append('<li><a href="' + current_url + '">' + obj.version + '</a></li>');
    }
}


$(document).ready(function() {
    renderDocVersions();
});
