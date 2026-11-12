// Listens on 3000 and nothing else: it never reads PORT. A service whose port
// isn't 3000 can't reach it, which is the failure this branch exists to show.
const http = require("node:http");

const PORT = 3000;

http
  .createServer((req, res) => {
    res.writeHead(200, { "content-type": "text/plain" });
    res.end("golden/fixed-port fixture\n");
  })
  .listen(PORT, () => console.log(`Server is running on port ${PORT}`));
