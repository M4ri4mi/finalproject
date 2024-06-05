document.addEventListener('DOMContentLoaded', function () {
  console.log('JavaScript is running'); // Debugging line

  var popup = document.getElementById("taskPopup");
  var btn = document.getElementById("addTaskBtn");
  var span = document.getElementsByClassName("close")[0];

  console.log(popup, btn, span); // Debugging: Check if elements are correctly selected

  btn.onclick = function() {
    console.log('Add Task button clicked'); // Debugging: Check if button click is detected
    popup.style.display = "block";
  }

  span.onclick = function() {
    console.log('Close button clicked'); // Debugging: Check if close button click is detected
    popup.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == popup) {
      console.log('Outside click detected'); // Debugging: Check if outside click is detected
      popup.style.display = "none";
    }
  }
});
