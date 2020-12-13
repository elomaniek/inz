const express = require('express');
const settings = require('./settings');
const connected = require('./connected');
const nms = require('./media-server');
const cors = require('cors')


const app = express();
app.use(express.json());
app.use(cors());

const nmsInstance = nms.run(settings.get().archive);

app.get('/settings', (_, res) => {
  res.status(200).send(settings.get());
});

app.get('/connected', (_, res) => {
  res.status(200).send(connected.get());
 });


app.post('/connected', (req, res) => {

  const filteredChanges = req.body;
 
  connected.set(filteredChanges);                             //JSON.parse(filteredChanges);
  res.status(200).send();
});

app.post('/connected_del', (req, res) => {
  const currentSettings = connected.get();
  
  

  const streams = Object.keys(req.body);
  console.log(streams[0])
  if ((streams[0] in currentSettings)==true){
    console.log("SENT REQUEST TO START STREAMING")
    delete currentSettings[streams[0]]
    connected.set(currentSettings)
  }
  
  
  res.status(200).send();
});



app.post('/settings', (req, res) => {
  const currentSettings = settings.get();
  const filteredChanges = Object.entries(req.body)
    .filter(([key]) => {
      if (currentSettings[key] === undefined) {
        return false;
      }

      return true;
    })
    .reduce((agg, curr) => {
      agg[curr[0]] = curr[1];
      return agg;
    }, {});

  if (currentSettings.archive !== filteredChanges.archive) {
    if (filteredChanges.archive) {
      nmsInstance.startArchiving();
      console.log('[!!!] Archiving started!');
    } else {
      nmsInstance.stopArchiving();
      console.log('[!!!] Archiving stopped!');
    }
  }

  settings.set(filteredChanges);
  res.status(200).send();
});

app.listen(8080);
console.info('Up and running, listening on 8080');
