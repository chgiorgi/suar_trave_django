


function showEditForm(id) {
    document.getElementById(id).classList.toggle("show");
}

function onDelete(id) {
    element = document.getElementById('delete_' + id);
    console.log(element);
    element.submit();
}
