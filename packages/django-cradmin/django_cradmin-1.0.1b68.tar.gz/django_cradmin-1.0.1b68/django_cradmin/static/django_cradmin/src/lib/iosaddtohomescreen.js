(function() {
  angular.module('djangoCradmin.iosaddtohomescreen', []).directive('iosAddToHomeScreen', [
    '$window', 'cradminDetectize', function($window, cradminDetectize) {
      return {
        transclude: true,
        template: '<div ng-transclude>This is my directive content</div>',
        link: function($scope, $element, attrs) {
          if (attrs.forceOs != null) {
            $scope.os = attrs.forceOs;
          } else {
            $scope.os = cradminDetectize.os.name;
          }
          if (attrs.forceBrowser != null) {
            $scope.browser = attrs.forceBrowser;
          } else {
            $scope.browser = cradminDetectize.browser.name;
          }
          if (attrs.forceDeviceModel != null) {
            $scope.deviceModel = attrs.forceDeviceModel;
          } else {
            $scope.deviceModel = cradminDetectize.device.model;
          }
          if ($scope.os === 'ios' && $scope.browser === 'safari') {
            $element.show();
          } else {
            $element.hide();
          }
        }
      };
    }
  ]);

}).call(this);
