document.addEventListener('DOMContentLoaded', () => {
  const passwordInput = document.getElementById('passwordInput');
  const toggleIcon = document.getElementById('togglePassword');

  toggleIcon.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Toggle icon class
    toggleIcon.classList.toggle('fa-eye');
    toggleIcon.classList.toggle('fa-eye-slash');
  });
});


var login_form = document.getElementById('login_form')
login_form.addEventListener('submit', function(event) {
  event.preventDefault()
  formData = new FormData(login_form)
  fetch('/sys/login/authenticate', {
    method: 'POST',
    body:formData
  }).then(response => {
    if (!response.ok) {
      console.error('Network response was not ok')
    }
    return response.json()
  }).then(login => {
    if (login.success) {
      window.location.reload()
    }else{
      document.getElementById('login-status').innerText = login.feedback
    }
  })
})

      