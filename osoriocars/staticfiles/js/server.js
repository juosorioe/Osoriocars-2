const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'osoriocars'
});

db.connect(err => {
    if (err) {
        throw err;
    }
    console.log('MySQL connected...');
});

app.post('/register', (req, res) => {
    const { username, email, password } = req.body;
    const hashedPassword = bcrypt.hashSync(password, 8);

    const query = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)';
    db.execute(query, [username, email, hashedPassword], (err, results) => {
        if (err) {
            return res.status(500).send('Server error');
        }
        const token = jwt.sign({ id: results.insertId }, 'secretkey', {
            expiresIn: 86400
        });
        res.status(201).send({ auth: true, token });
    });
});

app.post('/login', (req, res) => {
    const { email, password } = req.body;

    const query = 'SELECT * FROM users WHERE email = ?';
    db.execute(query, [email], (err, results) => {
        if (err) {
            return res.status(500).send('Server error');
        }
        if (results.length === 0) {
            return res.status(404).send('User not found');
        }

        const user = results[0];
        const passwordIsValid = bcrypt.compareSync(password, user.password);

        if (!passwordIsValid) {
            return res.status(401).send('Invalid password');
        }

        const token = jwt.sign({ id: user.id }, 'secretkey', {
            expiresIn: 86400
        });

        res.status(200).send({ auth: true, token });
    });
});

app.listen(3000, () => {
    console.log('Server started on port 3000');
});