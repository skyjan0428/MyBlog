
function sendPost(){
  var content = document.getElementById("content").value;
  console.log(content);
	$.ajax({
            type: "POST", //傳送方式
            url: "/sendPost/", //傳送目的地
            dataType: "json", //資料格式
            data: { //傳送資料
                content: content, //表單欄位 ID nickname
                token: getCookie('token') //表單欄位 ID gender
            },
            success: function(data) {
              console.log(data)
                if (data.status) { 
                  var dv = document.createElement("DIV");
                    dv.innerHTML = '<li>' + data.data.content + '</li>' + '<li>' + data.data.date + '</li></br>';
                    var posts = document.getElementById('post')
                    posts.insertBefore(dv, posts.firstChild);
                }
            },
            error: function(jqXHR) {
              console.log(jqXHR)
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jsqXHR.status + '</font>');
            }
        });
}

function like(id){
  $.ajax({
            type: "POST", //傳送方式
            url: "/postoperation/", //傳送目的地
            dataType: "json", //資料格式
            data: { //傳送資料
                post_id: id, 
                token: getCookie('token'),
                operate: '1',
            },
            success: function(data) {
              console.log(data)
                if (data.status) { 
                  
                }
            },
            error: function(jqXHR) {
              console.log(jqXHR)
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jsqXHR.status + '</font>');
            }
        });
}
var user_id = "";

function chooseUser(id){
  user_id = id;
}


function sendChat(){
  var chat = document.getElementById("chat");
  console.log(chat);
  var message = chat.value;
  
  chat.value = "";
  var chatRoom = document.getElementById('chatRoom');
  chatRoom.value += "\n"+"You" + " : " + message;
  chatSocket.send(JSON.stringify({
    'message': message,
      'user_id':user_id,
      
  }));
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

var chatSocket = new WebSocket(
  'ws://127.0.0.1/blog/');

chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  console.log(e.data);
  var message = data['message'];
  var chatRoom = document.getElementById('chatRoom');
  chatRoom.value += "\n"+data['sender'] + " : " + message;
  console.log("收到" + message + '\n');
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

// document.querySelector('#chat-message-input').focus();

// document.querySelector('#chat-message-input').onkeyup = function(e) {
//   if (e.keyCode === 13) {  // enter, return
//       document.querySelector('#chat-message-submit').click();
//   }
// };

function sendTest(){
  console.log("click!");
  var message = "test";
  chatSocket.send(JSON.stringify({
      'message': message
  }));
}
