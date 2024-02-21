const express = require('express');
const { Pool } = require('pg');
const fs = require('fs');
const ini = require('ini');

const app = express();
const port = 3000;

// Read the INI file to get database connection details
const config = ini.parse(fs.readFileSync('./db.INI', 'utf-8'));

// Create a PostgreSQL connection pool
const pool = new Pool({
    user: config.db_connection.user,
    host: config.db_connection.host,
    database: config.db_connection.database,
    password: config.db_connection.password,
    port: 5432
});

// Set EJS as the view engine
app.set('view engine', 'ejs');

// Define a route to render the dashboard
app.get('/', async (req, res) => {
    try {
        const client = await pool.connect();
        const result = await client.query('SELECT * FROM users');
        const users = result.rows;
        client.release();
        res.render('dashboard', { users: users });
    } catch (error) {
        console.error('Error executing query', error);
        res.status(500).send('Internal Server Error');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
});
