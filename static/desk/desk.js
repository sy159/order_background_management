var sendUsers = [];//骑手信息
var userOrders = [];//骑手所拥有的订单
var userSendLabel = [];//配送员的配送订单的送货地址
var userFetchLabel = [];//配送员的配送订单的取货地址
var polineArray = [];//选择的订单的配送线路
var fetchLabel = [];//选择的订单的取货地址
var sendLabel = [];//选择的订单的送货地址
var supplyArray = [];//待指派的订单
var orderHtmlFunTime = 0;


$(document).ready(function(){
    //查看配送员的订单详情
    $(document).on('click', '.location', function(){
        var uid = $(this).data('uid');
        var html = '';
        if (userOrders[uid] != undefined && userOrders[uid].length > 0) {
            $.each(userOrders[uid], function(i, item){
                html += '<tr>';
                html += '<td>' + item.store_name + '</td>';
                html += '<td>' + item.aim_site + '</td>';
                if (item.status == 2) {
                    html += '<td class="order-status">待取单</td>';
                    html += '<td><button type="button" class="btn btn-primary btn-ressign ng-scope changeOrder" data-uid="' + item.uid + '" data-order_id="' + item.supply_id + '">改派</button></td>';
                } else {
                    html += '<td class="order-status">配送中</td>';
                    html += '<td></td>';
                }
                html += '</tr>';
            });
        } else {
            html += '<tr>';
            html += '<td></td>';
            html += '<td>--</td>';
            html += '<td class="order-status">--</td>';
            html += '<td></td>';
            html += '</tr>';
        }
        $('.table-wrapper').find('tbody').html(html);
        $('.assigned-orders-modal').removeClass('ng-hide assigned-orders-modal--hide');
        var top = parseInt($(this).offset().top), thisHeight = parseInt($('.table-wrapper').find('tbody').height()), windowHeight = parseInt($(window).height());
        if (parseInt(top) + parseInt(thisHeight) > parseInt(windowHeight)) {
            top = windowHeight - thisHeight - 50;
        }
        $('.assigned-orders-modal').css('top', top);
    });
    //关闭订单详情
    $(document).click(function(e){
        var parent = e.target;
        if (!$('.assigned-orders-modal').hasClass('ng-hide assigned-orders-modal--hide') && !$(parent).parents('#orderDetail').hasClass('assigned-orders-modal') && !$(parent).hasClass('location')){
            $('.assigned-orders-modal').addClass('ng-hide assigned-orders-modal--hide')
        }
        if (!$(parent).hasClass('delivery-icon') && !$(parent).hasClass('deliveryman-icon-click') && !$(parent).parents('div').hasClass('deliveryman-icon-click')) {
            $('.deliveryman-icon-click').hide();
        }
    });

    //点击指派给配送的按钮事件
//    $(document).on('click', '.dispatch-button, .assign', function(e){
//     $(document).on('click', '.assign, .zhipaibutton', function(e){
//         e.stopPropagation();
//         var uid = $(this).data('uid');
//         var supplyIds = [];
//         $('.order-list').children('.selected').each(function(obj){
//             supplyIds.push($(this).data('supply_id'))
//         });
//         var supply_ids = '';
//         var num = supplyIds.length;
//         if (supplyIds.length > 0) {
//             supply_ids = supplyIds.join(',');
//         } else {
// //            alert('请选择指派单子')
//             art.dialog({
//                 content: '请选择一个有效的配送单子指派给该配送员',
//                 ok: function () {},
//                 cancelVal: '关闭',
//                 lock:true,
//                 cancel: true //为true等价于function(){}
//             });
//             return false;
//         }
//         var obj = $(this);
//         $(this).attr('disabled', true);
//         $.post(url + 'appointDeliver', {'uid':uid, 'supply_ids':supply_ids}, function(response){
//             obj.attr('disabled', false);
//             if (response.errcode == false) {
//                 $('.deliveryman-icon-click').hide();
//                 $('.order-list').children('.selected').each(function(obj){
//                     supplyArray[$(this).data('supply_id')].status = 2;
//                     userOrders[uid].push(supplyArray[$(this).data('supply_id')]);
//                     map.removeOverlay(polineArray[$(this).data('supply_id')]);
//                     map.removeOverlay(fetchLabel[$(this).data('supply_id')]);
//                     map.removeOverlay(sendLabel[$(this).data('supply_id')]);
//                     $(this).remove();
//                 });
//                 var tempFetch = parseInt($('#__content' + uid + ' .deliveryman-icon').find('.fetch_' + uid).text());
//                 $('.fetch_' + uid).text(tempFetch + num);
//                 sendUsersHtml(sendUsers, 0);
//             }
//         }, 'json');
//     });
    // $(document).on('click', '.order-tab a', function(){
    //     location.href = url + 'desk&type=' + $(this).data('type') + '&area_id=' + $('#choose_area').val();
    // });

    //选择待指派的单子
    $(document).on('click', '.order-item', function(){
        var supplyId = $(this).data('supply_id');
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            $(this).find('.checked-icon').removeClass('selected');
            
            map.removeOverlay(polineArray[supplyId]);
            map.removeOverlay(fetchLabel[supplyId]);
            map.removeOverlay(sendLabel[supplyId]);
            sendUsersHtml(sendUsers, 0);
        } else {
            $(this).addClass('selected');
            $(this).find('.checked-icon').addClass('selected');
            $('.dispatch-order-count').text($('.order-list').children('.selected').size());
            var sendHtml = '';
            sendHtml += '<div class="amap-marker-content" style="opacity: 1;">';
            sendHtml += '<div tpl="user" id="user_400000515608307626" class="user-marker">';
            sendHtml += '<div class="big-circle"></div>';
            sendHtml += '<div class="small-circle">送</div>';
            sendHtml += '<div class="triangle"></div>';
            sendHtml += '</div>';
            sendHtml += '</div>';
            console.log(supplyArray[supplyId].aim_lnt)
            console.log(supplyArray[supplyId].aim_lat)
            sendLabel[supplyId] = new BMap.Label(sendHtml, {position:new BMap.Point(supplyArray[supplyId].aim_lnt, supplyArray[supplyId].aim_lat), offset:new BMap.Size(-18, -50)});  // 创建文本标注对象
            map.addOverlay(sendLabel[supplyId]);
            
            var fetchHtml = '';
            fetchHtml += '<div class="amap-marker-content" style="opacity: 1;">';
            fetchHtml += '<div tpl="retailer" id="retailer_15105253" class="retailer-marker">';
            fetchHtml += '<div class="big-circle"></div>';
            fetchHtml += '<div class="small-circle">取</div>';
            fetchHtml += '<div class="triangle"></div>';
            fetchHtml += '</div>';
            fetchHtml += '</div>';
            fetchLabel[supplyId] = new BMap.Label(fetchHtml, {position:new BMap.Point(supplyArray[supplyId].from_lnt, supplyArray[supplyId].from_lat), offset:new BMap.Size(-18, -50)});  // 创建文本标注对象
            map.addOverlay(fetchLabel[supplyId]);
            
            polineArray[supplyId] = new BMap.Polyline([
                new BMap.Point(supplyArray[supplyId].from_lnt, supplyArray[supplyId].from_lat),
                new BMap.Point(supplyArray[supplyId].aim_lnt, supplyArray[supplyId].aim_lat)
            ], {strokeColor:"blue", strokeWeight:2, strokeOpacity:0.5});   //创建折线
            map.addOverlay(polineArray[supplyId]); 
            
            var newSendUsers = [];
            for (var uid in sendUsers) {
                var tmp = sendUsers[uid]
                tmp.distance = (map.getDistance(new BMap.Point(supplyArray[supplyId].from_lnt, supplyArray[supplyId].from_lat), new BMap.Point(sendUsers[uid].now_lng, sendUsers[uid].now_lat))).toFixed(2);
                newSendUsers.push(tmp);
            }
            newSendUsers = newSendUsers.sort(compare('distance'))
            sendUsersHtml(newSendUsers, 1);
        }
    });
    

    //配送员标签的鼠标移动效果
    $(document).on('mouseover mouseout', '.postman-item', function(event){
       var id = $(this).attr('id').substr(16);
        if (event.type == 'mouseover') {
            $('#__content' + id).addClass('hover');
            $(this).find('.assign-wrapper').show();
        } else if(event.type == 'mouseout') {
            $('#__content' + id).removeClass('hover');
            $(this).find('.assign-wrapper').hide();
        }
    });
    
    $(document).on('mouseover mouseout', '.deliveryman-marker', function(event){
       var id = $(this).attr('id').substr(9);
        if (event.type == 'mouseover') {
            $(this).addClass('hover');
            $('#deliverymanItem_' + id).find('.assign-wrapper').show();
        } else if(event.type == 'mouseout') {
            $(this).removeClass('hover');
            $('#deliverymanItem_' + id).find('.assign-wrapper').hide();
        }
    });

    //点击改派
    $(document).on('click', '.changeOrder', function(){
        var uid = $(this).data('uid'), supply_id = $(this).data('order_id');
        var html = '';
        for (var i in sendUsers) {
            var item = sendUsers[i];
            if (item.uid != uid) {
                html += '<div class="courier ng-scope" data-uid="' + item.uid + '" data-olduid="' + uid + '" data-supply_id="' + supply_id + '"><span class="ng-binding">' + item.name + '</span>';
                if (item.fetch > 0) {
                    html += '<span class="num ng-binding ng-scope">' + item.fetch + '</span>';
                }
                html += '</div>';
            }
        }
        $('.courier-list').html(html);
        $('.modal-backdrop, .reassign-window').show();
        $('.btn-primary').attr('disabled', true);
    });
    
    //确认改派
    $(document).on('click', '.reassign-window .btn-primary', function(){
        var uid = $('.reassign-window').find('.active').data('uid'), olduid = $('.reassign-window').find('.active').data('olduid');
        var supply_id = $('.reassign-window').find('.active').data('supply_id');
        $.post(url + 'appoint_deliver', {'supply_id':supply_id, 'uid':uid}, function(response){
            if (response.status == 1) {
                $('.modal-backdrop, .reassign-window').hide();
                var tempFetch = parseInt($('#__content' + uid + ' .deliveryman-icon').find('.fetch_' + uid).text());
                var oldtempFetch = parseInt($('#__content' + olduid + ' .deliveryman-icon').find('.fetch_' + olduid).text());
                if (oldtempFetch > 1) {
                    $('.fetch_' + olduid).text(oldtempFetch - 1);
                } else {
                    $('.fetch_' + olduid).text(0);
                }
                $('.fetch_' + uid).text(tempFetch + 1);
                var newUserOrders = [], moveOrder = null;
                $.each(userOrders[olduid], function(i, item){
                    if (item.supply_id != supply_id) {
                        newUserOrders.push(item);
                    } else {
                        moveOrder = item;
                    }
                });
                userOrders[olduid] = newUserOrders;
                sendUsers[olduid].fetch--;
                sendUsers[uid].fetch++;
                if (moveOrder != null) {
                    moveOrder.uid = uid;
                    userOrders[uid].push(moveOrder);
                }
            } else {
                alert(response.info);
            }
        }, 'json')
    });
    //选择配送员
    $(document).on('click', '.courier-list .courier', function(){
        $(this).addClass('active').siblings().removeClass('active');
        $('.btn-primary').attr('disabled', false);
    });
    //点击关闭选择配送员页
    $(document).on('click', '.fa-close, .modal-backdrop', function(){
        $('.modal-backdrop, .reassign-window').hide();
    });
    $(document).on('click', '#sendCount', function(){
        location.href = $(this).data('href') + '&area_id=' + $('#choose_area').val();
    });

    // show_province();

    $(document).on('change', '#choose_area', function(){
        userListFun(1);
//        clearInterval(orderHtmlFunTime);
        clearTimeout(orderHtmlFunTime);
        orderHtmlFun();
//        orderHtmlFunTime = setInterval(orderHtmlFun, 4000);
//        userSendOrderFun();
    });
//    orderHtmlFun();
//    orderHtmlFunTime = setInterval(orderHtmlFun, 4000);
//     setInterval(userSendOrderFun, 5000);
//     setInterval(userListFun, 3000);
    
});

