import 'regenerator-runtime/runtime';

import showGaze from "../showGaze";

// npm module
//import EasySeeSo from 'seeso/easy-seeso';

const licenseKey = 'dev_ae171a1si0eryn930qa5hdu53j1q9t01zgkp41pj'; // Issue license key! -> https://console.seeso.io

// gaze callback.
function onGaze(gazeInfo) {
  // do something with gaze info.
  showGaze(gazeInfo)
}

// debug callback.
function onDebug(FPS, latency_min, latency_max, latency_avg){
  // do something with debug info.
}


async function main() {
  const seeSo = new EasySeeSo();
  /**
   * set monitor size.    default: 16 inch.
   * set face distance.   default: 30 cm.
   * set camera position. default:
   * camera x: right center
   * cameraOnTop: true
   */

  await seeSo.init(licenseKey,
      () => {
      seeSo.setMonitorSize(16);
      seeSo.setFaceDistance(50);
      seeSo.setCameraPosition(window.outerWidth / 2, true);
      seeSo.startTracking(onGaze, onDebug)
            }, // callback when init succeeded.
      () => console.log("callback when init failed"),  // callback when init failed.
  )
}

(async () => {
  await main();
})()
