/**
 *
 * Created by abnerzheng on 15/5/24.
 */

$(document).ready(function () {
    jQuery.jqtab = function (tabtit, tabcon) {
        $(tabcon).hide();
        $(tabtit + " li:first").addClass("thistab").show();
        $(tabcon + ":first").show();
        $(tabtit + " li").click(function () {
            $(tabtit + " li").removeClass("thistab");
            $(this).addClass("thistab");
            $(tabcon).hide();
            var activeTab = $(this).find("a").attr("tab");
            $("#" + activeTab).fadeIn();
            return false;
        });
    };
    /*调用方法如下：*/
    $.jqtab("#tabs", ".tab_con");
});