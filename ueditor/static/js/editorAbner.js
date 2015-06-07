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
    $.get('/getChannels',function(data){
        data = JSON.parse(data)
        var options = data.map(function(e){
            return "<option>" + e.title + "</option>"
        }).join(" ")

        $("select").html(options)
    })

    var type;
    var id;
    var href = window.location.href;
    var match = href.match(/\?article_id=(\d*)/);
    if (match && match[1]) {//说明是修改文章
        type = "modify";
        id = match[1];
        $.get('/getArticleInfo', {id: id}, function (data) {
            data = JSON.parse(data)
            $("#article-title").val(data.title)
            ue.setContent(data['body']);
            $("select").val(data['channel'])
            $("#article-desc").val(data['desc'])
            console.log(data);
        })
    }

    $("#saveSubmit").click(saveSubmit);


    function saveSubmit() {
        var content = ue.getContent();
        var firstImage = $(content).find("img")[0];
        var imageSrc = firstImage && firstImage.src || "null";
        var data = {
            'content': content,
            'title': $("#article-title").val(),
            'catalog': $('#catalog').val(),
            'image': imageSrc,
            'id':id
        };
        var url = type === "modify"? "/modify": "/save";
        $.post(url, data, function (msg) {
                msg = JSON.parse(msg);
                if (msg.status === 'success') {
                    alert("操作成功");
                }
            })
        }


});