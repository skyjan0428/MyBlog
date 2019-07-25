
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
  if(content == "")
    return;
  document.getElementById("content").value = "";
  var fd = new FormData();
  var files = $('#file')[0].files[0];
  fd.append('files',files);
  fd.append('token', getCookie('token'))
  fd.append('content', content)
  function success(data){
    console.log(data);
    if (data.status) { 
        var dv = document.createElement("DIV");
        dv.className='postForm';
        var photo = ""
        if(data.data.contentPhoto)
          photo = "<img class='postContentImg' src='"+data.data.contentPhoto+"'><br>"
        
        // dv.innerHTML = "<div id='title'> <img class='postFace' src='"+data.data.userPhoto+"' > <span id='name'>"+data.data.name+"</span><span id='date'>"+data.data.date+"</span>"+"</div><p>"+data.data.content+"</p>" + photo + "<a onclick='like("+data.data.post_id+")'>讚</a>";
        

        dv.innerHTML = '<div class="title">' +
                              '<img class="postFace" src="'+data.data.userPhoto+'" alt="Avatar">' +
                              '<span class="name">'+data.data.name+'</span>'+
                              '<span class="date">'+data.data.date+'</span>'+
                          '</div>'+
                          '<p align="left"> '+data.data.content+'</p>'+
                          photo +
                          '<div style="width:97%; height:2px; background: #F7F8FA; margin-bottom: 5px; margin-top: 10px;"></div>'+
                          '<div class = "title">'+
                              '<button onclick="like('+data.data.post_id+')"> 讚</button>' + 
                              '<button onclick=""> 留言</button>' +
                              '<button onclick=""> 分享</button>' +
                          '</div>' +
                          '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>' +
                          '<div id="message'+data.data.post_id+'">'+
                          '</div>'+
                          '<div id="leaveMessage">' +
                              '<textarea placeholder="留言" id="mess'+data.data.post_id+'" onkeypress="onTestChange('+data.data.post_id+')"></textarea>' +
                          '</div>';



        var posts = document.getElementById('posts')
        posts.insertBefore(dv, posts.firstChild);

    }
  }
  function error(data){
    console.log(data)
  }
  $.ajax({
            type: "POST", //傳送方式
            url: "/sendPost/", //傳送目的地
            enctype: 'multipart/form-data',
            data: fd,
            contentType: false,
            processData: false,
            success: success,
            error: error,
        });

}

function like(id){
  function success(data) {
      console.log(data)
      if (data.status) { 
        document.getElementById('like'+id).innerHTML = "讚 " + data.data.likes;
        button = document.getElementById('like_button'+id);
        if(button.textContent.indexOf("收回讚") != -1)
          button.textContent ="讚";
        else button.textContent  = "收回讚";
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

function leaveMessage(id){
  document.getElementById("leaveMessage").style.display = "block";
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
function onTestChange(id) {
    var key = window.event.keyCode;

    // If the user has pressed enter
    if (key === 13) {
      value = document.getElementById("mess"+id).value;
      console.log(value)
      if(value != "")
        leaveMessage(id);

    }
    else {
        return true;
    }
}

function leaveMessage(id){
  var content = document.getElementById("mess"+id).value;
  document.getElementById("mess"+id).value = "";
  var fd = new FormData();
  var files = $('#file')[0].files[0];
  fd.append('files',files);
  fd.append('token', getCookie('token'))
  fd.append('content', content)
  fd.append('attach_id', id)
  function success(data){
    if (data.status) { 
        var outside = document.createElement("DIV");
        outside.className = "messages";
        outside.id = 'messages' + data.data.post_id;
        var img = document.createElement("IMG");
        img.src = data.data.userPhoto;
        img.className = "postFace";
        var div = document.createElement("DIV");
        var a = document.createElement("A");
        a.append(data.data.name);
        div.append(a);
        div.append(data.data.content);

        // var photo = ""
        // if(data.data.contentPhoto)
        //   photo = "<img class='postContentImg' src='"+data.data.contentPhoto+"'><br>"
        // dv.innerHTML = "<div id='title'> <img class='postFace' src='"+data.data.userPhoto+"' > <span id='name'>"+data.data.name+"</span><span id='date'>"+data.data.date+"</span>"+"</div><p>"+data.data.content+"</p>" + photo + "<a onclick='like("+data.data.post_id+")'>讚</a>";
        
        // dv.innerHTML = "<img class='postFace' src='"+data.data.userPhoto+"'' alt='Avatar'><div> <a href='/information/1>"+ data.data.name + "</a></div>";
        var posts = document.getElementById('message'+data.data.attach_id)
        outside.append(img);
        outside.append(div);
        posts.append(outside);

    }
  }
  function error(data){
    console.log(data)
  }
  $.ajax({
            type: "POST", //傳送方式
            url: "/sendPost/", //傳送目的地
            enctype: 'multipart/form-data',
            data: fd,
            contentType: false,
            processData: false,
            success: success,
            error: error,
  });

}

function hiddenBody(id){
  var chatBody = document.getElementById("chatBody"+id);
  var chatRoom = document.getElementById("chatRoom"+id);
  if(chatBody.style.display == 'none'){
    chatBody.style.display = "block";
    chatRoom.style.height = '300px';
    chatRoom.style.width = '250px';
  }
  else{
    chatBody.style.display = 'none';
    chatRoom.style.height = '40px';
    chatRoom.style.width = '170px';
  }
  
}

function openChat(id){
  function success(data) {
    console.log(data);
      if (data.status) { 
        var chatRoom = document.createElement("DIV");
        chatRoom.id = 'chatRoom'+data.data.reciever.id;
        chatRoom.className = 'chatRoom';
        var messages = data.data.messages;
        m = '';
        messages.forEach(function(element){
          if(element.user_id == data.data.reciever.id){
            m += '<div style = "display: flex; justify-content: flex-start;">'+
                    '<div class="chatLeft" align="left"> '+
                      element.text+
                    '</div>' +
                  '</div>'
          }else{
            m += '<div style = "display: flex; justify-content: flex-end;">'+
                    '<div class="chatRight" align="right"> '+
                      element.text+
                    '</div>' +
                  '</div>'
          }
        });
        chatRoom.innerHTML = '<div class="chatRoomTitle" onclick="hiddenBody('+data.data.reciever.id+')"><img id = "cat" src="'+data.data.reciever.photo+'" alt="Avatar">&nbsp;&nbsp;&nbsp; '+ data.data.reciever.name+' </div>'+
                                '<div id="chatBody'+data.data.reciever.id+'">'+
                                '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>'+
                                '<div class="chatRoomContent">'+ m +'</div>' +
                                '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>'+
                                '<input id="inputChat" placeholder="輸入訊息" type="text">'+
                              '</div>'
        
        

          var chatRooms = document.getElementById('chatRooms');
          chatRooms.append(chatRoom);
          // lst = data['data']
          // var chatRoom = document.getElementById('chatRoom');
          // lst.forEach(function(e){
          //     chatRoom.value += "\n"+ e['text'];
          // });
      }
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data={ 
     'token': getCookie('token'),
    'reciever': id,
  }
  sendAjax(data,"/openChatRoom/","POST", "json", success, error)
}


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
