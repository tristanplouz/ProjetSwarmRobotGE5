function WS(){
	console.log("try");
	this.connect = function(addr,port){
		var that=this;
		this.socket = new WebSocket('ws://'+addr+':'+port);
		this.socket.onerror = function (err){
			if (that.socket.readyState == 3) {
				console.log("Erreur de connexion");
			}
		};
		this.socket.onopen = function (evt) {
			console.log(evt);
			that.send({"type":"hello","msg":"nOUVEAUX client connecté"}); 
			console.log("Connecté: ");
		};
		this.socket.onmessage = function (evt) {
            console.log(evt)
			that.recv(evt);
		};
	}
	this.close = function(code,reason){
		this.send({"type":"closing"});
		this.socket.close(code,reason);
	}
	this.send = function(msg){
		console.log(msg);
		this.socket.send(JSON.stringify(msg));
	}
	this.recv =function(evt){
		console.log(evt);
        var msg = JSON.parse(evt.data);
        console.log(msg.type);
        console.log(msg.ctn);
		switch(msg.type){               
			case "masterP":
                console.log("Master: "+msg.lat+msg.lon+msg.head);
                 marker1.setLatLng([msg.lat, msg.lon]);
                 marker1._icon.style[L.DomUtil.TRANSFORM]+="rotate("+msg.head+"deg)"
                break;
            case "slaveP":
                break;
            default:
                
			}
	}
}