var userListFun = function(move){
    var params = {'province_id':0, 'city_id':0, 'area_id':0};
    if ($('#choose_province').val() == null) {
        params.province_id = $('#choose_pca').attr('province_id');
    } else {
        params.province_id = $('#choose_province').val();
    }
    if ($('#choose_city').val() == null) {
        params.city_id = $('#choose_pca').attr('city_id');
    } else {
        params.city_id = $('#choose_city').val();
    }
    if ($('#choose_area').val() == null) {
        params.area_id = $('#choose_pca').attr('area_id');
    } else {
        params.area_id = $('#choose_area').val();
    }
    $.get(url + 'getData', params, function(response){
        if (response.errcode == false) {
            var html = '', indx = 0;
            if (move != undefined && move == 1) {
                for (var t in sendUsers) {
                    if (labelArray[sendUsers[t].uid] != undefined) {
                        map.removeOverlay(labelArray[sendUsers[t].uid]);
                    }
                }
                labelArray = [];
                for (var up in userPolineArray) map.removeOverlay(userPolineArray[up]);
                for (var us in userSendLabel) map.removeOverlay(userSendLabel[us]);
                for (var uf in userFetchLabel) map.removeOverlay(userFetchLabel[uf]);
                
                for (var p in polineArray) map.removeOverlay(polineArray[p]);
                for (var f in fetchLabel) map.removeOverlay(fetchLabel[f]);
                for (var s in sendLabel) map.removeOverlay(sendLabel[s]);
                userPolineArray = [];//配送员的配送订单的配送线图
                userSendLabel = [];
                userFetchLabel = [];
                sendUsers = [];
                userOrders = [];
                polineArray = [];
                fetchLabel = [];
                sendLabel = [];
                supplyArray = [];
            }
            
            
            if (response.data != null) {
//                html += '<ul>';
                var newSendUsers = [], newLabelArray = [];
                $.each(response.data, function(i, item) {
                    newSendUsers[item.uid] = item;
                    if (sendUsers[item.uid] == undefined) {
//                        sendUsers[item.uid] = item;
                        if (indx == 0) {
                            lng = item.now_lng;
                            lat = item.now_lat;
                        }
                        indx ++;
                        html += '<li id="deliverymanItem_' + item.uid + '" class="postman-item ng-scope">';
                        html += '<p>';
                        html += '<span class="name ng-binding">' + item.name + '</span>';
                        html += '<span class="new-order-count ng-binding ng-hide">+0</span>';
                        html += '</p>';
                        html += '<p class="staff-mobile ng-binding">' + item.phone + '</p>';
                        html += '<div>';
                        html += '<p class="wait-for-fetch">';
                        html += '<span>取：<span class="ng-binding fetch_' + item.uid + '">' + item.fetch + '</span></span>';
                        html += '</p>';
                        html += '<p class="wait-for-send">';
                        html += '<span>送：<span class="ng-binding send_' + item.uid + '">' + item.send + '</span></span>';
                        html += '</p>';
                        html += '</div>';
                        html += '<div class="assign-wrapper">';
                        html += '<p class="name-wrapper">';
                        html += '<span class="name-label ng-binding">' + item.name + '</span>';
                        html += '</p>';
                        html += '<p>';
                        html += '<span class="delivery-detail" data-id="' + item.uid + '"></span>';
                        html += '<span class="assign ng-binding no-motorcycle" data-uid="' + item.uid + '">指派给他</span>';
                        html += '<span class="motorcycle">';
                        html += '<i class="fa fa-motorcycle"></i>';
                        html += '</span>';
                        html += '<span class="location" data-uid="' + item.uid + '">详情</span>';
                        html += '</p>';
                        html += '</div>';
                        html += '<div class="ng-scope"><div class="ng-scope"></div></div>';
                        html += '</li>';
                    } else {
                        $('.fetch_' + item.uid).text(item.fetch);
                        $('.send_' + item.uid).text(item.send);
                    }
                    
                    
                    if (labelArray[item.uid] != undefined) {
                        labelArray[item.uid].setPosition(new BMap.Point(item.now_lng, item.now_lat));
                    } else {
                        var htmlMap = '';
                        htmlMap += '<div class="amap-marker" >';
                        htmlMap += '<div class="amap-marker-content" style="opacity: 1;">';
                        htmlMap += '<div id="__content' + item.uid + '" class="deliveryman-marker improve">';
                        htmlMap += '<div class="deliveryman-icon" data-id="' + item.uid + '" id="__' + item.uid + '">';
                        htmlMap += '<div class="name" data-uid="' + item.uid + '">' + item.name + '</div>';
                        htmlMap += '<div class="display-area" data-uid="' + item.uid + '">';
                        htmlMap += '<div class="text-move-animation" data-uid="' + item.uid + '">';
                        htmlMap += '<span class="wait-for-take wait-for-take-count fetch_' + item.uid + '">' + item.fetch + '</span>';
                        htmlMap += '/';
                        htmlMap += '<span class="wait-for-delivery wait-for-delivery-count send_' + item.uid + '">' + item.send + '</span>';
                        htmlMap += '<div style="text-align: center; font-weight: normal; color: red; margin-top: -3px; height: 30px;">要单</div>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        htmlMap += '<i class="delivery-icon" data-id="' + item.uid + '"></i>';
                        htmlMap += '<span class="angle"></span>';
                        htmlMap += '<span class="b-oval"></span>';
                        htmlMap += '<span class="s-oval"></span>';
                        htmlMap += '</div>';
                        htmlMap += '<div class="deliveryman-icon-click" id="__detail' + item.uid + '">';
                        htmlMap += '<a class="close marker-content-close" href="javascript: void(0)" data-id="' + item.uid + '">×</a>';
                        htmlMap += '<div>' + item.name;
                        htmlMap += '<div class="finished">' + item.phone + '</div>';
                        htmlMap += '<div class="wait-for-take">待取餐：<span class="wait-for-take-count fetch_' + item.uid + '">' + item.fetch + '</span></div>';
                        htmlMap += '<div class="wait-for-delivery">待送达：<span class="wait-for-delivery-count send_' + item.uid + '">' + item.send + '</span></div>';
                        htmlMap += '<div>将选择的<span class="dispatch-order-count">0</span>笔订单</div>';
                        htmlMap += '<div class="button zhipaibutton" data-uid="' + item.uid + '">';
                        htmlMap += '<a class="dispatch-button" data-uid="' + item.uid + '">指派给' + item.name + '</a>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        htmlMap += '</div>';
                        labelArray[item.uid] = new BMap.Label(htmlMap, {position:new BMap.Point(item.now_lng, item.now_lat), offset:new BMap.Size(30, -30)});  // 创建文本标注对象
                        map.addOverlay(labelArray[item.uid]);
                    }
                    
                    newLabelArray[item.uid] = labelArray[item.uid];
                });
//                html += '</ul>';
                for (var uid in sendUsers) {
                    if (newSendUsers[uid] == undefined || newSendUsers[uid] == '' || newSendUsers[uid] == null) {
                        $('#deliverymanItem_' + uid).remove();
                        map.removeOverlay(labelArray[uid]);
                    }
                }
                sendUsers = newSendUsers;
                labelArray = newLabelArray;
            }
            
            if (move != undefined && move == 1) {
                if (lng > 0 && lat > 0) {
                    map.panTo(new BMap.Point(lng, lat), 15);
                }
                
                $('.postman-list ul').remove();
            }
            if ($('.postman-list ul').find('li').size() > 0) {
                $('.postman-list ul').append(html);
            } else {
                $('.postman-list ul').remove();
                $('.postman-list').append('<ul>' + html + '</ul>');
            }
            if ($('#searchUser').val() == '') {
                $('.postman-list').find('.empty-list-label').text('可选骑手(' + response.userCount + ')');
            }
            $('#unGetCount').html('待指派 ( ' + response.unGetCount + ' )');
            $('#sendCount').html('配送中 ( ' + response.sendCount + ' )');
        }
    }, 'json');
}
var userSendOrderFun = function() {
    //加载每个配送员身上的未完成的单子
    var params = {'province_id':0, 'city_id':0, 'area_id':0};
    if ($('#choose_province').val() == null) {
        params.province_id = $('#choose_pca').attr('province_id');
    } else {
        params.province_id = $('#choose_province').val();
    }
    if ($('#choose_city').val() == null) {
        params.city_id = $('#choose_pca').attr('city_id');
    } else {
        params.city_id = $('#choose_city').val();
    }
    if ($('#choose_area').val() == null) {
        params.area_id = $('#choose_pca').attr('area_id');
    } else {
        params.area_id = $('#choose_area').val();
    }
    $.get(url + 'initUserOrders', params, function(response){
        if (response.errcode == false) {
            userOrders = response.data;
        }
    }, 'json');
}
var loading = false;
var orderHtmlFun = function(){
    //待指派的单子
    if (loading) return false;
    loading = true;
    var params = {'type':type, 'province_id':0, 'city_id':0, 'area_id':0};
    if ($('#choose_province').val() == null) {
        params.province_id = $('#choose_pca').attr('province_id');
    } else {
        params.province_id = $('#choose_province').val();
    }
    if ($('#choose_city').val() == null) {
        params.city_id = $('#choose_pca').attr('city_id');
    } else {
        params.city_id = $('#choose_city').val();
    }
    if ($('#choose_area').val() == null) {
        params.area_id = $('#choose_pca').attr('area_id');
    } else {
        params.area_id = $('#choose_area').val();
    }
    $.get(url + 'initOrders', params, function(response){
        if (response.errcode == false) {
            var orderHtml = '', newOrders = [];
            if (response.data != null && response.data.length > 0) {
                $.each(response.data, function(i, item){
                    if ($('#supply_' + item.supply_id).length > 0) {
                        $('#out_order_time_' + item.supply_id).text(item.desk_time + '分钟');
                    } else {
//                    if (supplyArray[item.supply_id] == undefined) {
                        orderHtml += '<div class="order-item ng-scope" id="supply_' + item.supply_id + '" data-supply_id = "' + item.supply_id + '">';
                        orderHtml += '<div class="checked-icon">';
                        orderHtml += '<i class="fa fa-check"></i>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="sign ng-hide"></div>';
                        orderHtml += '<div class="section">';
                        orderHtml += '<div class="wrapper">';
                        orderHtml += '<i class="icon icon-fetch"></i>';
                        orderHtml += '<div class="rst-name ng-binding">' + item.store_name + '</div>';
                        orderHtml += '</div>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="section">';
                        orderHtml += '<div class="wrapper">';
                        orderHtml += '<i class="icon icon-delivery"></i>';
                        orderHtml += '<div class="des-addr ng-binding">' + item.aim_site + '</div>';
                        orderHtml += '</div>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="other-info clearfix">';
                        orderHtml += '<div class="info-item order-number">';
                        orderHtml += '<div class="res-number active ng-binding">' + item.fetch_number + '</div>';
                        orderHtml += '<div class="cooking-time">预计<span class="ng-binding">' + item.order_out_time + '</span>出餐</div>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="info-item order-number ng-hide">';
                        orderHtml += '<div class="res-number inactive ng-binding">#7</div>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="info-item timing">';
                        orderHtml += '<div class="ng-isolate-scope">';
                        orderHtml += '<div class="minutes ng-binding" style="color: #008000" id="out_order_time_' + item.supply_id + '">' + item.desk_time + '分钟</div>';
                        orderHtml += '<div class="hint weak ng-binding">调度时间</div>';
                        orderHtml += '</div>';
                        orderHtml += '</div>';
                        orderHtml += '<div class="info-item detail"><a class="orderDetail" data-order_id="' + item.order_id + '">详情</a></div>';
                        orderHtml += '</div>';
                        orderHtml += '</div>';
//                    } else {
//                        $('#out_order_time_' + item.supply_id).text(item.desk_time + '分钟');
                    }
                    newOrders[item.supply_id] = item;
                });
            }
            if (newOrders.length > 0) {
                supplyArray = newOrders;
                $('.order-list .no-data').remove();
                $('.order-list').append(orderHtml);
            } else {
                supplyArray = [];
                $('.order-list').html('<p class="no-data ng-scope">暂无订单</p>');
            }
            $('.order-tab .assigning-count').text('(' + response.nowCount + ')');
            $('.order-tab .other-count').text('(' + response.otherCount + ')');
        } else {
            supplyArray = [];
            $('.order-list').html('<p class="no-data ng-scope">' + response.msg + '</p>');
            $('.order-tab .assigning-count').text('(0)');
            $('.order-tab .other-count').text('(0)');
            $('#unGetCount').html('待指派 (0)');
        }
        loading = false;
        orderHtmlFunTime = setTimeout(orderHtmlFun, 4000);
    }, 'json');
}

