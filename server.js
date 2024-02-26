const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();

app.use("/static", express.static(path.resolve(__dirname, "frontend", "static")));


app.get("/run-image-python-qtm", (req, res) => {
    const scriptPath = path.resolve(__dirname, 'backend/retrieve_coin.py');
    console.log(scriptPath);
    
    exec(`python "${scriptPath}" "QTUM_BTC"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ message: "Internal Server Error" });
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        
        // Assuming your Python script outputs the path to the generated image
        const imageUrl = stdout.trim();
        res.json({ status: `ok`, imageUrl: `/static/js/images/coin_predict.png?${new Date().getTime()}` });
    });
});

app.get("/run-image-python-eth", (req, res) => {
    const scriptPath = path.resolve(__dirname, 'backend/retrieve_coin.py');
    console.log(scriptPath);
    
    exec(`python "${scriptPath}" "ETH_BTC"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ message: "Internal Server Error" });
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
        
        // Assuming your Python script outputs the path to the generated image
        const imageUrl = stdout.trim();
        res.json({ status: `ok`, imageUrl: `/static/js/images/coin_predict.png?${new Date().getTime()}` });
    });
});

app.get("/*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8888, () => console.log("Server running..."));