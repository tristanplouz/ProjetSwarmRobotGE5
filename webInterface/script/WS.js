function WS(){
	console.log("try");
	this.connect = function(addr,port){
		var that=this;
		this.socket = new WebSocket('ws://'+addr+':'+port);
		this.socket.onerror = function (err){
			if (that.socket.readyState == 3) {
				screen_panel.update("vers","Erreur de connexion");
			}
		};
		this.socket.onopen = function (evt) {
			console.log(evt);
			that.send({"type":"hello","msg":"nOUVEAUX client connecté"}); 
			screen_panel.update("vers","Connecté: ");
		};
		this.socket.onmessage = function (evt) {
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
		switch(evt.type){
			default:
				console.log("msg inconnu: "+evt.type);
			}
	}
}