function sendUsersHtml(data, sort)
{
    var html = '<ul>';
    var ii = 0;
    $.each(data, function(i, item){
        if (undefined != item) {
            html += '<li id="deliverymanItem_' + item.uid + '" class="postman-item ng-scope">';
            html += '<p>';
            html += '<span class="name ng-binding">' + item.name + '</span>';
            html += '<span class="new-order-count ng-binding ng-hide">+0</span>';
            html += '</p>';
            html += '<p class="staff-mobile ng-binding">' + item.phone + '</p>';
            html += '<div>';
            html += '<p class="wait-for-fetch">';
            html += '<span>取：<span class="ng-binding fetch_' + item.uid + '">' + item.fetch + '</span></span>';
            html += '</p>';
            html += '<p class="wait-for-send">';
            html += '<span>送：<span class="ng-binding send_' + item.uid + '">' + item.send + '</span></span>';
            html += '</p>';
            html += '</div>';
            html += '<div class="assign-wrapper">';
            html += '<p class="name-wrapper">';
            html += '<span class="name-label ng-binding">' + item.name + '</span>';
            html += '</p>';
            html += '<p>';
            html += '<span class="delivery-detail" data-id="' + item.uid + '"></span>';
            html += '<span class="assign ng-binding no-motorcycle" data-uid="' + item.uid + '">指派给他</span>';
            html += '<span class="motorcycle">';
            html += '<i class="fa fa-motorcycle"></i>';
            html += '</span>';
            html += '<span class="location" data-uid="' + item.uid + '">详情</span>';
            html += '</p>';
            html += '</div>';
            if (ii == 0 && sort == 1) {
                html += '<div class="ng-scope"><div class="ranking ranking ng-scope"></div></div>';
            } else if (ii == 1 && sort == 1) {
                html += '<div class="ng-scope"><div class="ranking ranking1 ng-scope"></div></div>';
            } else if (ii == 2 && sort == 1) {
                html += '<div class="ng-scope"><div class="ranking ranking2 ng-scope"></div></div>';
            } else {
                html += '<div class="ng-scope"><div class="ng-scope"></div></div>';
            }
            html += '</li>';
            ii ++;
        }
    });
    html += '</ul>';
    $('.postman-list ul').remove();
    $('.postman-list').append(html);
    
}


