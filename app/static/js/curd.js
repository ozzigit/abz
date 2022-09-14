// in form elments have no element select_with_search
// this script adds options to the select tag from query with a keyword from input apper

function list_of_names(part_of_name) {
    let tmp = null;
    $.ajax({
        'async': false,
        'type': "GET",
        'dataType': 'json',
        'url': "/api/get_list_by_filter_names",
        'data': {'name': part_of_name},
        'success': function (data) {
            tmp = data;
        }
    });
    return tmp.data;
}

function render_options(data) {

    var elem_in_listresult = []
    for (res in data) {
        elem_in_listresult.push(data[res].name + '_' + data[res].date_join);
    }
    console.log(elem_in_listresult)
    $("#chief_name").empty()
    let select_list = document.getElementById('chief_name')
    for (elem in elem_in_listresult) {
        renderSelectElem(elem_in_listresult[elem])
    }

    function renderSelectElem(elem) {
        let option = document.createElement('option');
        option.text = elem;
        option.setAttribute('value', elem);
        select_list.appendChild(option);
    }
}

$(document).ready(function () {
    $('#chief_part_name').on('input', async function () {
        let search = this.value;
        if (search.length >= 5) {
            if ((search !== undefined) && (search !== null) && (search !== "")) {
                let result = list_of_names(search);
                render_options(result);

            }
        }
    });
});

