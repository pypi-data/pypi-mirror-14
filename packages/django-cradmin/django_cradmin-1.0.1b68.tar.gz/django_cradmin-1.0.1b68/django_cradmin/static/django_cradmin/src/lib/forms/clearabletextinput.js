(function() {
  angular.module('djangoCradmin.forms.clearabletextinput', []).directive('djangoCradminClearableTextinput', [
    function() {
      return {
        restrict: 'A',
        link: function($scope, $element, attributes) {
          var $target, onTargetValueChange, targetElementSelector;
          targetElementSelector = attributes.djangoCradminClearableTextinput;
          $target = angular.element(targetElementSelector);
          onTargetValueChange = function() {
            if ($target.val() === '') {
              return $element.removeClass('django-cradmin-clearable-textinput-button-visible');
            } else {
              return $element.addClass('django-cradmin-clearable-textinput-button-visible');
            }
          };
          $element.on('click', function(e) {
            e.preventDefault();
            $target.val('');
            $target.focus();
            return $target.change();
          });
          $target.on('change', function() {
            return onTargetValueChange();
          });
          $target.on('keydown', function(e) {
            return onTargetValueChange();
          });
          return onTargetValueChange();
        }
      };
    }
  ]);

}).call(this);
