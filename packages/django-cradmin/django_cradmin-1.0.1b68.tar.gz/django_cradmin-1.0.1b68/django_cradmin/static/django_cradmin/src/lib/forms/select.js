(function() {
  angular.module('djangoCradmin.forms.select', []).directive('djangoCradminOpenUrlStoredInSelectedOption', [
    function() {
      return {
        restrict: 'A',
        link: function($scope, $element, attributes) {
          var getValue;
          getValue = function() {
            return $element.find("option:selected").attr('value');
          };
          return $element.on('change', function() {
            var remoteUrl;
            remoteUrl = getValue();
            return window.location = value;
          });
        }
      };
    }
  ]);

}).call(this);
