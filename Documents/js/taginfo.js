/**
 * Created by zyj on 2017/1/30.
 */
var opts = {
    //innerImage: {url: '../img/logo.png', width: 56, height: 56 }, //内部图片
    lines: 13, // 花瓣数目
    length: 20, // 花瓣长度
    width: 10, // 花瓣宽度
    radius: 30, // 花瓣距中心半径
    corners: 1, // 花瓣圆滑度 (0-1)
    rotate: 0, // 花瓣旋转角度
    direction: 1, // 花瓣旋转方向 1: 顺时针, -1: 逆时针
    color: '#5882FA', // 花瓣颜色
    speed: 1, // 花瓣旋转速度
    trail: 60, // 花瓣旋转时的拖影(百分比)
    shadow: false, // 花瓣是否显示阴影
    hwaccel: false, //spinner 是否启用硬件加速及高速旋转
    className: 'spinner', // spinner css 样式名称
    zIndex: 2e9, // spinner的z轴 (默认是2000000000)
    top: 'auto', // spinner 相对父容器Top定位 单位 px
    left: 'auto', // spinner 相对父容器Left定位 单位 px
    position: 'relative', // element position
    progress: true,      // show progress tracker
    progressTop: 0,       // offset top for progress tracker
    progressLeft: 0       // offset left for progress tracker
};
var spinner = new Spinner(opts)

bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
    $('#alert_placeholder').html('<div id="myAlert" class="alert alert-warning"><a href="#" class="close" data-dismiss="alert">&times;</a>'+message+'</div>')
}
bootstrap_alert.success = function(message) {
    $('#alert_placeholder').html('<div id="myAlert" class="alert alert-success"><a href="#" class="close" data-dismiss="alert">&times;</a>'+message+'</div>')
}

var tagData

var methodObj={
    getDate:function(pid) {
        console.log(pid);
        $.ajax({
            url: 'http://127.0.0.1:8080/api?m=tag_list&sid=1&pid='+pid,
            data: pid,
            type: 'GET',
            dataType: "jsonp",
            jsonp: 'callback',
            success: function (data) {
                var templi = Handlebars.compile($("#templi").html());
                tagData = data['data']
                $('.tablelist').html(templi(data));
            },
            error: function () {
                console.log('接口有问题');
            }
        })
    }
};

//创建新的tag
function creatTag(pid,tag,tagBranch){

    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=tag_add&sid=1',
        data: {'pid':pid,'tag':tag,'tagBranch':tagBranch},
        type: 'POST',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                methodObj.getDate(pid);
                $('#addModal').modal('hide');
                bootstrap_alert.success('创建成功');
                setTimeout(function(){$("#myAlert").alert('close')},3000);
            }
        },
        error: function () {
            console.log('接口有问题');
        }
    })
}

//删除tag
function deleteTag(tid,pid){
    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=tag_delete&sid=1',
        data: {'tid':tid,'pid':pid},
        type: 'POST',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                methodObj.getDate(pid);
                $('#deleteModal').modal('hide');
                bootstrap_alert.success('删除成功');
                setTimeout(function () {
                    $("#myAlert").alert('close')
                }, 3000);
            }
        },
        error: function () {
            console.log('接口有问题');
        }
    })
}

//获取url里的参数
function getQueryString(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

$(function(){
    var tagInfo
    var pid = getQueryString('pid');
    methodObj.getDate(pid);
    document.getElementById("podname").innerHTML= "库名:  "+ getQueryString('podname');

    $(document).on('click','.newfolder',function(){
        $('#addModal').modal({
            keyboard: true
        })
    });

    $('#addModal').on('hidden.bs.modal', function (e) {
        console.log('hhh');
    });

    //删除行
    $(document).on('click','.removeli',function(){
        var index = $(this).attr('data-index');
        tagInfo = tagData[index];
        $('#deleteModal').modal({
            keyboard: true
        })
    });

    //编辑行
    $(document).on('click','.editli',function(){
        for(var i=0;i<3;i++) {
            $(this).parent().parent().parent().siblings('input').eq(i).removeAttr('readOnly');
        }
        $(this).parent().parent().parent().siblings('input').eq(0).focus();
    });

    //modal确认
    $(document).on('click','.creatconfri',function(){
        var tag = document.getElementById("tag-name").value;
        if (tag == ""){
            document.getElementById("tag-name-label").style.color="red";
            return;
        }else{
            document.getElementById("tag-name-label").style.color="";
        }

        var tagBranch = document.getElementById("tagBranch-name").value;
        if (tagBranch == ""){
            document.getElementById("tagBranch-name-label").style.color="red";
            return;
        }else{
            document.getElementById("tagBranch-name-label").style.color="";
        }

        creatTag(pid,tag,tagBranch)
    });

    //model删除确认
    $(document).on('click','.deleteconfir',function(){
        var tid = tagInfo['tid']
        deleteTag(tid,pid);
    })
});