function CustomFileBrowser(callback, value, meta) {

    var cmsURL = "/uploader/all/?_popup=1&type=" + meta.filetype;

    tinymce.activeEditor.windowManager.open(
        {
            file: cmsURL,
            title: "File Manager",
            width: 780,
            height: 500
        },
        {
            oninsert: function (url) {
                callback(url);
            }
        }
    );
    return false;
}
