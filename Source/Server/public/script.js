function clickToggle() {
	if($('#dev1status').text() == 'Device 1: ON') {
		$('#dev1status').text('Device 1: OFF')
	}
	else {
		$('#dev1status').text('Device 1: ON')
	}
}

$(document).ready( () => {
	const socket = io('hgn37.ddns.net:9899')
	socket.on('connect', () => {
		console.log('Connected')
	})
	socket.on('disconnect', () => {
		console.log('Disconnected')
	})
	socket.open(
})