function reorderEvents() {
	var chron = $('.plot li [type="number"]');
	chron.each(function(index) {
		$(this).val(index+1);
	})
}

function reorderRequirements() {
	var reqs = $($('.requirements li [type="number"]').get().reverse());
	reqs.each(function(index) {
		$(this).val(index+1);
	})
}

reorderEvents();
reorderRequirements();

$('.requirement [type="checkbox"], .event [type="checkbox"]').click(function (e) {
	$(this).parent().hide();
});

$('.requirements').sortable({
	update: reorderRequirements
});
$('.plot').sortable({
	update: reorderEvents
});