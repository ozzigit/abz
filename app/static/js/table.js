let table
$(document).ready(function () {
    table = $('#data').DataTable({
        ajax: '/api/data',
        serverSide: true,
        columns: [
            {data: 'name',},
            {data: 'work_position'},
            {data: 'date_join'},
            {data: 'wage'},
            {data: 'chief_name'}
        ],
    });
});
$('#data').on('click', 'tbody td', function () {
    //get textContent of the TD
    const row = table.row(this).data();
    const text_pushed = this.textContent;
    if (row.chief_name == text_pushed) {
        window.location.href = "/person/" + row.chief_id;
    } else {
        window.location.href = "/person/" + row.id;
    }
});
