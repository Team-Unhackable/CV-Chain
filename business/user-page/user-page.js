var type = "";

AV.init({
  appId: "",
  appKey: "",
  serverURL: ""
});

function setupData() {
  $("#welcome").text("Welcome! " + LC.User.current().data.username);
  $("#name").text(LC.User.current().data.username);

  // https://leancloud.cn/docs/leanstorage_guide-js.html#hash860317
  LC.CLASS("_User")
    .include("username", "email", "shortId")
    .find()
    .then((users) => {
      users.forEach((user) => {
        const username = user.data.username;
        const email = user.data.email;
        if (username == LC.User.current().data.username) {
          $("#email").text(email);
        }
      });
    })
     .catch((error) => alert(error.error));

}


function updateType() {
  const query = new AV.Query('_User');
  console.log(AV.User.current());
  query.equalTo('username', AV.User.current().get('username'));
  query.find().then((user) => {
    if (user[0].get('nameOnBlk') != ""){
      
      document.getElementById("type").innerText = user[0].get('companyType'); 
      type = user[0].get('companyType'); 

    }
    else {

    }
  });
}


function logout() {
  LC.User.logOut();
  AV.User.logOut();
  window.location.href = "./../login/login.html";
}

function jump() {
  if (type == "Organization") {
    window.location.href = "./addJob.html";
  }
  else if (type == "School") {
    window.location.href = "./addEdu.html";
  }
  
  
}


$(function () {
  if (LC.User.current()) {
    setupData();
    updateType();
    
  } else {
    window.location.href = "./../login/login.html";
  }
});
