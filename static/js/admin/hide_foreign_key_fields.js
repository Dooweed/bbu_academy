/*jshint esversion: 6 */
"use strict";

$(document).ready(function () {
    const $newsRef = $("div.form-row.field-news_reference"),
        $trainingsRef = $("div.form-row.field-training_reference"),
        $coursesRef = $("div.form-row.field-course_reference"),
        $radio = $("div.form-row.field-reference input[name=reference]");

    function hide() {
        $newsRef.css("display", "none");
        $trainingsRef.css("display", "none");
        $coursesRef.css("display", "none");
    }

    function redisplay(event) {
        hide();
        let $value = event.target.value;
        if($value === "news_reference") {
            $newsRef.css("display", "block");
        } else if ($value === "training_reference") {
            $trainingsRef.css("display", "block");
        } else if ($value === "course_reference") {
            $coursesRef.css("display", "block");
        }
    }

    hide();
    let $value = $("div.form-row.field-reference input[name=reference][checked]").val();
    if($value === "news_reference") {
        $newsRef.css("display", "block");
    } else if ($value === "training_reference") {
        $trainingsRef.css("display", "block");
    } else if ($value === "course_reference") {
        $coursesRef.css("display", "block");
    }

    $radio.click(redisplay);
});