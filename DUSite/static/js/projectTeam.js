$(function () {
    var cur_page = document.getElementById('cur-page');
    cur_page.setAttribute('value', '1');
    $.ajax({
        type: "POST",
        url: "post_tol_page/",
        success: function (data) {
            var tol_page = document.getElementById('tol-page');
            tol_page.setAttribute('value', data.tol_page);
            initPagination(data.tol_page);
            jump(1);
        }
    });

});

function initPagination() {
    var page=parseInt(document.getElementById('tol-page').value);
    var cur_page = parseInt(document.getElementById('cur-page').value);
    var pagination = document.getElementById('pagination');
    if (page <= 5) {
        pagination.innerHTML = '<li><a class=\'page-link\' onclick="jump(\'-\')">«</a></li>';
        for (var i = 1; i <= page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' onclick=\"jump('" + i + "')\">" + i + "</a></li>";
            else
                pagination.innerHTML += "<li><a class=\"page-link active\">" + i + "</a></li>";
        }
        pagination.innerHTML += '<li><a class=\'page-link\' onclick="jump(\'+\')">»</a></li>';
    }
    else {
        pagination.innerHTML = '<li><a class=\'page-link\' onclick="jump(\'-\')">«</a></li>';
        if (cur_page !== 1)
            pagination.innerHTML += "……";
        for (var i = 1; i < cur_page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' style='display:none'>" + i + "</a></li>";
        }
        for (var i = cur_page; i < cur_page + 5 && i <= page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' onclick=\"jump('" + i + "')\">" + i + "</a></li>";
            else
                pagination.innerHTML += "<li><a class=\"page-link active\">" + i + "</a></li>";
        }
        if (cur_page + 5 <= page)
            pagination.innerHTML += "……";
        pagination.innerHTML += '<li><a class=\'page-link\' onclick="jump(\'+\')">»</a></li>';
    }
}

function jump(page) {
    var jump_to = page;
    var cur_page = document.getElementById('cur-page');
    if (page === '-') {
        jump_to = cur_page.value - 1;
        if (jump_to < 1)
            return;
    }
    if (page === '+') {
        jump_to = document.getElementById('cur-page').value + 1;
        if (jump_to > document.getElementById('tol-page').value)
            return
    }
    $.ajax({
        type: "POST",
        url: "post_blog_ajax/",
        data: {
            "page": jump_to
        },
        success: function (result) {
            var blog = document.getElementsByClassName("group-blog")
            for (var i = 0; i < blog.length; i++) {
                blog[i].setAttribute("style", "display:none");
            }
            for (var i = 0; i < result.length; i++) {
                blog[i].setAttribute("style", "");
                blog[i].getElementsByClassName("msg").item(0).innerHTML = result[i].month + '-' + result[i].day;
                blog[i].getElementsByClassName("msg").item(1).innerHTML = result[i].year;
                blog[i].getElementsByClassName("msg").item(2).innerHTML = result[i].name;
                blog[i].getElementsByClassName("intro").item(0).innerHTML = result[i].content;
                blog[i].getElementsByClassName("edit").item(0).setAttribute('onclick', "alertInfoWithJump2('你确定删除这篇日志吗？','delete/article=" + result[i].id + "/')");
                blog[i].getElementsByClassName("edit").item(1).setAttribute('onclick', "window.location.href='article=" + result[i].id + "/'");
            }
        }
    });
    var pagination = document.getElementById('pagination');
    var old_l = pagination.getElementsByClassName('page-link').item(cur_page.value);
    old_l.removeAttribute('class');
    old_l.setAttribute('class', 'page-link');
    old_l.setAttribute('onclick', "jump('" + cur_page.value + "')");
    var cur_l = pagination.getElementsByClassName('page-link').item(jump_to);
    cur_l.setAttribute('class', 'page-link active');
    cur_page.setAttribute('value', jump_to);
    //document.getElementById('ul-nav').getElementsByTagName('li').item(1).getElementsByTagName('a').item(0).click();
    initPagination();
}