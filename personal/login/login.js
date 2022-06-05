AV.init({
  appId: "",
  appKey: "",
  serverURL: ""
});

function login() {
  const username = $("#inputUsername").val();
  const password = $("#inputPassword").val();

  // https://leancloud.cn/docs/leanstorage_guide-js.html#hash964666

  AV.User.logIn(username, password).then(function () {

  }, function (error) {
  });

  LC.User.login(username, password)
    .then(() => {
      window.location.href = "./../user-page/user-page.html";
    })
    .catch(({ error }) => alert(error));
}


$(function () {
  $(".form-signin").on("submit", function (e) {
    e.preventDefault();
    login();
  });
});
