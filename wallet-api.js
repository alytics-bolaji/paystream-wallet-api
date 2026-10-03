// wallet-api.js  --  Paystream Kenya wallet API (staging)
// The same tiny service you ran as a systemd unit in Week 4. This week it moves
// into version control, where every change to it is tracked and reviewed.

const http = require('http');
const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({ status: 'ok', estate: 'kenya-staging' }));
    return;
  }

  if (req.url.startsWith('/wallet/')) {
    const id = req.url.split('/')[2] || 'unknown';
    res.writeHead(200);
    res.end(JSON.stringify({
      wallet: id,
      currency: 'KES',
      balance_minor: 1250000,
      source: 'database'
    }));
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({ error: 'not found' }));
});

server.listen(PORT, () => {
  console.log(`paystream wallet-api listening on port ${PORT}`);
});
