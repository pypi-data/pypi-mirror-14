
(function($) {

    function add_images(){

    try {
        var table = document.getElementsByTagName("table")[0];

        for (var i = 0, row; row = table.rows[i]; i++) {
           UID=$(row).attr("data-uid");
           var type=$(row).attr("data-type");
           if (type=="Image"){
               for (var j = 0, col; col = row.cells[j]; j++) {
                 var cell_id = $(col).attr("class");
                 if (cell_id == "preview") {
                    get_image_html(UID, col);
                 }
               }
           }
        }
    }
    catch(err){
        // for the case table does not exist
    }
    };

    function get_image_html(UID, col){
        var url = window.location.href
        var image_url = url.replace('folder_contents', 'image_html')
        $.post( image_url, { uid: UID }, function( data ) {
            col.innerHTML = data.html
        }, "json");
    }

    window.onload=add_images;

    MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

    var observer = new MutationObserver(function(mutations, observer) {
        add_images()
    });

    // define what element should be observed by the observer
    // and what types of mutations trigger the callback
    observer.observe(document, {
      subtree: true,
      attributes: true
});

}(jQuery));