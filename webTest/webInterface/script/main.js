var screen_info = new ScreenInfo();
var screen_slave = new ScreenAddSlave();
var screen_panel = new ScreenPanel();
var screen_mission = new ScreenMissionPlanner();

var screen_handler = new ScreenSwitch();

screen_handler.change_screen(screen_panel);
screen_panel.updateView();

var socket_handler = new WS();
socket_handler.connect("172.20.10.6",8765);

window.onbeforeunload = function(){
		socket_handler.close(1000,"reload")
		console.log("Fermeture de la connection");
		return true;
};
