AV.init({
  appId: "",
  appKey: "",
  serverURL: ""
});

function signup() {

  LC.User.signUp({
    username: $("#inputUsername").val(),
    password: $("#inputPassword").val(),
    email: document.getElementById("inputEmail").value,
    
  }).then(() => {

      AV.User.logIn($("#inputUsername").val(), $("#inputPassword").val()).then(function (loginedUser) {
       
        LC.CLASS("_User")
        .find()
        .then((users) => {
          users.forEach((user) => {
            const username = user.data.username;
            if (username == LC.User.current().data.username) {
              user.setEmail() = $("inputEmail").val();
            }
          });
        })
  
        window.location.href = "./../user-page/user-page.html";
      }, function (error) {
        alert(JSON.stringify(error));
      });


    })
    .catch(({ error }) => alert(error));
}


$(function () {
  $(".form-signup").on("submit", function (e) {
    e.preventDefault();
    signup();
  });
});
