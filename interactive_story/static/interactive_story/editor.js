$('.requirement [type="checkbox"], .event [type="checkbox"]').click(function (e) {
	$(this).parent().hide();
});

$('.sortable').sortable()