var compare = function (prop) {
    return function (obj1, obj2) {
        var val1 = obj1[prop], val2 = obj2[prop];
        if (val1 < val2) {
            return 1;
        } else if (val1 > val2) {
            return -1;
        } else {
            return 0;
        }
    }
}

//art弹框组件
function artiframe(url, title, width, height, lock, resize, background, button, id, fixeds, closefun, left, top, padding){
    if(url.indexOf("?") != -1){
        url = url+'&frame=1';
    }else{
        url = url+'?frame=1';
    }
    if (!width) width = 'auto';
    if (!height) height = 'auto';
    if (!lock) lock = false;
    if (!resize) resize = false;
    if (!background) background = 'black';
    if (!closefun) closefun = null;
    if (!button) button = null;
    if (!left) left = '50%';
    if (!top) top = '38.2%';
    if (!id) id = null;
    if (!fixeds) fixeds = false;
    if (!padding) padding = 0;
    art.dialog.open(url, {
        init: function(){
            var iframe = this.iframe.contentWindow;
            window.top.art.dialog.data('iframe' + id, iframe);
        },
        id: id,
        title: title,
        padding: padding,
        width: width,
        height: height,
        lock: lock,
        resize: resize,
        background: background,
        button: button,
        fixed: fixeds,
        close: closefun,
        left: left,
        top: top,
        opacity:'0.4'
    });
}


