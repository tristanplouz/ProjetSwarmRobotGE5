function Screen(sec){
	this.section = sec;
	this.show = function(){
		this.section.style.display = "block";
		console.log(this.section.id+" showed");
		try{
			this.updateView();
		}
		catch(err){
			
		}
	}
	this.hide = function(){
		this.section.style.display = "none";
		console.log(this.section.id+" hidded");
	}
	
	this.update=function(id,content){
		document.getElementById(id).innerHTML =content;
	}
}

function ScreenInfo(){
	this.section = document.getElementById("info");
	this.section.style.display = "none";
}

ScreenInfo.prototype = new Screen;

function ScreenPanel(){
	
	this.section = document.getElementById("ctl_panel");
	this.section.style.display = "none";
	canvas = document.getElementById("canvasOverView");
	this.ctx = canvas.getContext("2d");
	this.cparti = function(){
		socket_handler.send({"type":"GO","msg":"c'est parti"})	
	}
	this.updateView = function(){
		
		this.drawDrone(this.ctx,canvas.width/2,canvas.height/2,'red')
	}
	this.drawDrone=function(context,x,y,color,size=0.5){
		console.log("Draw drone " );
		context.fillStyle = color;
		context.beginPath();
		context.moveTo(x-25*size,y-30*size);
		context.lineTo(x+30*size,y+25*size);
		context.lineTo(x+25*size,y+30*size);
		context.lineTo(x-30*size,y-25*size);
		context.fill();
		context.beginPath();
		context.moveTo(x+25*size,y-30*size);
		context.lineTo(x+30*size,y-25*size);
		context.lineTo(x-25*size,y+30*size);
		context.lineTo(x-30*size,y+25*size);
		context.fill();
		context.beginPath();
		context.arc(x, y, 15*size, 0, 2*Math.PI)
		context.fill();
	}

}

ScreenPanel.prototype = new Screen;

function ScreenAddSlave(){
	this.section = document.getElementById("add_slave");
	this.section.style.display = "none";
	canvas = document.getElementById("canvasConfView");
	ctx = canvas.getContext("2d");
	canvas.onclick = function (evnt){
		
		screen_panel.drawDrone(ctx,evnt.clientX,evnt.clientX,'green')
	}
	
	this.updateView = function(){
		
		screen_panel.drawDrone(ctx,canvas.width/2,canvas.height/2,'red')
		ctx.beginPath();
		ctx.arc(canvas.width/2,canvas.height/2,75, 0, 2*Math.PI);
		ctx.stroke();
		ctx.beginPath();
		ctx.arc(canvas.width/2,canvas.height/2,150, 0, 2*Math.PI);
		ctx.stroke();

	}
}

ScreenAddSlave.prototype = new Screen;

function ScreenMissionPlanner(){
	this.section = document.getElementById("mission");
	this.section.style.display = "none";
	this.path=[];
	this.map = L.map('map').setView([48.58219,7.76497], 18);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				    }).addTo(this.map);
	this.map.invalidateSize();
	
	this.coordUp = function(e){
		document.getElementById("lonP").value=e.latlng.lng;
		document.getElementById("latP").value=e.latlng.lat;
	}
	this.map.on('click',this.coordUp);
	
	this.addPt = function(){
		console.log(this.path);
		lat=parseFloat(document.getElementById("latP").value);
		lon=parseFloat(document.getElementById("lonP").value);
		alt=parseFloat(document.getElementById("altP").value);
		this.map.invalidateSize();
		try{
			this.poly.addLatLng([lat,lon])
		}
		catch(err){
			this.poly=L.polyline(L.latLng(lat, lon), {color: 'red'}).addTo(this.map);
		}
		this.path.push([lat,lon,alt])
	}
	this.show = function(){
		this.section.style.display = "block";
		console.log(this.section.id+" showed");
	}
	this.hide = function(){
		this.section.style.display = "none";
		console.log(this.section.id+" hidded");
		try{
			this.poly.remove();
		}
		catch(err){
		;	
		}
	}
}

ScreenMissionPlanner.prototype = new Screen;



function ScreenSwitch(){
		this.current_screen=null;
		this.change_screen=function(screenToShow){
			if(this.current_screen != null){
				this.current_screen.hide();
				screenToShow.show();
				this.current_screen = screenToShow;
			}
			else{
				screenToShow.show();
				this.current_screen = screenToShow;
			}
		}
}
