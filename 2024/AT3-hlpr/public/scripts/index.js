welcomebackDiv = document.getElementById("welcomeback");
answersDiv = document.getElementById("answers");
scoreDiv = document.getElementById("score");
questionsDiv = document.getElementById("questions");
console.log(welcomebackDiv.value);
token = getCookie("token");

(async () => {
  const rawResponse = await fetch(`/api/user/profile/${token}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const content = await rawResponse.json();

  // Invalid token: Go to login page
  if (content["valid-token"] === 0) {
    window.location.replace("/login");
  }
  welcomebackDiv.innerText = `welcome back ${content["username"]}`;
  questionsDiv.innerText = `Questions asked: ${content["asked"]}`;
  scoreDiv.innerText = `Score: ${content["score"]}`;
  answersDiv.innerText = `Answers answered: ${content["resposes"]}`;
})();

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return ".";
}