//显示省份
// function show_province(){
//     $.post(areaUrl + 'ajax_province', function(result){
//         result = $.parseJSON(result);
//         if(result.error == 0){
//             if ($('#choose_pca').attr('is_province') == 1) {
//                 var area_dom = '<select id="choose_province" name="province_id" class="select2-choice ui-select-match ng-scope">';
//             } else {
//                 var area_dom = '<select id="choose_province" name="province_id" class="select2-choice ui-select-match ng-scope" style="display:none;">';
//             }
// //            area_dom+= '<option value="0" '+(0==$('#choose_pca').attr('province_id') ? 'selected="selected"' : '')+'>全部省</option>';
//             $.each(result.list,function(i,item){
//                 area_dom += '<option value="'+item.id+'" '+(item.id==$('#choose_pca').attr('province_id') ? 'selected="selected"' : '')+'>'+item.name+'</option>';
//             });
//             area_dom += '</select>';
//
//             $('#choose_pca').prepend(area_dom);
//             show_city($('#choose_province').val(),$('#choose_province').find('option:selected').html(),1);
//             $('#choose_province').change(function(){
//                 show_city($(this).val(), $(this).find('option:selected').html(), 1);
//             });
//         }else if(result.error == 2){
//             var area_dom = '<select id="choose_province" name="province_id" style="display:none;">';
//             area_dom += '<option value="'+result.id+'">'+result.name+'</option>';
//             area_dom += '</select>';
//             $('#choose_pca').prepend(area_dom);
//             show_city(result.id, result.name, 0);
//         }else{
//             art.dialog({
//                 time: 5,
//                 title: '提示信息',
//                 opacity:'0.4',
//                 fixed: true,
//                 resize: false,
//                 content: result.info
//             });
//         }
//     });
// }
//显示城市

