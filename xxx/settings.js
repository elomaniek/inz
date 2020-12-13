const HandyStorage = require('handy-storage');

const storage = new HandyStorage('settings.json', {
  beautify: true,
});

module.exports = {
  get: () => storage.state,
  set: changes => storage.setState(changes),
};
