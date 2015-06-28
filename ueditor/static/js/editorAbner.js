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
    $.get('/getChannels', function (data) {
        data = JSON.parse(data)
        var options = data.map(function (e) {
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
        setTimeout(function() {
            $.get('/getArticleInfo', {id: id}, function (data) {
                data = JSON.parse(data)
                $("#article-title").val(data.title)
                ue.setContent('<p><img src="' + data.image + '" /></p>' + data['body']);
                $("select").val(data['channel'])
                $("#article-desc").val(data['desc'])
                console.log(data);
            })
        }, 1000)
    }

    $("#saveSubmit").click(function saveSubmit(e) {
        e = e|| window.event;
        e.preventDefault();
        var content = ue.getContent();
        var imgs = $(content).find("img");
        var firstImage = imgs[0]
        imgs.each(function (i, e) {
            if (e.src.search(window.location.host) === -1) {
                e.src = "http://" + window.location.host + e.src;
                //e.src = ""
            }
        });
        //$(content).find("p").remove();
        var b = "";
        $(content).each(function(i, e){
            if(i!=0){
                b+= e.outerHTML;
            }
        })
        var imageSrc = firstImage && firstImage.src || "null";

        var data = {
            'content': b,
            'title': $("#article-title").val(),
            'desc': $('#article-desc').val(),
            'image': imageSrc,
            'id': id,
            'channel': $("select").val(),
            'text':ue.getContentTxt()
        };
	if(data.content === ""){
		alert("请输入文章内容");
		return;
	}else if(data.image === "null"){
		alert("请在文章起始插入图片");
		return;
	}
        var url = type === "modify" ? "/modify" : "/save";
        $.post(url, data, function (msg) {
            msg = JSON.parse(msg);
            if (msg.status === 'success') {
		// 保存
		if(msg.id !== undefined){
			$.post("http://www.funpeach.com:8000/push_article",
				{id:msg.id}, 
				function(msg){
					msg = JSON.parse(msg);
					if(msg.status === "OK"){
						alert("保存发布成功");
						window.location.href = "/";
						return;
					}
				}
			       )
		}else{	
                	alert("修改成功");
                	window.location.href = "/";
            	}
           }})

    })
})