function show_city(id, name, type) {
    $.post(areaUrl + 'ajax_city',{id:id, name:name, type:type}, function(result){
        result = $.parseJSON(result);
        if(result.error == 0){
            if ($('#choose_pca').attr('is_city') == 1) {
                var area_dom = '　<select id="choose_city" name="city_id" class="select2-choice ui-select-match ng-scope">';
            } else {
                var area_dom = '　<select id="choose_city" name="city_id" class="select2-choice ui-select-match ng-scope" style="display:none;">';
            }
//            area_dom+= '<option value="0" '+(0==$('#choose_pca').attr('city_id') ? 'selected="selected"' : '')+'>全部市</option>';
            $.each(result.list,function(i,item){
                area_dom += '<option value="'+item.id+'" '+(item.id==$('#choose_pca').attr('city_id') ? 'selected="selected"' : '')+'>'+item.name+'</option>';
            });
            area_dom += '</select>';
            
            if (document.getElementById('choose_city')) {
                $('#choose_city').replaceWith(area_dom);
            } else if(document.getElementById('choose_province')) {
                $('#choose_province').after(area_dom);
            } else {
                $('#choose_pca').prepend(area_dom);
            }
            
            show_area($('#choose_city').val(),$('#choose_city').find('option:selected').html(),1);
            $('#choose_city').change(function(){
                show_area($(this).val(), $(this).find('option:selected').html(), 1);
            });
            
        } else if(result.error == 2) {
            var area_dom = '<select id="choose_city" name="city_id" style="display:none;">';
            area_dom += '<option value="'+result.id+'">'+result.name+'</option>';
            area_dom += '</select>';
            $('#choose_pca').prepend(area_dom);
            show_area(result.id, result.name, 0);
        } else {
            art.dialog({
                time: 5,
                title: '提示信息',
                opacity:'0.4',
                fixed: true,
                resize: false,
                content: result.info
            });
        }
    });
}

