"use strict";
const express = require("express");
const app = express();
const { spawnSync } = require("child_process");
const fs = require("fs").promises;

const port = 9000;

const exec_update_reservations = function () {
  const process = spawnSync("venv/bin/python", [
    "execs/update_reservations.py",
  ]);
  //   process.stdout.on("data", (data) => {
  //     console.log(`stdout: ${data}`);
  //   });
  //   process.on("close", (code) => {
  //     console.log(`child process exited with code ${code}`);
  //   });
};

app.get("/update", async function (req, res) {
  exec_update_reservations();
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/plain");
  res.send("res from server");
});
app.get("/", function (req, res) {
  fs.readFile(__dirname + "/main.html").then((contents) => {
    res.setHeader("Content-Type", "text/html");
    res.writeHead(200);
    res.end(contents);
  });
});
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
app.use(express.static("./"));
