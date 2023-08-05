(function() {
  angular.module('djangoCradmin.forms.clearvalue', []).directive('djangoCradminClearValue', [
    function() {
      return {
        restrict: 'A',
        link: function($scope, $element, attributes) {
          var $target, targetElementSelector;
          targetElementSelector = attributes.djangoCradminClearValue;
          $target = angular.element(targetElementSelector);
          return $element.on('click', function(e) {
            e.preventDefault();
            $target.val('');
            $target.focus();
            return $target.change();
          });
        }
      };
    }
  ]);

}).call(this);