//显示区域
function show_area(id, name, type){

    $.post(areaUrl + 'ajax_area',{id:id, name:name, type:type},function(result){
        result = $.parseJSON(result);
        if(result.error == 0){
            if ($('#choose_pca').attr('is_area') == 1) {
                var area_dom = '　<select id="choose_area" name="area_id" class="select2-choice ui-select-match ng-scope" >';
            } else {
                var area_dom = '　<select id="choose_area" name="area_id" class="select2-choice ui-select-match ng-scope" style="display:none;">';
            }
//            area_dom+= '<option value="0" '+(0==$('#choose_pca').attr('area_id') ? 'selected="selected"' : '')+'>全部区</option>';
            $.each(result.list, function(i,item) {
                area_dom += '<option value="'+item.id+'" '+(item.id == $('#choose_pca').attr('area_id') ? 'selected="selected"' : '')+'>'+item.name+'</option>';
            });
            area_dom += '</select>';
            
            if (document.getElementById('choose_area')) {
                $('#choose_area').replaceWith(area_dom);
            } else if(document.getElementById('choose_city')) {
                $('#choose_city').after(area_dom);
            } else {
                $('#choose_pca').prepend(area_dom);
            }
            clearTimeout(orderHtmlFunTime);
            orderHtmlFun();
            userSendOrderFun();
            userListFun();
            
        }else{
            art.dialog({
                time: 5,
                title: '提示信息',
                opacity:'0.4',
                fixed: true,
                resize: false,
                content: result.info
            });
        }
    });
}