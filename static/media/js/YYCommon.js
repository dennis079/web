Date.prototype.MyFormat = function (fmt) {
var o = {
"M+": this.getMonth() + 1, //月份
"d+": this.getDate(), //日
"h+": this.getHours(), //小时
"m+": this.getMinutes(), //分
"s+": this.getSeconds(), //秒
"q+": Math.floor((this.getMonth() + 3) / 3), //季度
"S": this.getMilliseconds() //毫秒
};
if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
for (var k in o)
if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
return fmt;
};

function YYCommon()
{
}

YYCommon.prototype = {
    init:function() {
    },
    show: function() {
    }
}

YYCommon.get_alter_type = function(htype)
{
    if( htype == 1 )
    {
        return "自选";
    }
    else if( htype == 2 )
    {
        return "W底策略";
    }
    else if( htype == 3 )
    {
        return "突破策略";
    }
    else if( htype == 4 )
    {
        return "Dual Trust策略";
    }
    else if( htype == 5 )
    {
        return "综合策略1";
    }
    else if( htype == 6 )
    {
        return "综合策略2";
    }
    else if( htype == 7 )
    {
        return "综合策略3";
    }
    else if( htype == 8 )
    {
        return "综合策略4";
    }

    return "未知策略";
}

YYCommon.get_alter_status = function(hstatus)
{
    if( hstatus == 1 )
    {
        return "评估中";
    }
    else if( hstatus == 2 )
    {
        return "评估完成";
    }
    else if( hstatus == 3)
    {
        return "推荐中";
    }
    else if( hstatus == 4 )
    {
        return "平衡中";
    }
    else if( hstatus == 5 )
    {
        return "配置完成";
    }
    else if( hstatus == -2 )
    {
        return "技术止盈关闭";
    }
    else if( hstatus == -3 )
    {
        return "技术止损关闭";
    }
    else if( hstatus == -4 )
    {
        return "评估失败";
    }
    else if( hstatus < 0 )
    {
        return "取消推荐";
    }

    return "未评估";
}

YYCommon.get_alter_est = function(estp)
{
    if( estp == 1 )
    {
        return "盘整";
    }
    else if( estp == 2 )
    {
        return "上升趋势";
    }
    else if( estp == 3 )
    {
        return "下降趋势";
    }
    else if( estp == 4 )
    {
        return "未知趋势";
    }

    return "未评估";
}

YYCommon.get_gold_direct = function(gdirect)
{
    if( gdirect == 1 )
    {
        return "出金";
    }

    return "入金";
}

YYCommon.get_open_policy = function(optype, opvalue, opstyle, opdirect, sbuyprice, ssellprice, opinterval)
{
    opinfo = "开仓类型：";
    if( optype == 0 ) {
        opinfo += "暂不开仓";
    }
    else if( optype == 1 )
    {
        opinfo += "指定份额开仓（1手=100股）<br/>";
        opinfo += "开仓目标份额：" + opvalue.toFixed(2) + "份<br/>";
    }
    else if( optype == 2 )
    {
        opinfo += "指定金额开仓（以万为单位）<br/>";
        opinfo += "开仓目标金额：" + opvalue.toFixed(2) + "万<br/>";
    }
    else if( optype == 3 )
    {
        opinfo += "指定仓位配比开仓（以%为单位）<br/>";
        opinfo += "开仓目标：" + opvalue.toFixed(2) + "%<br/>";
    }
    else if( optype == 4 )
    {
        opinfo += "已清仓<br/>";
    }
    else
    {
        opinfo += "无<br/>";
    }

    if( opdirect == 0 )
    {
        opinfo += "开仓方向：买开<br/>";
        opinfo += "买开价格不高于：" + sbuyprice.toFixed(2) + "<br/>";
    }
    else {
        opinfo += "开仓方向：卖开<br/>";
        opinfo += "卖开价格不高于：" + ssellprice.toFixed(2) + "<br/>";
    }

    if( opstyle <= 0 )
    {
        opinfo += "开仓方式：暂停开仓";
    }
    else if( opstyle == 1 )
    {
        opinfo += "开仓方式：一次性开仓";
    }
    else
    {
        opinfo += "开仓方式：分 " + opstyle + " 次开仓，每两次开仓时间间隔不低于 " + opinterval + " 分钟";
    }

    return opinfo;
}

