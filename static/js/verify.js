// static/js/verify.js

function verifyLicense() {
  const licenseSerial = document.getElementById("licenseSerial").value.trim();
  if (!licenseSerial) {
    document.getElementById("result").innerHTML = "<p style='color: red;'>Please enter a license serial.</p>";
    return;
  }
  
  fetch(`http://127.0.0.1:5000/verify/${licenseSerial}`)
    .then(response => response.json())
    .then(data => {
      if (data.status === "valid") {
        document.getElementById("result").innerHTML = `
          <p style="color: green;">
            ✅ License is valid!<br>
            License Serial: ${data.license_serial}<br>
            Licensee: ${data.licensee}<br>
            License Type: ${data.license_type}<br>
            License Status: ${data.license_status}<br>
            Issued Date: ${data.issue_date}<br>
            Expiration Date: ${data.expiration_date}
          </p>`;
      } else {
        document.getElementById("result").innerHTML = `<p style="color: red;">❌ ${data.message}</p>`;
      }
    })
    .catch(error => {
      console.error("Error:", error);
      document.getElementById("result").innerHTML = `<p style="color: red;">⚠️ Error connecting to server.</p>`;
    });
}
