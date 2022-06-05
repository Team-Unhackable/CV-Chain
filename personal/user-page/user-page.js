AV.init({
  appId: "",
  appKey: "",
  serverURL: ""
});

function setupData() {
  $("#welcome").text("Hello! " + LC.User.current().data.username);
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

function updateBlkId() {
  var query2 = new AV.Query('UserData');
  query2.equalTo('username', AV.User.current().get('username'));
  query2.find().then((user) => {
    if (user.length>0) {
      if (user[0].get('blockIndex') != ""){
        document.getElementById("blkid").innerText = user[0].get('blockIndex'); 
        document.getElementById("btn").disabled = true;
      }
      else {
        document.getElementById("btn").disabled = false;
      }
    }

  });
  
  
}

function updateRealName() {
  const query = new AV.Query('_User');
  console.log(AV.User.current());
  query.equalTo('username', AV.User.current().get('username'));
  query.find().then((user) => {
    if (user[0].get('nameOnBlk') != ""){
      document.getElementById("realname").innerText = user[0].get('nameOnBlk'); 

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
  
  window.location.href = "./addname.html";
}
function jump2() {
  
  window.location.href = "./explorer/index.html";
}

$(function () {
  if (LC.User.current()) {
    setupData();
    updateRealName();
    updateBlkId();
    
  } else {
    window.location.href = "./../login/login.html";
  }
});
