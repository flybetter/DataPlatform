$(function () {
    var chartSan;
    var chartBing;
    var map;
    var initInfo;
    var sorted_key = '1';
    var zIndex = 10;
    // initArray();

    $("#dialog").dialog({
        autoOpen: false,
        width: 400,
        buttons: [
            {
                text: "Ok",
                click: function () {
                    $(this).dialog("close");
                }
            }
        ]
    });

    // $("#dialog").dialog("open");


    // 初始化数据
    $.ajax({
        url: '/v1/houses/api',
        method: 'GET',
        data: {
            phone: phone,
            city: city,
            days: '30',
            secret_key: secret_key,
            sorted_key: '0'
        },
        success: function (resp) {
            if (resp.result) {
                renderResp(resp);
            } else {
                $('#dialog p').html(resp.msg);
                $("#dialog").dialog("open");
            }

        }
    })

    function renderResp(json) {
        // 准备数据开始
        if (flag) {
            city = $('#changeCity').val()
        }
        var newhouses = JSON.parse(json.data.newhouses);
        var data = json.data;
        var sortednewhouses = newhouses.slice().sort(function (a, b) {
            return b.COUNT - a.COUNT;
        });
        var bing10house = [];
        for (var i = 0; i < 10 && i < sortednewhouses.length; i++) {
            bing10house.push({
                name: sortednewhouses[i].PRJ_ITEMNAME,
                y: sortednewhouses[i].COUNT
            });
        }
        var newhouses_scatter_diagram = JSON.parse(json.data.newhouses_scatter_diagram);
        var now = new Date();
        var maxday = $('#changeDay').val();
        for (var index = 0; index < newhouses_scatter_diagram.length; index++) {
            var ttime = new Date(newhouses_scatter_diagram[index].START_TIME);
            var day = parseInt(Math.abs(now - ttime) / 1000 / 60 / 60 / 24)
            newhouses_scatter_diagram[index] = [
                maxday - day ,
                parseFloat(newhouses_scatter_diagram[index].PIC_HX_TOTALPRICE)
            ];
        }
        // 准备数据结束

        // 渲染开始

        // 渲染select表单以及访问详情数据
        var optionHtml = '';
        for (var j = 0; j < data.cities.length; j++) {
            optionHtml = optionHtml + '<option value="' + data.cities[j] + '">' + data.cities[j] + '</option>';
        }
        $('#changeCity').html(optionHtml);
        $('#changeCity').val(city);
        $('.p-title .count').html(data.count);

        renderDetailLi(newhouses);

        // 渲染数据轨迹里面的用户信息
        $('.user-info').html('');
        if (data.phone_show) {
            $('.user-info').append('<div class="info-item"><span class="label">用户：</span><span class="content">' + data.phone_show + '</span></div>')
        }
        if (data.sex) {
            var tempstr = data.sex == 1 ? '男' : '女';
            $('.user-info').append('<div class="info-item"><span class="label">性别：</span><span class="content">' + tempstr + '</span></div>')
        }
        if (data.age) {
            $('.user-info').append('<div class="info-item"><span class="label">年龄：</span><span class="content">' + data.age + '</span></div>')
        }
        if (true) {
            var title = '总次数 = 总价浏览次数 + 均价 & 面积的次数（备注：总次数即为“有总价”或者“均价和面积都有”）\n总价 = (总价求和 + 均价 * 面积) / 总次数';
            ;
            var tempStr = '';
            if (data.sum_price) {
                tempStr = Math.ceil(data.sum_price) + '万';
            }
            $('.user-info').append('<div class="info-item" title="' + title + '"><span class="label">意向总价：</span><span class="content">' + tempStr + '</span></div>')
        }
        if (true) {
            var title = '面积 = 总价 / 均价';
            var tempStr = '';
            if (data.area) {
                tempStr = Math.ceil(data.area) + '平方';
            }
            $('.user-info').append('<div class="info-item" title="' + title + '"><span class="label">意向面积：</span><span class="content">' + tempStr + '</span></div>')
        }
        if (true) {
            var title = '户型 = 户型求和 / 次数';
            var tempStr = '';
            if (data.bedroom) {
                tempStr = Math.ceil(data.bedroom) + '室';
            }
            $('.user-info').append('<div class="info-item" title="' + title + '"><span class="label">意向户型：</span><span class="content">' + tempStr + '</span></div>')
        }
        if (true) {
            var title = '均价 = 均价求和 / 均价次数（备注：此处均价次数是有均价的次数和）';
            var tempStr = '';
            if (data.avg_price) {
                tempStr = Math.ceil(data.avg_price) + '元/平米';
            }
            $('.user-info').append('<div class="info-item" title="' + title + '"><span class="label">意向均价：</span><span class="content">' + tempStr + '</span></div>')
        }
        // 渲染散点图
        if (chartSan) {
            if (maxday == 7) {
                temptickAmount = 8;
                temptickInterval = 1;
            } else {
                temptickAmount = 7;
                temptickInterval = 5;
            }
            chartSan.update({
                xAxis: [{
                    max: maxday,
                    tickAmount: temptickAmount,
                    tickInterval: temptickInterval
                }],
                series: [{
                    data: newhouses_scatter_diagram
                }]
            })
        } else {
            chartSan = Highcharts.chart('diantu', {
                chart: {
                    type: 'scatter',
                    zoomType: 'xy',
                    backgroundColor: '#f3f3f3'
                },
                title: {
                    text: null
                },
                credits: {
                    enabled: false
                },
                xAxis: [{
                    title: {
                        enabled: false
                    },
                    lineWidth: 1,
                    //eaeaea
                    gridLineColor: '#eaeaea',
                    gridLineWidth: 1,
                    lineColor: '#c3c3c3',
                    max: maxday,
                    min: 0,
                    // startOnTick: false,
                    tickAmount: 7,
                    tickInterval: 5
                }],
                yAxis: [{
                    title: {
                        enabled: false
                    },
                    lineWidth: 1,
                    //eaeaea
                    gridLineColor: '#eaeaea',
                    gridLineWidth: 1,
                    lineColor: '#c3c3c3'
                }],
                legend: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        marker: {
                            radius: 3
                        }
                    },
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: 'rgb(100,100,100)'
                                }
                            }
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false
                                }
                            }
                        },
                        tooltip: {
                             headerFormat: null,
                            pointFormat: '第{point.x}天,总价：{point.y} 万元'
                        }
                    }
                },
                series: [{
                    // name: '女',
                    color: '#ce5858',
                    data: newhouses_scatter_diagram
                }]
            });
        }

        // 渲染饼图
        if (chartBing) {
            chartBing.update({
                series: [{
                    data: bing10house
                }]
            })
        } else {
            chartBing = Highcharts.chart('bingtu', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    backgroundColor: '#f3f3f3',
                    type: 'pie'
                },
                title: {
                    text: null
                },
                credits: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        size: 160,
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
                                fontWeight: 'normal',
                                fontSize: '8px'
                            }
                        }
                    }
                },
                series: [{
                    dataLabels: {
                        distance: 5
                    },
                    name: '占比',
                    colorByPoint: true,
                    data: bing10house
                }]
            });
        }

        // 渲染地图
        if (map) {
            map.clearOverlays();
        } else {
            // 创建地图实例
            var map = new BMap.Map("mapContainer");
            // 创建点坐标
            map.centerAndZoom(city);
            map.enableScrollWheelZoom(true);
            map.addControl(new BMap.NavigationControl());
            map.addControl(new BMap.ScaleControl());

        }
        for (var index = 0; index < newhouses.length; index++) {
            var poi = newhouses[index];
            // 创建点坐标
            var point = new BMap.Point(poi.B_LNG, poi.B_LAT);
            // 创建标注
            var marker = new BMap.Marker(point);
            if (poi.COUNT < 6) {
                var myIcon = new BMap.Icon("../../../static/images/circle.png", new BMap.Size(25, 25));
            } else if (poi.COUNT < 21) {
                var myIcon = new BMap.Icon("../../../static/images/circle-middle.png", new BMap.Size(36, 36));
            } else {
                var myIcon = new BMap.Icon("../../../static/images/circle-big.png", new BMap.Size(50, 50));
            }
            var marker = new BMap.Marker(point, {
                icon: myIcon
            });

            // 将标注添加到地图中
            map.addOverlay(marker);
            // 设置覆盖物的文字标签


            var label = new BMap.Label(poi.PRJ_ITEMNAME, {
                offset: new BMap.Size(0, -30)
            });
            label.setStyle({
                background: "#fff",
                padding: "5px 10px",
                textAlign: "center",
                top: "-20px",
                border: "none",
                boxShadow: "0 0 10px #aaa",
                borderRadius: "3px",
                fontWeight: "bold"
            });
            label.addEventListener('click',function(e){
                $(e.domEvent.target).parent().css('zIndex',zIndex)
                zIndex ++;
            })

            marker.setLabel(label);

        }

        $(".panel-1-wrap").niceScroll({
            cursorcolor: "#ccc"
        });

        // 渲染结束
    }

    // 绑定事件
    $('.selectChange').change(function () {
        var city = $('#changeCity').val();
        var days = $('#changeDay').val();
        $.ajax({
            url: '/v1/houses/api',
            method: 'GET',
            data: {
                phone: phone,
                city: city,
                days: days,
                secret_key: secret_key,
                sorted_key: sorted_key
            },
            success: function (resp) {
                if (resp.result) {
                    renderResp(resp, true);
                } else {
                    $('#dialog p').html(resp.msg);
                    $("#dialog").dialog("open");
                }
            }
        })
    })

    function renderDetailLi(newhouses) {
        var historyHtml = '';
        for (var k = 0; k < newhouses.length; k++) {
            if (newhouses[k].COUNT > 10) {
                historyHtml += '<li class="bold">';
            } else {
                historyHtml += '<li>';
            }
            historyHtml += '<div class="line1">';
            historyHtml += '<div class="left">' + FormatDate(newhouses[k].START_TIME) + '</div>';
            historyHtml += '<div class="right">' + newhouses[k].COUNT + '次</div>';
            historyHtml += '</div>';
            historyHtml += '<div class="line2">';
            historyHtml += '<div class="left">' + newhouses[k].PRJ_ITEMNAME + '</div>';
            var price = newhouses[k].PRICE_SHOW || '未知';
            historyHtml += '<div class="right">' + price + '</div>';
            historyHtml += '</div>';
            historyHtml += '</li>';
        }
        $('#history-map-div').html(historyHtml);
    }

    // tab切换
    $('.newpanel .tab').click(function () {
        var index = $('.newpanel .tab').index(this);
        $('.newpanel .tab').eq(index).addClass('active');
        $('.newpanel .tab').eq(1 - index).removeClass('active');
        $('.newpanel .panel-item').eq(index).show();
        $('.newpanel .panel-item').eq(1 - index).hide();
        $("#history-map-div").height('95%');
        $("#history-map-div").niceScroll({
            cursorcolor: "#ccc"
        });
    })

    // 排序
    $('.filter .ub-f1').click(function () {
        var intA = 0, intB = 0
        $('.filter .ub-f1').removeClass('active');
        // $('.filter .ub-f1').removeClass('up');
        $(this).addClass('active');
        if ($(this).hasClass('up')) {
            $(this).removeClass('up');
            if ($(this).hasClass('time')) {
                sorted_key = 2
            } else {
                sorted_key = 0
            }
        } else {
            $(this).addClass('up');
            if ($(this).hasClass('time')) {
                sorted_key = 3
            } else {
                sorted_key = 1
            }
        }

        var city = $('#changeCity').val();
        var days = $('#changeDay').val();
        $.ajax({
            url: '/v1/houses/api',
            method: 'GET',
            data: {
                phone: phone,
                city: city,
                days: days,
                secret_key: secret_key,
                sorted_key: sorted_key
            },
            success: function (resp) {
                if (resp.result) {
                    var newhouses = JSON.parse(resp.data.newhouses);
                    renderDetailLi(newhouses)
                } else {
                    $('#dialog p').html(resp.msg);
                    $("#dialog").dialog("open");
                }
            }
        })
    })
});


// var href = window.location.href,
//     url = window.location.pathname,
//     hostname = window.location.hostname,
//     protocol = window.location.protocol,
//     port = window.location.port;
// url = decodeURI(url);
// urlleft = url.substring(0, url.lastIndexOf("/"));
// day = url.substring(url.lastIndexOf("/") + 1);
// urlphone = urlleft.substring(0, urlleft.lastIndexOf("/"));
// city = urlleft.substring(urlleft.lastIndexOf("/") + 1);
// href = decodeURI(href);
// arrObj = href.substring(href.lastIndexOf("&&") + 2);
// arrObj = arrObj.split("=");
// filter = arrObj[1];
// commonurl = protocol + "//" + hostname + ":" + port + urlphone + "/";

function FormatDate(strTime) {
    // strTime = strTime - 28800000;
    var date = new Date(strTime);
    return date.getFullYear() + "-" + plusZero(date.getMonth() + 1) + "-" + plusZero(date.getDate()) + " " + plusZero(date.getHours()) + ":" + plusZero(date.getMinutes()) + ":" + plusZero(date.getSeconds());
}

function plusZero(int) {
    if (int <= 9) {
        int = '0' + int;
    }
    return '' + int;
}
