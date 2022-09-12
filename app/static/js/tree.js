// maybe need chenge render func to render and hide childs 1th lewel (doble click effect)
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
        ul.setAttribute('class', 'list-group');
        document.getElementById(id_chief).appendChild(ul);
        for (obj in response_data) {
            renderProductList(response_data[obj]);
        }

        function renderProductList(element) {
            var li = document.createElement('li');
            li.setAttribute('class', 'list-group-item tree');
            li.setAttribute('id', element.id);
            ul.appendChild(li);
            li.innerHTML = li.innerHTML + element.name + ', ' + element.work_position + ', ' + element.date_join + ', ' + element.wage
        }

    });
    $('#renderList').on('click', '.tree', (function () {
        var class_chief = $(this).attr('class');
        var id_chief = $(this).attr('id');
        var chief_el = document.getElementById(id_chief);
        var childs = chief_el.getElementsByClassName('tree');

        if (class_chief.indexOf('childs_rendered') === -1) {
            render_childs(id_chief);
            chief_el.className += ' childs_rendered';
        }
        for (child in childs) {
            if (childs[child].className.indexOf(' hide') === -1) {
                childs[child].className += ' hide'
            } else {
                childs[child].className = childs[child].className.replace(' hide', '')
            }
        }
    }));

    render_childs();
});