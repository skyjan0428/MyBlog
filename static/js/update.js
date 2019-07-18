
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

