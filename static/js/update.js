
function sendPost(){
	console.log(getCookie('token').replace("\"", ""))
	$.ajax({
            type: "POST", //傳送方式
            url: "/sendPost/", //傳送目的地
            dataType: "json", //資料格式
            data: { //傳送資料
                content: '123456', //表單欄位 ID nickname
                token: getCookie('token') //表單欄位 ID gender
            },
            success: function(data) {
                // if (data.nickname) { //如果後端回傳 json 資料有 nickname
                //     $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                //     $("#result").html('<font color="#007500">您的暱稱為「<font color="#0000ff">' + data.nickname + '</font>」，性別為「<font color="#0000ff">' + data.gender + '</font>」！</font>');
                // } else { //否則讀取後端回傳 json 資料 errorMsg 顯示錯誤訊息
                //     $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                //     $("#result").html('<font color="#ff0000">' + data.errorMsg + '</font>');
                // }
            },
            error: function(jqXHR) {
                // $("#demo")[0].reset(); //重設 ID 為 demo 的 form (表單)
                // $("#result").html('<font color="#ff0000">發生錯誤：' + jqXHR.status + '</font>');
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

