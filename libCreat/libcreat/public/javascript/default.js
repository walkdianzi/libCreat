/**
 * Created by zyj on 2017/1/30.
 */
var methodObj={
    getDate:function(data) {
        $.ajax({
            url: 'http://127.0.0.1:8080/api?m=addr_list&sid=1',
            data: data,
            type: 'GET',
            dataType: "json",
            success: function (data) {
                var templi = Handlebars.compile($("#templi").html());
                $('.tablelist').html(templi(data));
            },
            error: function () {
                console.log('接口有问题');
            }
        })
    }
};

$(function(){
    methodObj.getDate();
    $(document).on('click','.removeli',function(){
        $(this).parentsUntil('.tablelist').remove();
    });
    $(document).on('click','.newfolder',function(){
        var out=" <li class='datali'>"+
                    '<input type="text" value="" class="key" />'+
                    '<input type="text" value="" class="value" />'+
                    '<input type="text" value="" class="type" />'+
                    '<div class="operation">'+
                        '<ul>'+
                            '<li>'+
                                '<a href="javascript:void(0)">编辑</a>'+
                                '<a href="javascript:void(0)" class="removeli">删除</a>'+
                                '<a href="javascript:void(0)">历史</a>'+
                            '</li>'+
                        '</ul>'+
                    '</div>'+
                "</li>";
        $('.tablelist').append(out);
        $('.tablelist').find('input').eq(-3).focus();
    });
    $(document).on('click','.editli',function(){
        for(var i=0;i<3;i++) {
            $(this).parent().parent().parent().siblings('input').eq(i).removeAttr('readOnly');
        }
        $(this).parent().parent().parent().siblings('input').eq(0).focus();
    });
    $(document).on('keydown','.datali input',function(e){
        if(e.keyCode==13){
            $(this).attr('readOnly','true');
        }
    })
    $(document).on('click','.configname button',function(){
        $('.configname button').removeClass('active');
        $(this).addClass('active');
        methodObj.getDate();
    })
});