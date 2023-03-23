$(function() {
    $('[data-widget="customer-autocomplete"]').autocomplete({
        source: '/customers/autocomplete/',
        minLength: 3,
        select: function(event, ui) {
            $(this).val(ui.item.label);
            $('[name="customer"]').val(ui.item.value);
            return false;
        }
    });
});
