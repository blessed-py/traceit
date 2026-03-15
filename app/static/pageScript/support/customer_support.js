        // Data Table Initialization
  $(function () {
    $("#example1").DataTable({
      "responsive": true,
      "lengthChange": false,
      "autoWidth": false,
      "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"]
    }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
  });



    //Delete Support Ticket
    function deleteSupportTicket(ticket) {
        
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
        data = {
      support_ticket_id: ticket
      }

      fetch('/support/delete_support_ticket', {
        method:'POST',
        headers: {
          'Content-Type':'application/json'
        },
        body:JSON.stringify(data)

      }).then(response => response.json()).then(result => {
        if (result.success){
          Swal.fire({
          title: "Deleted!",
          text: result.feedback,
          icon: "success",
          confirmButtonColor: "#3085d6",
          timer: 1500
        }).then(Swal => {
          if (Swal.isDismissed || Swal.isConfirmed){
            window.location.reload();
          }
        })
        } else {
          Swal.fire({
          title: "Error!",
          text: result.feedback,
          icon: "error"
        });
        }
      })
        
       
      } else {
        Swal.fire({
          title: "Alright!",
          text: "Everything is fine!",
          icon: "info",
          confirmButtonColor: "#3085d6",
          timer: 1500
        });
      }
    });
  }

