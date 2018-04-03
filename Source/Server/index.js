var express = require('express')
var app = express();
app.use(express.static('public'))

app.get('/', function (req, res) {
   res.sendFile('index.html')
   res.end()
})

var server = app.listen(9898, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Ung dung Node.js dang lang nghe tai dia chi: http://%s:%s", host, port)

})