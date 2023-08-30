var Chatty = {

    get_env : function(){
        var url = document.URL;
        if (url.indexOf('localhost') >= 0 || url.indexOf('127.0.0.1') >= 0 || url.indexOf('192.168') >= 0 || url.indexOf('file://') >= 0) {
            return "local";
        }
        return "prd";
    },

    get_server : function(){
        var env = this.get_env();
        if (env == 'local') {
            return "ws://localhost:8888";
        }
        return "wss://www.chatties.shop:8888";
    },

    init : function() {

        // 웹 서버를 접속한다.
        var self = this;
        var server = this.get_server();
        this.webSocket = new WebSocket(server);

        // 웹 서버와의 통신을 주고 받은 결과를 출력할 오브젝트를 가져옵니다.
        var logViewArea = document.getElementById("logViewArea");
        var chatMessage = document.getElementById("chatMessage");
        var textbook = document.getElementById("textbook");
        var transcribedText = document.getElementById("transcribedText");
        var recordStatus = 'stop';

        // 소켓 접속이 되면 호출되는 함수
        this.webSocket.onopen = function (message) {

            console.log("Server connect...");
            //var contents_url = document.getElementById("contents_url").value;
            //autoMessage("TEXTBOOK", {"url": contents_url})
        };
        // 소켓 접속이 끝나면 호출되는 함수
        this.webSocket.onclose = function (message) {
            //logViewArea.value += "Server Disconnect...\n";
        };
        // 소켓 통신 중에 에러가 발생되면 호출되는 함수
        this.webSocket.onerror = function (message) {
            //logViewArea.value += "error...\n";
        };
        // 소켓 서버로 부터 메시지가 오면 호출되는 함수.
        this.webSocket.onmessage = function (message) {
            // 출력 area에 메시지를 표시한다.
            var recv_data = JSON.parse(message.data);
            console.log(recv_data);

            var command = recv_data['cmd'];
            var data = recv_data['data'];
            if (command == "TEXTBOOK_ACK") {
                textbook.value += data['contents'] + "\n";
                //clickRecordBtn();
            } else if (command == "CHAT_MSG_ACK") {
                //chatMessage.value += "[AGENT] : " + data['msg'] + "\n";
                console.log(  "[AGENT] : ", data['msg']  );
                JSUtils.generateTemplate( "conv_list", "conv_tmpl", { speaker: "agent", text : data['msg'] }, true );
                scroll_to_bottom();

                var audioPath = data['tts_path'];
                self.playAudio( audioPath );
                //clickRecordBtn(); // 다음대화 시작을 위한 녹음모드 열기(start)
            } else {
                chatMessage.value += "[ERROR] : unknown_data, cmd = " + command + "\n";
            }

        };

        //this.webSocket2 = webSocket;

        this.initEvent();
    },


    initEvent: function() {
        var self = this;
        var sendButton = document.getElementById("sendBtn");
        var textMessage = document.getElementById("textMessage");
        //window.addEventListener('focus', $.proxy( this.onFocusView, this ), false );
        textMessage.addEventListener("keyup", function (event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                self.sendMessage();
            }
        });

        sendButton.addEventListener("click", function (event) {
            self.sendMessage();
        });
    },

    // 서버로 메시지를 전송하는 함수
    sendMessage : function(value) {
        var message = document.getElementById("textMessage");
        if (!value) {
            value = message.value;
        }
        var data = {"cmd": "CHAT_MSG", "params": {'msg': value}};
        var sendData = JSON.stringify(data);

        //logViewArea.value += "[SEND] to Server => " + value + "\n";
        //chatMessage.value += "[ME] : " + value + "\n";
        JSUtils.generateTemplate( "conv_list", "conv_tmpl", { speaker: "me", text : value }, true );


        //웹소켓으로 textMessage객체의 값을 보낸다.
        this.webSocket.send(sendData);
        //textMessage객체의 값 초기화
        message.value = "";
    },

    autoMessage : function(command, params) {
        //var data = { "cmd" : command, "params" : JSON.parse( message ) };
        var data = {"cmd": command, "params": params};
        var sendData = JSON.stringify(data);
        //웹소켓으로 textMessage객체의 값을 보낸다.
        this.webSocket.send(sendData);
    },

    disconnect : function() {
        this.webSocket.close();
    },

    playAudio : function(audio_url) {
        var myAudio = document.getElementById("myAudio");
        var url = document.URL;
        var env = this.get_env();

        if (env == 'local') {
            var host = url.substring(0, url.lastIndexOf("/"));
            myAudio.src = host + audio_url;
        } else {
            myAudio.src = window.location.origin + audio_url;
        }
        myAudio.play();
    },

    clickRecordBtn : function() {
        $("#record").trigger("click");
    },

    /*
    function checkSpeech(){
        var stt_text = transcribedText.innerText.trim();
        console.log("timeout = ", stt_text );
    }
     */

    /*
    var prevSendMessage = '';
    setInterval(() => {
        var stt_text = transcribedText.innerText.trim();
        console.log("setInterval => ", stt_text );
        if ( stt_text.length > 0 && stt_text != prevSendMessage ){
            sendMessage( stt_text );
            prevSendMessage = stt_text;

            clickRecordBtn(); // stop
        }
    }, 2000);
    */
}

function callbackStartRecording() {
    console.log("[callback] start recording");
    //recordStatus = 'start';
}

function callbackStopRecording() {
    console.log("[callback] stop recording");
    var transcribedText = document.getElementById("transcribedText");
    //recordStatus = 'stop';

    // 여러번 호출될 가능성 존재
    var timeoutId = setTimeout(() => {
        var stt_text = transcribedText.innerText.trim();
        console.log("[ASR] timeout = ", stt_text);
        if (stt_text.length > 0) {
            Chatty.sendMessage(stt_text);
            scroll_to_bottom();
        }
    }, 2000);
    // clearTimeout(timeoutId);
}

function scroll_to_bottom() {
  var chatUl = document.getElementById('chatview');
  chatUl.scrollTop = chatUl.scrollHeight; // 스크롤의 위치를 최하단으로
}


Chatty.init();