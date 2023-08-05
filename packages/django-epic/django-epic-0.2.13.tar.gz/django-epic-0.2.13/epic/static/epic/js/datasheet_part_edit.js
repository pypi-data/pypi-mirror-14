// Hack alert: the default getValue() function in text_widget.js returns
// the auto-completion label rather than the value, which is just broken.
// Override that here:
if ("yourlabs" in window) {
    yourlabs.TextWidget.prototype.getValue = function (choice) {
	return choice.attr("data-value");
   }
}

$(function () {

    function get_part_info (query, callback) {
		var url = "/epic/part/info?" + query;
		$.getJSON (url, "", function (obj) {
			callback (obj);
		});
    }

    function part_changed (obj) {
		var prefix = obj.attr("id").replace (/-id$/, "");
		var mfg_pn = $("#" + prefix + "-mfg_pn");

		var part_id = obj.val ();
		if (!part_id) {
			mfg_pn.val ("");
			return;
		}
		var query = "pid=" + part_id;

		get_part_info (query,
					   function (part_info) {
						   if (!(part_id in part_info)) {
							   mfg_pn.val ("");
							   return;
						   }
						   obj = part_info[part_id];
						   mfg_pn.val (obj["mfg"] + " " + obj["mfg_pn"])
					   });
    }

	$("body").on ("selectChoice",
				  "input.autocomplete-light-text-widget[name$=-id]",
				  function () { part_changed ($(this)) });

    $("input.autocomplete-light-text-widget[name$=-id]").change(function () {
        part_changed ($(this));
    });

});
