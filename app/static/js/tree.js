$(document).ready(function () {
    var return_first = (function () {
        var tmp = null;
        $.ajax({
            'async': false,
            'type': "GET",
            'dataType': 'json',
            'url': "/api/get_employeers",
            'data': {text: "text"},
            'success': function (data) {
                tmp = data;
            }
        });
        return tmp.data;
    });
    // get names of boss
    var response_data = return_first();
    // Do stuff after everything has been loaded
    var ul = document.createElement('ul');
    ul.setAttribute('id', 'chiefs');


    document.getElementById('renderList').appendChild(ul);
    for (obj in response_data) {
        renderProductList(response_data[obj]);
    }


    function renderProductList(element) {
        var li = document.createElement('li');
        li.setAttribute('class', 'item');
        li.setAttribute('id', element.id);
        ul.appendChild(li);
        li.innerHTML = li.innerHTML + element.name;
    }
});
var ul = document.querySelectorAll('.treeCSS > li:not(:only-child) ul, .treeCSS ul ul');
for (var i = 0; i < ul.length; i++) {
    var div = document.createElement('div');
    div.className = 'drop';
    div.innerHTML = '+'; // картинки лучше выравниваются, т.к. символы на одном браузере ровно выглядят, на другом — чуть съезжают
    ul[i].parentNode.insertBefore(div, ul[i].previousSibling);
    div.onclick = function () {
        this.innerHTML = (this.innerHTML == '+' ? '−' : '+');
        this.className = (this.className == 'drop' ? 'drop dropM' : 'drop');
    };
    document.appendChild(div);

}
;