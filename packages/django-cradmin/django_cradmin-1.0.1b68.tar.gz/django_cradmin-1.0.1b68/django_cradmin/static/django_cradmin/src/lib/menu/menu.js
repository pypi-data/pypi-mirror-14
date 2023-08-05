(function() {
  angular.module('djangoCradmin.menu', []).directive('djangoCradminMenu', [
    function() {
      /** Menu that collapses automatically on small displays.
      
      Example
      =======
      
      ```html
      <nav django-cradmin-menu class="django-cradmin-menu">
        <div class="django-cradmin-menu-mobileheader">
          <a href="#" role="button"
              class="django-cradmin-menu-mobiletoggle"
              ng-click="cradminMenuTogglePressed()"
              ng-class="{'django-cradmin-menu-mobile-toggle-button-expanded': cradminMenuDisplay}"
              aria-pressed="{{ getAriaPressed() }}">
            Menu
          </a>
        </div>
        <div class="django-cradmin-menu-content"
            ng-class="{'django-cradmin-menu-content-display': cradminMenuDisplay}">
          <ul>
            <li><a href="#">Menu item 1</a></li>
            <li><a href="#">Menu item 2</a></li>
          </ul>
        </div>
      </nav>
      ```
      
      Design notes
      ============
      
      The example uses css classes provided by the default cradmin CSS, but
      you specify all classes yourself, so you can easily provide your own
      css classes and still use the directive.
      */

      return {
        scope: true,
        controller: function($scope, djangoCradminPagePreview) {
          $scope.cradminMenuDisplay = false;
          $scope.cradminMenuTogglePressed = function() {
            return $scope.cradminMenuDisplay = !$scope.cradminMenuDisplay;
          };
          $scope.getAriaPressed = function() {
            if ($scope.cradminMenuDisplay) {
              return 'pressed';
            } else {
              return '';
            }
          };
          this.close = function() {
            $scope.cradminMenuDisplay = false;
            return $scope.$apply();
          };
        }
      };
    }
  ]).directive('djangoCradminMenuAutodetectOverflowY', [
    'djangoCradminWindowDimensions', function(djangoCradminWindowDimensions) {
      /**
      */

      return {
        require: '?djangoCradminMenu',
        controller: function($scope) {
          var disableInitialWatcher;
          $scope.onWindowResize = function(newWindowDimensions) {
            return $scope.setOrUnsetOverflowYClass();
          };
          $scope.setOrUnsetOverflowYClass = function() {
            var menuDomElement, _ref;
            menuDomElement = (_ref = $scope.menuElement) != null ? _ref[0] : void 0;
            if (menuDomElement != null) {
              if (menuDomElement.clientHeight < menuDomElement.scrollHeight) {
                return $scope.menuElement.addClass($scope.overflowYClass);
              } else {
                return $scope.menuElement.removeClass($scope.overflowYClass);
              }
            }
          };
          disableInitialWatcher = $scope.$watch(function() {
            var _ref;
            if (((_ref = $scope.menuElement) != null ? _ref[0] : void 0) != null) {
              return true;
            } else {
              return false;
            }
          }, function(newValue) {
            if (newValue) {
              $scope.setOrUnsetOverflowYClass();
              return disableInitialWatcher();
            }
          });
        },
        link: function($scope, element, attrs) {
          $scope.overflowYClass = attrs.djangoCradminMenuAutodetectOverflowY;
          $scope.menuElement = element;
          djangoCradminWindowDimensions.register($scope);
          $scope.$on('$destroy', function() {
            return djangoCradminWindowDimensions.unregister($scope);
          });
        }
      };
    }
  ]).directive('djangoCradminMenuCloseOnClick', [
    function() {
      /** Directive that you can put on menu links to automatically close the
      menu on click.
      */

      return {
        require: '^^djangoCradminMenu',
        link: function(scope, element, attrs, djangoCradminMenuCtrl) {
          element.on('click', function() {
            djangoCradminMenuCtrl.close();
          });
        }
      };
    }
  ]);

}).call(this);
