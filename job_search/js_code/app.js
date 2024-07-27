const express = require('express');
const app = express();
const port = 3000;
const axios = require('axios');
const path = require('path');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
async function jobSearch(jobName) {
    const response = await axios.get('http://127.0.0.1:8000/job?job=' + jobName + '');
    return response.data
}
// Middleware to serve static files
app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res, next) => {
    console.log(req.method, req.url);
    next();
})
// Set up view engine and views directory
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});
app.post('/job',async (req, res) => { 
    var job = req.body.jobName;
    var resp = await jobSearch(job);
    res.render('joblist', { jobs: resp,ob:job });
})
app.get('/api/jobs', async(req, res) => {
    const jobName = req.query.job;
    
    var resp = await jobSearch(jobName);
    res.json(resp);
});
app.post('/job-details/', (req, res) => {
    console.log(req.body);
    const job = req.body;
    if (job) {
        res.render('jobview', { job: JSON.parse(job.jobData) });
    } else {
        res.status(404).send('Job not foun');
    }
});
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
