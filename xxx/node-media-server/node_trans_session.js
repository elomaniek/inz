//
//  Created by Mingliang Chen on 18/3/9.
//  illuspas[a]gmail.com
//  Copyright (c) 2018 Nodemedia. All rights reserved.
//
const Logger = require('./node_core_logger');

const EventEmitter = require('events');
const { spawn } = require('child_process');
const dateFormat = require('dateformat');
const mkdirp = require('mkdirp');
const fs = require('fs');

class NodeTransSession extends EventEmitter {
  constructor(conf) {
    super();
    this.conf = conf;
  }

  run() {
    let vc = this.conf.vc || 'copy';
    let ac = this.conf.ac || 'copy';
    let inPath = 'rtmp://127.0.0.1:' + this.conf.rtmpPort + this.conf.streamPath;
    let ouPath = `${this.conf.mediaroot}/${this.conf.streamApp}/${this.conf.streamName}`;
    let mapStr = '';

    if (this.conf.rtmp && this.conf.rtmpApp) {
      if (this.conf.rtmpApp === this.conf.streamApp) {
        Logger.error('[Transmuxing RTMP] Cannot output to the same app.');
      } else {
        let rtmpOutput = `rtmp://127.0.0.1:${this.conf.rtmpPort}/${this.conf.rtmpApp}/${this.conf.streamName}`;
        mapStr += `[f=flv]${rtmpOutput}|`;
        Logger.log('[Transmuxing RTMP] ' + this.conf.streamPath + ' to ' + rtmpOutput);
      }
    }
    if (this.conf.hls) {
      this.conf.hlsFlags = this.conf.hlsFlags ? this.conf.hlsFlags : '';
      let hlsFileName = 'index.m3u8';
      let mapHls = `${this.conf.hlsFlags}${ouPath}/${hlsFileName}|`;
      mapStr += mapHls;
      Logger.log('[Transmuxing HLS] ' + this.conf.streamPath + ' to ' + ouPath + '/' + hlsFileName);
    }
    if (this.conf.dash) {
      this.conf.dashFlags = this.conf.dashFlags ? this.conf.dashFlags : '';
      let dashFileName = 'index.mpd';
      let mapDash = `${this.conf.dashFlags}${ouPath}/${dashFileName}`;
      mapStr += mapDash;
      Logger.log('[Transmuxing DASH] ' + this.conf.streamPath + ' to ' + ouPath + '/' + dashFileName);
    }
    mkdirp.sync(ouPath);
    let argv = ['-y', '-i', inPath];
    Array.prototype.push.apply(argv, ['-c:v', vc]);
    Array.prototype.push.apply(argv, this.conf.vcParam);
    Array.prototype.push.apply(argv, ['-c:a', ac]);
    Array.prototype.push.apply(argv, this.conf.acParam);
    Array.prototype.push.apply(argv, ['-f', 'tee', '-map', '0:a?', '-map', '0:v?', mapStr]);
    argv = argv.filter(n => {
      return n;
    }); //去空

    this.ffmpegs = {
      trans: spawn(this.conf.ffmpeg, argv),
      dump: null,
    };

    this.ffmpegs.trans = spawn(this.conf.ffmpeg, argv);
    this.ffmpegs.trans.on('error', e => {
      Logger.ffdebug(e);
    });
    this.ffmpegs.trans.stdout.on('data', data => {
      Logger.ffdebug(`FF输出：${data}`);
    });
    this.ffmpegs.trans.stderr.on('data', data => {
      Logger.ffdebug(`FF输出：${data}`);
    });
    this.ffmpegs.trans.on('close', code => {
      Logger.log('[Transmuxing end] ' + this.conf.streamPath);
      this.emit('end');
      fs.readdir(ouPath, function (err, files) {
        if (!err) {
          files.forEach(filename => {
            if (
              filename.endsWith('.ts') ||
              filename.endsWith('.m3u8') ||
              filename.endsWith('.mpd') ||
              filename.endsWith('.m4s') ||
              filename.endsWith('.tmp')
            ) {
              fs.unlinkSync(ouPath + '/' + filename);
            }
          });
        }
      });
    });

    if (this.conf.dumping) {
      this.startDumping();
    }
  }

  startDumping() {
    if (!this.conf.mp4Flags) {
      console.error('Missing mp4Flags!');
      return;
    }

    // Ogarnianie ścieżek, ustawienie nazwy pliku
    const vc = this.conf.vc || 'copy';
    const ac = this.conf.ac || 'copy';
    const inPath = 'rtmp://127.0.0.1:' + this.conf.rtmpPort + this.conf.streamPath;
    const ouPath = `${this.conf.mediaroot}/${this.conf.streamApp}/${this.conf.streamName}`;
    this.conf.mp4Flags = this.conf.mp4Flags ? this.conf.mp4Flags : '';
    const mp4FileName = dateFormat('yyyy-mm-dd-HH-MM-ss') + '.mp4';
    const mapStr = `${this.conf.mp4Flags}${ouPath}/${mp4FileName}`;

    // Parametry przekazywane FFMPEG
    let argv = [
      '-y',
      '-i',
      inPath,
      '-c:v',
      vc,
      this.conf.vcParam,
      '-c:a',
      ac,
      this.conf.acParam,
      '-f',
      'tee',
      '-map',
      '0:a?',
      '-map',
      '0:v?',
      mapStr,
    ];

    // Usuwanie pustych wartości, jeżeli zostały podane
    argv = argv.filter(n => n != null);

    // Uruchamianie FFMPEG
    console.log('running mp4');
    this.ffmpegs.dump = spawn(this.conf.ffmpeg, argv);
    this.ffmpegs.dump.on('close', () => {
      console.log('[!!! - Dumping end] ' + this.conf.streamPath);
    });
    console.log('[!!! - Dumping MP4] ' + this.conf.streamPath + ' to ' + ouPath + '/' + mp4FileName);
  }

  stopDumping() {
    if (!this.ffmpegs.dump) {
      console.error('Dumping was not started!');
      return;
    }

    // Zabicie FFMPEG odpowiedzialnego za zapis do MP4
    this.ffmpegs.dump.kill();
  }

  end() {
    if (this.ffmpegs.dump) {
      this.ffmpegs.dump.kill();
    }
    this.ffmpegs.trans.kill();
  }
}

module.exports = NodeTransSession;
