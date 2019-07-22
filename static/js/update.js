
function sendAjax(data, path, type,dataType, success, error){
  $.ajax({
            type: type, //傳送方式
            url: path, //傳送目的地
            dataType: dataType, //資料格式
            data: data,
            success: success,
            error: error,
        });
}
function sendPost(){
  var content = document.getElementById("content").value;
  data = { 
    content: content, 
    token: getCookie('token')
  }
  function success(data){
    if (data.status) { 
        var dv = document.createElement("DIV");
        dv.id='postForm';
        dv.innerHTML = "<div id='title'> <img class='postFace' src='"+data.data.photo+"' > <span id='name'>"+data.data.name+"</span><span id='date'>"+data.data.date+"</span>"+"</div><p>"+data.data.content+"</p><a onclick='like("+data.data.post_id+")'>讚</a>";
        var posts = document.getElementById('posts')
        posts.insertBefore(dv, posts.firstChild);

    }
  }
  function error(data){
    console.log(jqXHR)
  }
  sendAjax(data,"/sendPost/","POST", "json", success, error)
}

function like(id){
  function success(data) {
      console.log(data)
      if (data.status) { 
        
      }
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data= { 
      post_id: id, 
      token: getCookie('token'),
      operate: 'likepost',
  }
  sendAjax(data,"/postoperation/","POST", "json", success, error)
}

var user_id = "";
function chooseUser(id){
  user_id = id;
  document.getElementById('chatRoom').value = "";
  function success(data) {
      if (data.status) { 
          lst = data['data']
          var chatRoom = document.getElementById('chatRoom');
          lst.forEach(function(e){
              chatRoom.value += "\n"+ e['text'];
          });
      }
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data={ 
    token: getCookie('token'),
    'reciever': user_id,
  }
  sendAjax(data,"/openChatRoom/","POST", "json", success, error)
}
function addFriend(id){
  function success(data) {
      console.log(data)
  }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data = { 
    token: getCookie('token'),
    'user_id': id,
  }
  sendAjax(data,"/information/addFriend/","POST", "json", success, error)
    
}


function createDescription(){
  var des = document.getElementById("makeDescription");
  var content = ""
  if(des.innerText != null)
    content = des.innerText;
  des.innerHTML = "<textarea id='des' placeholder='在此更新你的簡介'>" + content + "</textarea> <button type='button' onclick='addDescription()'> 確認 </button>";
}

function addDescription(){
  var content = document.getElementById('des');
  function success(data) {
      var des = document.getElementById("makeDescription");
       des.innerHTML = content.value;
  }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data = { 
    token: getCookie('token'),
    'type': '1',
    'description': content.value,
  }
  sendAjax(data,"/information/revise/","POST", "json", success, error)

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
