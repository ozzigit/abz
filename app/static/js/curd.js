// in form elments have no element select_with_search
// this script adds options to the select tag from query with a keyword from input apper
$(document).ready(function () {
    var list_of_names = (function (part_of_name) {
        var tmp = null;
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
    });
    $('#chief_part_name').on('input', function () {
        var search = this.value;
        if (search.length >= 5) {
            if ((search !== undefined) && (search !== null) && (search !== "")) {
                var result = list_of_names(search);
                var elem_in_listresult = []
                for (res in result) {
                    elem_in_listresult.push(result[res].name + '_' + result[res].date_join);
                }
                console.log(elem_in_listresult)
                $("#chief_name").empty()
                var select_list = document.getElementById('chief_name')
                for (elem in elem_in_listresult) {
                    renderSelectElem(elem_in_listresult[elem])
                }

                function renderSelectElem(elem) {
                    var option = document.createElement('option');
                    option.text = elem;
                    option.setAttribute('value', elem);
                    select_list.appendChild(option);
                }

            }
        }
    });
});

