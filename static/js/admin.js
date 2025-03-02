// static/js/admin.js

document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById('registerForm');
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const licensee = document.getElementById('licensee').value.trim();
    const license_type = document.getElementById('license_type').value;
    const issue_date = document.getElementById('issue_date').value.trim();
    const expiration_date = document.getElementById('expiration_date').value.trim() || null;
    
    if (!licensee || !license_type || !issue_date) {
      document.getElementById('message').innerHTML = "<p style='color: red;'>Please fill in all required fields.</p>";
      return;
    }
    
    fetch('http://127.0.0.1:5000/register-license', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ licensee, license_type, issue_date, expiration_date })
    })
    .then(response => response.json())
    .then(data => {
      const messageDiv = document.getElementById('message');
      if (data.status === "success") {
        messageDiv.innerHTML = `<p style="color: green;">License registered successfully! License Serial: ${data.license_serial}</p>`;
      } else {
        messageDiv.innerHTML = `<p style="color: red;">Error: ${data.message}</p>`;
      }
    })
    .catch(error => {
      document.getElementById('message').innerHTML = `<p style="color: red;">Error connecting to server.</p>`;
    });
  });
});
