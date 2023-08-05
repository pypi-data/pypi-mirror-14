(function() {
  angular.module('djangoCradmin.modal', []).directive('djangoCradminModalWrapper', [
    function() {
      /** Shows a modal window on click.
      
      Example
      =======
      
      ```html
      <div django-cradmin-modal-wrapper>
        <button ng-click="showModal($event)" type="button">
          Show modal window
        </button>
        <div django-cradmin-modal class="django-cradmin-modal"
                ng-class="{'django-cradmin-modal-visible': modalVisible}">
            <div class="django-cradmin-modal-backdrop" ng-click="hideModal()"></div>
            <div class="django-cradmin-modal-content">
                <p>Something here</p>
                <button ng-click="hideModal()" type="button">
                  Hide modal window
                </button>
            </div>
        </div>
      </div>
      ```
      */

      return {
        scope: true,
        controller: function($scope) {
          var bodyElement;
          $scope.modalVisible = false;
          bodyElement = angular.element('body');
          $scope.showModal = function(e) {
            if (e != null) {
              e.preventDefault();
            }
            $scope.modalVisible = true;
            bodyElement.addClass('django-cradmin-noscroll');
          };
          $scope.hideModal = function() {
            $scope.modalVisible = false;
            bodyElement.removeClass('django-cradmin-noscroll');
          };
        }
      };
    }
  ]).directive('djangoCradminModal', [
    function() {
      return {
        require: '^^djangoCradminModalWrapper',
        link: function($scope, element) {
          var body;
          body = angular.element('body');
          return element.appendTo(body);
        }
      };
    }
  ]);

}).call(this);
