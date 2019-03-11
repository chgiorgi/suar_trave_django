// Get the button, and when the user clicks on it, execute myFunction

/* myFunction toggles between adding and removing the show class, which is used to hide and show the dropdown content */
function showEditForm(id) {
    document.getElementById(id).classList.toggle("show");
}

function onDelete(id) {
    element = document.getElementById('delete_' + id);
    console.log(element);
    element.submit();
}


// function comment_form() {
//     var x = document.createElement("INPUT");
//     var old= document.getElementById('old_com').innerHTML;
//     x.setAttribute("type", "text");
//     x.setAttribute("value", old);
//     console.log(x ,old);
//     document.body.appendChild(x);
//     document.getElementById('editform').body.appendChild(x)
//
//
// }