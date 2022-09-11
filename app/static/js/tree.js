$(document).ready(function () {

    var return_childs = (function (id_chief) {
        var tmp = null;
        $.ajax({
            'async': false,
            'type': "GET",
            'dataType': 'json',
            'url': "/api/get_employeers",
            'data': {'id_chief': id_chief},
            'success': function (data) {
                tmp = data;
            }
        });
        return tmp.data;
    });


    var render_childs = (function (id_chief) {
        if (!((id_chief !== undefined) && (id_chief !== null) && (id_chief !== ""))) {
            id_chief = 'renderList'
        }
        // get names of boss
        var response_data = return_childs(id_chief);
        // Do stuff after everything has been loaded
        var ul = document.createElement('ul');
        ul.setAttribute('id', 'chiefs');

        document.getElementById(id_chief).appendChild(ul);
        for (obj in response_data) {
            renderProductList(response_data[obj]);
        }

        function renderProductList(element) {
            var li = document.createElement('li');
            li.setAttribute('class', 'tree close');
            li.setAttribute('id', element.id);
            ul.appendChild(li);
            li.innerHTML = li.innerHTML + element.name;
        }

    });
    $('#renderList').on('click', '.open', (function () {
        // var id = $(this).attr('id');
        // render_childs(id)
    }));

    $('#renderList').on('click', '.close', (function () {

        var id = $(this).attr('id');
        render_childs(id)

        // var id = $(this).attr('id');
        // var childs = return_childs(id)
        // for (child in childs) {
        //     console.log(childs)
        // }
        this.className = this.className.replace('close', 'open')
    }));
    render_childs();
});

// var ul = document.querySelectorAll('.treeCSS > li:not(:only-child) ul, .treeCSS ul ul');
// for (var i = 0; i < ul.length; i++) {
//     var div = document.createElement('div');
//     div.className = 'drop';
//     div.innerHTML = '+'; // картинки лучше выравниваются, т.к. символы на одном браузере ровно выглядят, на другом — чуть съезжают
//     ul[i].parentNode.insertBefore(div, ul[i].previousSibling);
//     div.onclick = function () {
//         this.innerHTML = (this.innerHTML == '+' ? '−' : '+');
//         this.className = (this.className == 'drop' ? 'drop dropM' : 'drop');
//     };
//     document.appendChild(div);
//
// }
;