$(document).ready(function (){

$(".form-group").each(function () {
    if($(this).children("input[type=text], input[type=email], input[type=file]").length !== 0) {
        if($(this).children("input").is("[required]")) {
            $(this).children("label").addClass("required");
        }
    } else {
        $(this).children("label").addClass("required");
    }
});


const $switcher = $("#id_self_payment");
const $studentInputFields = $("#student input");
const $payerInputFields = $("#payer input");
const $autoFillLabel = $(".auto-fill-label");

const $payerDatepickerButtons = $("#payer button .filter-option-inner-inner");
const $studentDatepickerButtons = $("#student button .filter-option-inner-inner");
const $payerDatepickerSelectTags = $("#payer select.datepicker");
const $studentDatepickerSelectTags = $("#student select.datepicker");

$switcher.on("click", toggle);

function copyAllFields() {
    let len = $studentInputFields.length;
    for(let i=0; i<len-1; i++) {
        $studentInputFields[i].value = $payerInputFields[i].value;
    }

    for(let i=0; i<3; i++) {
        $studentDatepickerButtons[i].innerHTML = $payerDatepickerButtons[i].innerHTML;
    }
}

function blockStudentFields(block) {
    let len = $studentInputFields.length;

    for(let i=0; i<len; i++) {
        $studentInputFields[i].disabled = block;
        if(block)
            $payerInputFields[i].addEventListener("keyup", copyAllFields);
        else
            $payerInputFields[i].removeEventListener("keyup", copyAllFields);
    }

    for(let i=0; i<3; i++) {
        $studentDatepickerButtons[i].disabled = block;
        $studentDatepickerSelectTags[i].disabled = block;
        if(block)
            $payerDatepickerSelectTags[i].addEventListener("change", copyAllFields)
        else
            $payerDatepickerSelectTags[i].removeEventListener("change", copyAllFields)
    }

    $autoFillLabel.css("display", block ? "inline": "none");
}

function toggle() {
    if($switcher.is(":checked")) {
        copyAllFields();
        blockStudentFields(true);
    } else {
        blockStudentFields(false);
    }
}

toggle();

})