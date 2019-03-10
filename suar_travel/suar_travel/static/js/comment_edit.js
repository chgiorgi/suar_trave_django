
// Get the button, and when the user clicks on it, execute myFunction
document.getElementById("editform").onclick = function() {myFunction()};

/* myFunction toggles between adding and removing the show class, which is used to hide and show the dropdown content */
function myFunction() {
    document.getElementById("com_form").classList.toggle("show");
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