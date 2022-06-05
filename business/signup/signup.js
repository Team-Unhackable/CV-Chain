AV.init({
  appId: "",
  appKey: "",
  serverURL: ""
});

var companyType = 'School';

function signup() {

  // https://leancloud.cn/docs/leanstorage_guide-js.html#hash885156

  LC.User.signUp({
    username: $("#inputUsername").val(),
    password: $("#inputPassword").val(),
    email: document.getElementById("inputEmail").value,
    
  })
    .then(() => {

      AV.User.logIn($("#inputUsername").val(), $("#inputPassword").val()).then((user) => {
        
        const query = new AV.Query('_User');
        console.log(AV.User.current().get('username'));
        query.equalTo('username', AV.User.current().get('username'));
        query.find().then((user) => {
          if (user.length>0) {
            console.log(companyType);
            user[0].set("companyType",companyType);
            user[0].save();
          }
        });
      }, (error) => {

      });

      var delayInMilliseconds = 2000;

      setTimeout(function() {
        
        console.log(companyType);
        alert("Signup Successfully! Please login...");
        window.location.href = "./../login/login.html";
      }, delayInMilliseconds);

      
    })
    .catch(({ error }) => alert(error));
}



function schoolTag() {
  document.getElementById("inputUsername").placeholder = "School Name";
  companyType = 'School';
}

function orgTag() {
  document.getElementById("inputUsername").setAttribute("placeholder", "Organization Name");
  companyType = 'Organization';
}

$(function () {
  
  $(".form-signup").on("submit", function (e) {
    e.preventDefault();
    
    signup();
  });
});
