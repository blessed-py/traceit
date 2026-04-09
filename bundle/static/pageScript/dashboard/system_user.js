    //Data Table Initialization
$(function () {
    $("#example1").DataTable({
      "responsive": true,
      "lengthChange": false,
      "autoWidth": false,
      "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"]
    }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
  });


    //Add System User
document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("addUserForm");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirm_password");
  const passwordError = document.getElementById("passwordError");

  // 🔐 Live password match check
  function validatePasswords() {
    if (password.value !== confirmPassword.value) {
      confirmPassword.classList.add("is-invalid");
      passwordError.style.display = "block";
      return false;
    } else {
      confirmPassword.classList.remove("is-invalid");
      passwordError.style.display = "none";
      return true;
    }
  }

  password.addEventListener("input", validatePasswords);
  confirmPassword.addEventListener("input", validatePasswords);

  // 🚀 Submit form
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!validatePasswords()) {
      Swal.fire({
        title: "Error!",
        text: "Passwords do not match",
        icon: "error",
        confirmButtonColor: "#3085d6",
      });
      return;
    }

    const formData = new FormData(form);

    fetch("/sys/add_user", {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(result => {

      if (result.success) {
        Swal.fire({
          title: "Success!",
          text: result.message,
          icon: "success",
          confirmButtonColor: "#3085d6",
          timer: 1500
        }).then(Swal => {
          if (Swal.isConfirmed || Swal.isDismissed) {
            $("#addUser").modal("hide");
            form.reset();
            $("#user_role").val("").trigger("change");
            window.location.reload();
          }
        });

      } else {
        Swal.fire({
          title: "Error!",
          text: result.message,
          icon: "error",
          confirmButtonColor: "#3085d6",
        });
      }
    })
    .catch(() => {
      Swal.fire({
        title: "Error!",
        text: "Something went wrong. Please try again.",
        icon: "error",
        confirmButtonColor: "#3085d6",
      });
    });
  });

});

    //Delete System User
function deleteUser(user_id) {

  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!"
  }).then((result) => {

    if (result.isConfirmed) {

      const data = {
        user_id: user_id
      };

      fetch("/sys/delete_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {

        if (result.success) {
          Swal.fire({
            title: "Deleted!",
            text: result.message,
            icon: "success",
            confirmButtonColor: "#3085d6",
            timer: 1500
          }).then(Swal => {
            if (Swal.isDismissed || Swal.isConfirmed) {
              window.location.reload();
            }
          });

        } else {
          Swal.fire({
            title: "Error!",
            text: result.message,
            icon: "error",
            confirmButtonColor: "#3085d6",
          });
        }

      });

    } else {
      Swal.fire({
        title: "Alright!",
        text: "Everything is fine!",
        icon: "info",
        timer: 1500
      });
    }

  });
}    