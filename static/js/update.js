
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
  fd.append('type', 'uploadPost')
  fd.append('token', getCookie('token'))
  fd.append('owner', owner)
  fd.append('content', content)
  function success(data){
    console.log(data);
    if (data.status) { 
        var dv = document.createElement("DIV");
        dv.className='postForm';
        dv.id = "post" + data.data.post_id;
        var photo = ""
        if(data.data.contentPhoto)
          photo = "<img class='postContentImg' src='"+data.data.contentPhoto+"'><br>"
        
        // dv.innerHTML = "<div id='title'> <img class='postFace' src='"+data.data.userPhoto+"' > <span id='name'>"+data.data.name+"</span><span id='date'>"+data.data.date+"</span>"+"</div><p>"+data.data.content+"</p>" + photo + "<a onclick='like("+data.data.post_id+")'>讚</a>";
        
        dv.innerHTML = '<div class="title">' +
                              '<img class="postFace" src="'+data.data.userPhoto+'" alt="Avatar">' +
                              '<span class="name">'+data.data.name+'</span>'+
                              '<span class="date">'+data.data.date+'</span>'+
                              '<img id="delete" src ="'+url+'"class="delete" onclick="deletePost('+data.data.post_id+')">'+
                          '</div>'+
                          '<p align="left"> '+data.data.content+'</p>'+
                          photo +
                          '<div style="width:97%; height:2px; background: #F7F8FA; margin-bottom: 5px; margin-top: 10px;"></div>'+
                          '<p align="left" style="color:#4267B2; font-size: 10px;" id="like'+data.data.post_id+'"> 讚&nbsp;0</p>'+
                          '<div class = "leaveMessageButton">'+
                              '<button id = "like_button'+data.data.post_id+'" onclick="like('+data.data.post_id+')">讚</button>'+
                              '<button onclick=""> 留言</button>' +
                          '</div>' +
                          '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>' +
                          '<div id="message'+data.data.post_id+'">'+
                          '</div>'+
                          '<div id="leaveMessage">' +
                              '<textarea placeholder="留言" id="mess'+data.data.post_id+'" onkeypress="onTestChange('+data.data.post_id+')"></textarea>' +
                          '</div>';



        var posts = document.getElementById('posts')
        posts.insertBefore(dv, posts.firstChild);
        // document.getElementById("delete").src = url;

    }
  }
  function error(data){
    console.log(data)
  }
  $.ajax({
            type: "POST", //傳送方式
            url: "/postoperation/", //傳送目的地
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
      type: 'likepost',
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


function onTestChange(id) {
    var key = window.event.keyCode;

    // If the user has pressed enter
    if (key === 13) {
      value = document.getElementById("mess"+id).value;
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
  fd.append('token', getCookie('token'));
  fd.append('content', content);
  fd.append('type', 'uploadPost');
  fd.append('attach_id', id);
  fd.append('owner', owner);
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
            url: "/postoperation/", //傳送目的地
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
  if(!chatBody)
    return;
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
function closeChatRoom(id){
  var chatRoom = document.getElementById("chatRoom" + id);
  chatRoom.remove();

}

function openChat(id){
  if(document.getElementById("chatRoomContent" + id)){
    if(document.getElementById("chatBody"+id).style.display == 'none')
      hiddenBody(id);
    return;
  }
  function success(data) {
    console.log(data);
      if (data.status) { 
        console.log(data);
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
        chatRoom.innerHTML = '<div class="chatRoomTitle" onclick="hiddenBody('+data.data.reciever.id+')">' + 
                                '<span style = "display: flex; justify-content: space-around; align-items: center;">' +
                                '<img id = "cat" src="'+data.data.reciever.photo+'" alt="Avatar">&nbsp;&nbsp;&nbsp; '+ data.data.reciever.name+' </span>' + 
                                '</span> <span id = "closeChatRoom" onclick="closeChatRoom('+data.data.reciever.id+')" style="display: flex; justify-content: flex-end;"> X </span>'+
                                '</div>'+
                                '<div id="chatBody'+data.data.reciever.id+'">'+
                                '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>'+
                                '<div class="chatRoomContent" id="chatRoomContent'+data.data.reciever.id+'">'+ m +'</div>' +
                                '<div style="width:100%; height:2px; background: #F7F8FA; margin-top: 8px;margin-bottom: 8px;"></div>'+
                                '<input class="inputChat" id="inputChat'+ data.data.reciever.id+'" onkeypress="sendChatEnter('+ data.data.reciever.id+')"placeholder="輸入訊息" type="text">'+
                              '</div>'
        
        

          var chatRooms = document.getElementById('chatRooms');
          chatRooms.append(chatRoom);

          var chatRoomContent = document.getElementById('chatRoomContent'+data.data.reciever.id);
          chatRoomContent.scrollTop = chatRoomContent.scrollHeight;
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

function sendChat(id){
  var chat = document.getElementById("inputChat" + id);
  console.log(chat);
  var message = chat.value;
  
  chat.value = "";
  // var chatRoom = document.getElementById('chatRoom');
  chatSocket.send(JSON.stringify({
  'message': message,
  'user_id':id,
      
  }));
}

function sendChatEnter(id) {
    var key = window.event.keyCode;

    // If the user has pressed enter
    if (key === 13) {
      sendChat(id);
      return false;
    }
    else {
        return true;
    }
}

var chatSocket = new WebSocket(
  'ws://' + window.location.host + '/blog/');

chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  console.log(e.data);
  if(data['type'] == 'postLike'){
    console.log(data['content']);
  }else if(data['type'] == 'postMessage'){
    console.log(data['content']);
  }else{
    recieveChat(data);
  }
  
  
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

function recieveChat(data){
  var message = data['message'];
  var sender = data['sender'];
  var receiver = data['receiver'];
  var is_self = data['self'];
  
  var d = document.createElement("DIV");
  d.style.display="flex";
  

  var chatRoom; 
  if(is_self){
      chatRoom = document.getElementById('chatRoomContent'+receiver);
      d.style.justifyContent="flex-end";
      d.innerHTML =  '<div class="chatRight" align="right"> '+
                          message+
                    '</div>'
  }else{
      d.style.justifyContent="flex-start";
      chatRoom = document.getElementById('chatRoomContent'+sender);
      if(!chatRoom){       
        openChat(sender);
        return;
      }
      if(document.getElementById("chatBody"+sender).style.display == 'none')
        openChat(sender);
      d.innerHTML =  '<div class="chatLeft" align="left"> '+
                          message+
                    '</div>'
  }
  
  chatRoom.append(d);
  chatRoom.scrollTop = chatRoom.scrollHeight;
}

function loadPage(id){
  window.location.href = "../../post/" + id
}

function readNotification(){
  block = document.getElementById("notifyBlock")
  console.log(block.style.display);
  if(block.style.display=="none" || block.style.display==""){
    block.style.display="block";
    readNotifications();
  }else{
    block.style.display="none";
  }
}

function readNotifications(){
  function success(data) {
      notifyLength = document.getElementById("notifyLength");
      notifyLength.innerHTML = data.data.notifications;
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data= { 
      token: getCookie('token'),
  }
  sendAjax(data,"/readNotifications/","POST", "json", success, error)
}

function logout(){
  function success(data) {
      if(data.status){
        window.location.href = "/login/"
      }
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data= { 
      token: getCookie('token'),
  }
  sendAjax(data,"/logout/","POST", "json", success, error)
}

function deletePost(id){
  function success(data) {
      if(data.status){
        var post = document.getElementById("post" + id);
        post.parentNode.removeChild(post);
      }
   }
  function error(jqXHR) {
      console.log(jqXHR)
  }
  data= { 
      token: getCookie('token'),
      post_id: id,
      type: 'delete',
      owner: owner,
  }
  sendAjax(data,"/postoperation/","POST", "json", success, error)
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
