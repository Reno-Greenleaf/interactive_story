function reorderEvents() {
	var chron = $('.plot li [type="number"]');
	chron.each(function(index) {
		$(this).val(index+1);
	})
}

reorderEvents();

$('.requirement [type="checkbox"], .event [type="checkbox"]').click(function (e) {
	$(this).parent().hide();
});

$('.sortable').sortable();
$('.plot').sortable({
	update: reorderEvents
});