YYCommon.get_close_policy = function(opdirect, tpstyle, tpvalue, tpprice, tpcount, slstyle, slvalue, slprice, slcount)
{
    info = "止盈策略：";
    if( tpstyle == 0 ) {
        info += "暂不止盈";
    }
    else if( tpstyle == 1 ) {
        info += "盈利且到达最高价格后再次下跌最高价格的 " + tpvalue.toFixed(2) + " %后盈利平仓<br/>";
        if( opdirect == 1 )
        {
            info += "盈利且到达最低价格后再次上升开仓价格的 " + tpvalue.toFixed(2) + " %后止损<br/>";
        }
    }
    else if( tpstyle == 2 ) {
        info += "盈利且到达最高价格后再次下跌 " + tpvalue.toFixed(2) + " 后盈利平仓<br/>";
        if( opdirect == 1 )
        {
            info += "盈利且到达最低价格后再次上升 " + tpvalue.toFixed(2) + " 后止损<br/>";
        }
    }
    else if( tpstyle == 3 ) {
        info += "盈利且价格达到 " + tpprice.toFixed(2) + " 后盈利平仓<br/>";
    }
    else if( tpstyle == 4 ) {
        info += "盈利且价格达到 " + tpprice.toFixed(2) + " 后盈利平仓 " + tpvalue.toFixed(2) + "；价格达到 " + tpcount.tofixed(2) + " 后平仓剩余份额<br/>";
    }
    else if( tpstyle == 5 ) {
        info += "暂不支持！<br/>";
    }
    else {
        info += "暂不支持！<br/>";
    }

    info += "<br/>止损策略：";
    if( slstyle == 0 ) {
        info += "暂不止损";
    }
    else if( slstyle == 1 ) {
        info += "开仓后，价格下跌开仓价格的 " + slvalue.toFixed(2) + " %后止损平仓<br/>";
        if( opdirect == 1 )
        {
            info += "开仓后，价格上升开仓价格的 " + slvalue.toFixed(2) + " %后止损平仓<br/>";
        }
    }
    else if( slstyle == 2 ) {
        info += "开仓后，价格下跌 " + slvalue.toFixed(2) + " 后止损平仓<br/>";
        if( opdirect == 1 )
        {
            info += "开仓后，价格上升 " + slvalue.toFixed(2) + " 后止损平仓<br/>";
        }
    }
    else if( slstyle == 3 ) {
        info += "到达最高价格后再次下跌最高价格的 " + slvalue.toFixed(2) + " %后盈利平仓<br/>";
        if( opdirect == 1 )
        {
            info += "到达最低价格后再次上升开仓价格的 " + slvalue.toFixed(2) + " %后止损<br/>";
        }
    }
    else if( slstyle == 4 ) {
        info += "到达最高价格后再次下跌 " + slvalue.toFixed(2) + " 后盈利平仓<br/>";
        if( opdirect == 1 )
        {
            info += "到达最低价格后再次上升 " + slvalue.toFixed(2) + " 后止损<br/>";
        }
    }
    else if( slstyle == 5 ) {
        info += "不止损，亏损到达上次开仓价格的 " + slvalue.toFixed(2) + "%再次开同向仓 " + slprice.toFixed(0) + "份额，但不能超过" + slcount + "次";
    }
    else {
        info += "暂不支持！<br/>";
    }

    return info;
}

YYCommon.get_trade_param_name = function(ptype)
{
    pname = "";
    if( ptype == 1 ) {
        pname = "资金池保留余额";
    }
    else if( ptype == 2 ) {
        pname = "资金池保留空仓";
    }
    else if( ptype == 3 ) {
        pname = "止盈清盘阈值";
    }
    else if( ptype == 4 ) {
        pname = "止损清盘阈值";
    }
    else if( ptype == 5 ) {
        pname = "允许损失资金阈值";
    }
    else if( ptype == 6 ) {
        pname = "稳定资金阈值";
    }
    else if( ptype == 7 ) {
        pname = "激进资金阈值";
    }
    else if( ptype == 8 ) {
        pname = "单只标的最大仓位占比";
    }
    else if( ptype == 9 ) {
        pname = "总仓位控制策略";
    }
    else if( ptype == 10 ) {
        pname = "操盘风格策略";
    }
    else if( ptype == 11 ) {
        pname = "优先配置策略";
    }
    else if( ptype == 12 ) {
        pname = "优先平仓策略";
    }
    else if( ptype == 13 ) {
        pname = "操作计划——总体计划";
    }
    else if( ptype == 14 ) {
        pname = "操作计划——投资标的";
    }
    else if( ptype == 15 ) {
        pname = "操作计划——资金配置计划";
    }
    else if( ptype == 16 ) {
        pname = "操作计划——仓位管理计划";
    }
    else if( ptype == 17 ) {
        pname = "操作计划——风险管理计划";
    }
    else if( ptype == 18 ) {
        pname = "操作计划——时间管理计划";
    }
    else if( ptype == 19 ) {
        pname = "操作计划——资源管理计划";
    }
    else if( ptype == 20 ) {
        pname = "操作计划——现金流计划";
    }
    else if( ptype == 21 ) {
        pname = "操作计划——退出计划";
    }
    else if( ptype == 22 ) {
        pname = "操作计划——干系人计划";
    }
    else {
        pname = "未知参数";
    }

    return pname;
}
