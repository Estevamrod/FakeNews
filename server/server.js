const http = require('http');
const app = require('./app');
require('dotenv').config();

const server = http.createServer(app);
const PORT = process.env.PORT; //normally its 1024, but in linux, can be 1024 or over not down this.

server.listen(PORT, () => {
    console.log(`running on http://localhost:${PORT}`);
})