/**
 * brush.js - Monitor Menlo optical frequency combs
 */

/** Convenience function for retrieving a JSON response. */
function getJSON(url, timeout) {
  var promise = new Promise(
    function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url);
      xhr.timeout = timeout || 100;

      xhr.ontimeout = function (e) {
        reject(e);
      };

      xhr.onload = function () {
        if (xhr.status == 200) {
          var data = JSON.parse(xhr.responseText);
          resolve(data);
        } else {
          reject(new Error(xhr.statusText));
        }
      };

      xhr.onerror = function (e) {
        reject(e);
      };

      xhr.send();
    }
  );
  return promise;
}

/** Controller for displaying errors and other information. */
var Notifications = {
  serverReachable: function (state) {
    var el = document.querySelector('#server-unavailable-notif');
    el.style.visibility = state ? 'hidden' : 'visible';
  }
};

/** Controller for the status page. */
var Status = {
  /** Update current displayed values. */
  update: function (data) {
    _.forEach(['reprate_freq', 'offset_freq'], function (key) {
      var color, glyph, lockbox;
      document.querySelector(`#${key}-current`).innerHTML = data[key].toFixed(4);

      lockbox = key == 'reprate_freq' ? 'lb1_status' : 'lb2_status';
      if (data[lockbox] != 0) {
        color = 'green';
        glyph = 'glyphicon-ok-circle';
      } else {
        color = 'red';
        glyph = 'glyphicon-ban-circle';
      }
      document.querySelector(`#${key}-locked`).className = `glyphicon ${glyph} ${color}`;
    });
  },

  getCurrentData: function () {
    getJSON('/data/current')
      .then(function (data) {
        Status.update(data);
      })
      .then(function () {
        Notifications.serverReachable(true);
        window.setTimeout(Status.getCurrentData, 1000);
      })
      .catch(function (error) {
        console.error(error);
        console.log("Error in getting current data. Try again in 5 s...");
        Notifications.serverReachable(false);
        window.setTimeout(Status.getCurrentData, 5000);
      });
  },

  run: function () {
    this.getCurrentData();
  }
};

window.onload = function () {
  if (window.location.pathname == '/') {
    Status.run();
  }
};
