let $edit_form = $(".edit-student"), $delete_form = $(".delete-student"), $reload = $(".reload-student"), $student_form = $("#student"), $payer_form = $("#payer");

const $filled_students = $("div#filled-students");

function ajax(event) {
    event.preventDefault();
    let method = $(this).attr("method");
    let url = $(this).attr("data-url");
    let form_data = method.toUpperCase() === "POST" ? new FormData(this) : $(this).serialize();
    $.ajax({
        url: url,
        type: method,
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            populate_blocks(data);

            if(event.data != null && event.data.hasOwnProperty("callback_function"))
                event.data.callback_function();
        },
        error: function(data){ console.log("Something went wrong"); console.log(data); }
    });
}

function reattach_event_listeners() {
    $edit_form.off("submit");
    $delete_form.off("submit");
    $reload.off("click");

    $reload = $(".reload-student");
    $edit_form = $(".edit-student");
    $delete_form = $(".delete-student");

    $edit_form.submit(ajax);
    $delete_form.submit(ajax);
    $reload.on("click", load_page);
}

function scroll_to_students() {
    $('html, body').animate({
        scrollTop: $filled_students.offset().top
    }, 100);
}

$edit_form.submit(ajax);
$delete_form.submit(ajax);
$payer_form.submit(ajax);
$student_form.submit({callback_function: scroll_to_students},ajax);

function populate_blocks(data) {
    if(data["student_form"])
        $student_form.html(jQuery.parseHTML(data["student_form"]));
    if(data["students_list"])
        $filled_students.html(jQuery.parseHTML(data["students_list"]));
    if(data["payer_form"])
        $payer_form.html(jQuery.parseHTML(data["payer_form"]));

    $("#id_student_passport_received_date_day").selectpicker();
    $("#id_student_passport_received_date_month").selectpicker();
    $("#id_student_passport_received_date_year").selectpicker();
    $("#id_study_type").selectpicker();

    $(".form-group").each(function () {
        console.log(this);
        if($(this).find("input[required], select[required]").length !== 0) {
            $(this).find("label").addClass("required");
        }
    });

    reattach_event_listeners();
}

function load_page() {
    $.ajax({
        url: $("#data-load-url").attr("data-load"),
        success: function (data) { populate_blocks(data); },
        error: function(data){ console.log("Something went wrong"); console.log(data); }
    });
}

$( document ).ready(function() {
    load_page();
});