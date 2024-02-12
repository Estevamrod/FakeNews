const express = require('express');
const cors = require('cors');
const axios = require('axios');
const dotenv = require('dotenv').config();

const app = express();

app.use(express.json());
app.use(cors({
    origin:['http://localhost:3000', process.env.pyEndPoint.toString()],
    methods: ['GET', 'POST']
}))

app.get('/', (req, res) => {
    return res.status(200).json({msg:"OK"});
});

app.post('/similar', async(req, res) => {
    if (req.body){
        const {UserQuery} = req.body;
        try {
            const data = await axios.post(process.env.pyEndPoint.toString(), {
                'userQuery': UserQuery
            });
            console.log(data.data);
            return res.status(200).json({msg:"OK", data:data.data});
        } catch (e) {
            console.log(e);
            return e;
        }
    }
})

module.exports = app;