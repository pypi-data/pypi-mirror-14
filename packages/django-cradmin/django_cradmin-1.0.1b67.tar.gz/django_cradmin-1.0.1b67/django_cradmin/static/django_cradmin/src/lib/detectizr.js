(function() {
  angular.module('djangoCradmin.detectizr', []).factory('cradminDetectize', function() {
    Detectizr.detect({
      addAllFeaturesAsClass: false,
      detectDevice: true,
      detectDeviceModel: true,
      detectScreen: true,
      detectOS: true,
      detectBrowser: true,
      detectPlugins: false
    });
    return Detectizr;
  });

}).call(this);
