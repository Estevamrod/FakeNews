const http = require('http');
const app = require('./app');
const dotenv = require('dotenv').config();

const server = http.createServer(app);
const PORT = process.env.PORT;

server.listen(PORT, () => {
    console.log(`running on http://localhost:${PORT}`);
})