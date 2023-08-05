(function() {
  var app;

  app = angular.module('djangoCradmin.forms.filewidget', []);

  app.controller('CradminFileFieldController', function($scope, $filter) {
    $scope.init = function() {
      $scope.$watch('cradmin_filefield_has_value', function(newValue) {
        if (newValue != null) {
          if (newValue) {
            return $scope.cradmin_filefield_clearcheckbox_value = '';
          } else {
            return $scope.cradmin_filefield_clearcheckbox_value = 'checked';
          }
        }
      });
    };
    $scope.cradminClearFileField = function() {
      return $scope.cradmin_filefield_clear_value = true;
    };
    $scope.init();
  });

  app.directive('cradminFilefieldValue', function() {
    return {
      scope: false,
      link: function($scope, element, attributes) {
        var fileFieldElement, setupFileFieldChangeListener;
        $scope.cradmin_filefield_clear_value = false;
        fileFieldElement = element;
        if ((attributes.cradminFilefieldValue != null) && attributes.cradminFilefieldValue !== "") {
          $scope.cradmin_filefield_has_value = true;
          $scope.cradmin_filefield_has_original_value = true;
        }
        setupFileFieldChangeListener = function() {
          return fileFieldElement.bind('change', function(changeEvent) {
            var reader;
            reader = new FileReader;
            reader.onload = function(loadEvent) {
              $scope.$apply(function() {
                $scope.cradmin_filefield_has_value = true;
                $scope.cradmin_filefield_has_original_value = false;
              });
            };
            reader.readAsDataURL(changeEvent.target.files[0]);
          });
        };
        $scope.$watch('cradmin_filefield_clear_value', function(newValue) {
          var newFileFieldElement;
          if (newValue) {
            $scope.cradmin_filefield_has_value = false;
            $scope.cradmin_filefield_clear_value = false;
            $scope.cradmin_filefield_has_original_value = false;
            newFileFieldElement = fileFieldElement.clone();
            jQuery(fileFieldElement).replaceWith(newFileFieldElement);
            fileFieldElement = newFileFieldElement;
            return setupFileFieldChangeListener();
          }
        });
        setupFileFieldChangeListener();
      }
    };
  });

}).call(this);
