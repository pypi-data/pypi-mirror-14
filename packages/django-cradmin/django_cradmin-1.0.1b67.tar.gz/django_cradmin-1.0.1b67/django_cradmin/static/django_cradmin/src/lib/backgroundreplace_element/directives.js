(function() {
  angular.module('djangoCradmin.backgroundreplace_element.directives', []).directive('djangoCradminBgReplaceElementOnPageLoad', [
    '$window', 'djangoCradminBgReplaceElement', function($window, djangoCradminBgReplaceElement) {
      /*
      This is just an example/debugging directive for djangoCradminBgReplaceElement.
      */

      return {
        restrict: 'A',
        controller: function($scope, $element) {},
        link: function($scope, $element, attributes) {
          var remoteElementSelector, remoteUrl;
          remoteElementSelector = attributes.djangoCradminRemoteElementSelector;
          remoteUrl = attributes.djangoCradminRemoteUrl;
          if (remoteElementSelector == null) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.error === "function") {
                console.error("You must include the 'django-cradmin-remote-element-id' attribute.");
              }
            }
          }
          if (remoteUrl == null) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.error === "function") {
                console.error("You must include the 'django-cradmin-remote-url' attribute.");
              }
            }
          }
          angular.element(document).ready(function() {
            console.log('load', remoteUrl, remoteElementSelector);
            return djangoCradminBgReplaceElement.load({
              parameters: {
                method: 'GET',
                url: remoteUrl
              },
              remoteElementSelector: remoteElementSelector,
              targetElement: $element,
              $scope: $scope,
              replace: true,
              onHttpError: function(response) {
                return console.log('ERROR', response);
              },
              onSuccess: function() {
                return console.log('Success!');
              },
              onFinish: function() {
                return console.log('Finish!');
              }
            });
          });
        }
      };
    }
  ]);

}).call(this);
