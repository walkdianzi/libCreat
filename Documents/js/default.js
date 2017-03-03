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

//pod数据
var podData

var methodObj={
    getDate:function(data) {
        $.ajax({
            url: 'http://127.0.0.1:8080/api?m=spec_list&sid=1',
            data: data,
            type: 'GET',
            dataType: "jsonp",
            jsonp: 'callback',
            success: function (data) {
                console.log(data);
                podData = data['data']
                var templi = Handlebars.compile($("#templi").html());
                $('.tablelist').html(templi(data));
            },
            error: function () {
                console.log('接口有问题');
            }
        })
    }
};

//创建新的pod
function creatPod(podName,repoName,podspecName,sourceSSHUrl,sourceHttpUrl,libSSHUrl,libHttpUrl){

    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=spec_add&sid=1',
        data: {'podName':podName,'repoName':repoName,'podspecName':podspecName,'sourceSSHUrl':sourceSSHUrl,'sourceHttpUrl':sourceHttpUrl,'libSSHUrl':libSSHUrl,'libHttpUrl':libHttpUrl},
        type: 'POST',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                methodObj.getDate();
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

//更新pod
function updatePod(podName,repoName,podspecName,sourceSSHUrl,sourceHttpUrl,libSSHUrl,libHttpUrl,pid){

    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=spec_update&sid=1',
        data: {'podName':podName,'repoName':repoName,'podspecName':podspecName,'sourceSSHUrl':sourceSSHUrl,'sourceHttpUrl':sourceHttpUrl,'libSSHUrl':libSSHUrl,'libHttpUrl':libHttpUrl,'pid':pid},
        type: 'POST',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                methodObj.getDate();
                $('#addModal').modal('hide');
                bootstrap_alert.success('更新成功');
                setTimeout(function(){$("#myAlert").alert('close')},3000);
            }
        },
        error: function () {
            console.log('接口有问题');
        }
    })
}

//删除pod
function deletePod(pid){
    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=spec_delete&sid=1',
        data: {'pid':pid},
        type: 'POST',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                methodObj.getDate();
                $('#deleteModal').modal('hide');
                bootstrap_alert.success('删除成功');
                setTimeout(function(){$("#myAlert").alert('close')},3000);
            }
        },
        error: function () {
            console.log('接口有问题');
        }
    })
}

//更新无lib的spec
function updateNoLib(){
    $.ajax({
        url: 'http://127.0.0.1:8080/api?m=update_no_lib&sid=1',
        type: 'GET',
        dataType: "jsonp",
        jsonp: 'callback',
        success: function (data) {
            spinner.spin();
            if (data['status'] != 0) {
                bootstrap_alert.warning(data['info']);
            }
            else {
                bootstrap_alert.success('更新成功');
                setTimeout(function(){$("#myAlert").alert('close')},3000);
            }
        },
        error: function () {
            spinner.spin();
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
    var podInfo
    methodObj.getDate();

    $(document).on('click','.newfolder',function(){
        podInfo = null;
        $('#addModal').modal({
            keyboard: true
        })
    });
    $(document).on('click','.refresh',function(){
        var target = document.getElementById('container1');
        spinner.spin(target);
        updateNoLib();
    });

    //删除行
    $(document).on('click','.removeli',function(){
        var index = $(this).attr('data-index');
        podInfo = podData[index];
        $('#deleteModal').modal({
            keyboard: true
        })
    });

    //跳转到标签信息
    $(document).on('click','.tagli',function(){
        var pid = $(this).parent().parent().parent().siblings('input').eq(0).val();
        var podname = $(this).parent().parent().parent().siblings('input').eq(1).val();
        window.location.href="taginfo.html?pid=" + pid + "&podname=" + podname;
    });
    //编辑行
    $(document).on('click','.editli',function(){
        var index = $(this).attr('data-index');
        podInfo = podData[index];
        $('#addModal').modal({
            keyboard: true
        })
    });

    //modal创建更新确认
    $(document).on('click','.creatconfri',function(){
        var podName = document.getElementById("pod-name").value;
        if (podName == ""){
            document.getElementById("pod-name-label").style.color="red";
            return;
        }else{
            document.getElementById("pod-name-label").style.color="";
        }

        var repoName = document.getElementById("repo-name").value;
        if (repoName == ""){
            document.getElementById("repo-name-label").style.color="red";
            return;
        }else{
            document.getElementById("repo-name-label").style.color="";
        }

        var podspecName = document.getElementById("podspec-name").value;
        if (podspecName == ""){
            document.getElementById("podspec-name-label").style.color="red";
            return;
        }else{
            document.getElementById("podspec-name-label").style.color="";
        }

        var sourceSSHUrl = document.getElementById("sourceSSHUrl").value;
        if (sourceSSHUrl == ""){
            document.getElementById("sourceSSHUrl-label").style.color="red";
            return;
        }else{
            document.getElementById("sourceSSHUrl-label").style.color="";
        }

        var sourceHttpUrl = document.getElementById("sourceHttpUrl").value;
        if (sourceHttpUrl == ""){
            document.getElementById("sourceHttpUrl-label").style.color="red";
            return;
        }else{
            document.getElementById("sourceHttpUrl-label").style.color="";
        }

        var libSSHUrl = document.getElementById("libSSHUrl").value;
        if (libSSHUrl == ""){
            document.getElementById("libSSHUrl-label").style.color="red";
            return;
        }else{
            document.getElementById("libSSHUrl-label").style.color="";
        }

        var libHttpUrl = document.getElementById("libHttpUrl").value;
        if (libHttpUrl == ""){
            document.getElementById("libHttpUrl-label").style.color="red";
            return;
        }else{
            document.getElementById("libHttpUrl-label").style.color="";
        }

        var confirText = document.getElementById("confir").value;
        if (confirText == '创建') {
            console.log('创建')
            creatPod(podName, repoName, podspecName, sourceSSHUrl, sourceHttpUrl, libSSHUrl, libHttpUrl)
        }else{
            console.log('修改')
            updatePod(podName, repoName, podspecName, sourceSSHUrl, sourceHttpUrl, libSSHUrl, libHttpUrl,podInfo['pid'])
        }
    });

    //model删除确认
    $(document).on('click','.deleteconfir',function(){
        var pid = podInfo['pid'];
        deletePod(pid);
    })

    $('#addModal').on('show.bs.modal', function (event) {
        var modal = $(this);
        if (podInfo == null){
            //创建
            modal.find('.modal-title').text('添加新Pod')
            modal.find('.pod-name').val('');
            modal.find('.repo-name').val('');
            modal.find('.podspec-name').val('');
            modal.find('.sourceSSHUrl').val('');
            modal.find('.sourceHttpUrl').val('');
            modal.find('.libSSHUrl').val('');
            modal.find('.libHttpUrl').val('');
            modal.find('.creatconfri').text('创建');
            modal.find('.creatconfri').val('创建');
        }else {
            //编辑
            modal.find('.modal-title').text('修改: ' + podInfo['podName'])
            modal.find('.pod-name').val(podInfo['podName']);
            modal.find('.repo-name').val(podInfo['repoName']);
            modal.find('.podspec-name').val(podInfo['podspecName']);
            modal.find('.sourceSSHUrl').val(podInfo['sourceSSHUrl']);
            modal.find('.sourceHttpUrl').val(podInfo['sourceHttpUrl']);
            modal.find('.libSSHUrl').val(podInfo['libSSHUrl']);
            modal.find('.libHttpUrl').val(podInfo['libHttpUrl']);
            modal.find('.creatconfri').text('修改');
            modal.find('.creatconfri').val('修改');
        }
    })
});