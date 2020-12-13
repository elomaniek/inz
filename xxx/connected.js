const HandyStorage = require('handy-storage');

const storage = new HandyStorage('connected.json', {
  beautify: true,
});

module.exports = {
  get: () => storage.state,
  set: changes => storage.setState(changes),
};
