
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
  document.getElementById('chatRoom').value = "";
  $.ajax({
            type: "POST", 
            url: "/openChatRoom/", 
            dataType: "json", 
            data: { 
                'reciever': user_id,
            },
            success: function(data) {
              if (data.status) { 
                  lst = data['data']
                  var chatRoom = document.getElementById('chatRoom');
                  lst.forEach(function(e){
                      chatRoom.value += "\n"+ e['text'];
                  });
              }
            },
            error: function(jqXHR) {
              console.log(jqXHR)
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jsqXHR.status + '</font>');
            }
        });
}
function addFriend(id){
    $.ajax({
            type: "POST", 
            url: "/information/addFriend/", 
            dataType: "json", 
            data: { 
                'user_id': id,
            },
            success: function(data) {
              console.log(data)
            },
            error: function(jqXHR) {
              console.log(jqXHR)
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jsqXHR.status + '</font>');
            }
        });
  }


function createDescription(){
  console.log("createDescription");
  var des = document.getElementById("makeDescription");
  var content = ""
  if(des.innerText != null)
    content = des.innerText;
  des.innerHTML = "<textarea id='des' placeholder='在此更新你的簡介'>" + content + "</textarea> <button type='button' onclick='addDescription()'> 確認 </button>";
}

function addDescription(){
  console.log("addDescription");

  var content = document.getElementById('des');
  console.log(content.value);
  $.ajax({
            type: "POST", 
            url: "/information/revise/", 
            dataType: "json", 
            data: { 
                'type': '1',
                'description': content.value,
            },
            success: function(data) {
              var des = document.getElementById("makeDescription");
              des.innerHTML = content.value;
            },
            error: function(jqXHR) {
              console.log(jqXHR)
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jsqXHR.status + '</font>');
            }
        });
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
  'ws://' + window.location.host + '/blog/');

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

// function sendTest(){
//   console.log("click!");
//   var message = "test";
//   chatSocket.send(JSON.stringify({
//       'message': message
//   }));
// }
