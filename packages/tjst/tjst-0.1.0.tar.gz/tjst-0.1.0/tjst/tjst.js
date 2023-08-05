function tpl2code (tpl){
    var code = ['function (ctx) { with(ctx) { var __p = [];'];
    (tpl + '<%%>').replace(/((?:.|[\r\n])*?)<%((?:.|[\r\n])*?)%>/g, function () {
        var e = arguments[1].replace(/[\\'\r\n]/g, function (x) {
            if (x == '\r') return "\\r";
            if (x == '\n') return "\\n";
            return "\\" + x;
        });
        if (e.length) code.push("__p.push('" + e.replace(/[\r\n]/g) + "');");
        if (arguments[2][0] == '=')
            code.push('__p.push(' + arguments[2].substr(1) + ');');
        else
            code.push(arguments[2] + ' ;');
    });
    code.push("return __p.join('');}}");
    return code.join('');
}

function tpl2func (tpl) {
    return new Function('return ' + tpl2code(tpl))();
}