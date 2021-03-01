const $checkbox = $("#id_special_price");
const $inn_field = $("#id_inn");

function refresh_inn_field() {
    $inn_field.parent("div.form-group").css("display", $checkbox.prop("checked") ? "block": "none");
}

$checkbox.on("click", refresh_inn_field)

refresh_inn_field();