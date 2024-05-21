const username = document.getElementById("username");
const password = document.getElementById("password");
const school = document.getElementById("school");

function loginButton() {
  // Post send post request to server :)

  // https://stackoverflow.com/questions/29775797/fetch-post-json-data
  (async () => {
    const rawResponse = await fetch("/api/login", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        school: school.value,
      }),
    });
    const content = await rawResponse.json();

    if (content["success"] === 0) {
      alert(`Could not log in: ${content["error"]}`);
    } else {
      setCookie("token", content["token"], 100000000);
      alert("Successfully Signed in!");
      window.location.replace("/");
    }
  })();
}

// https://www.w3schools.com/js/js_cookies.asp
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
