(function() {
  angular.module('djangoCradmin.multiselect2.directives', []).directive('djangoCradminMultiselect2Target', [
    'djangoCradminMultiselect2Coordinator', '$window', function(djangoCradminMultiselect2Coordinator, $window) {
      return {
        restrict: 'A',
        scope: true,
        controller: function($scope, $element) {
          var domId;
          domId = $element.attr('id');
          $scope.selectedItemsScope = null;
          if (domId == null) {
            throw Error('Elements using django-cradmin-multiselect2-target must have an id.');
          }
          djangoCradminMultiselect2Coordinator.registerTarget(domId, $scope);
          $scope.$on("$destroy", function() {
            return djangoCradminMultiselect2Coordinator.unregisterTarget(domId);
          });
          $scope.select = function(selectScope) {
            /*
            Called by djangoCradminMultiselect2Select via
            djangoCradminMultiselect2Coordinator when an item is selected.
            
            Calls ``djangoCradminMultiselect2TargetSelectedItems.select()``.
            */

            $scope.selectedItemsScope.select(selectScope);
            if (!$scope.$$phase) {
              return $scope.$apply();
            }
          };
          $scope.isSelected = function(selectScope) {
            /*
            Called by djangoCradminMultiselect2Select via
            djangoCradminMultiselect2Coordinator to check if the item is selected.
            */

            return $scope.selectedItemsScope.isSelected(selectScope);
          };
          $scope.hasItems = function() {
            var _ref;
            return (_ref = $scope.selectedItemsScope) != null ? _ref.hasItems() : void 0;
          };
          this.setSelectedItemsScope = function(selectedItemsScope) {
            return $scope.selectedItemsScope = selectedItemsScope;
          };
          this.getSelectedItemsScope = function() {
            return $scope.selectedItemsScope;
          };
        },
        link: function($scope, $element, attributes) {
          var options;
          $scope.options = {
            updateFormActionToWindowLocation: false
          };
          if (attributes.djangoCradminMultiselect2Target !== '') {
            options = angular.fromJson(attributes.djangoCradminMultiselect2Target);
            angular.merge($scope.options, options);
          }
          $element.on('submit', function(e) {
            if ($scope.options.updateFormActionToWindowLocation) {
              return $element.attr('action', $window.location.href);
            }
          });
        }
      };
    }
  ]).directive('djangoCradminMultiselect2TargetSelectedItems', [
    '$compile', 'djangoCradminMultiselect2Coordinator', function($compile, djangoCradminMultiselect2Coordinator) {
      var selectedItemCssClass;
      selectedItemCssClass = 'django-cradmin-multiselect2-target-selected-item';
      return {
        restrict: 'A',
        require: '^djangoCradminMultiselect2Target',
        scope: true,
        controller: function($scope, $element) {
          $scope.selectedItemsCount = 0;
          $scope.selectedItemsData = {};
          $scope.select = function(selectScope) {
            var html, linkingFunction, loadedElement, previewHtml, selectButtonDomId;
            previewHtml = selectScope.getPreviewHtml();
            selectButtonDomId = selectScope.getDomId();
            html = ("<div id='" + selectButtonDomId + "_selected_item'") + ("django-cradmin-multiselect2-target-selected-item='" + selectButtonDomId + "' ") + ("class='" + selectedItemCssClass + "'>") + ("" + previewHtml + "</div>");
            linkingFunction = $compile(html);
            loadedElement = linkingFunction($scope);
            angular.element(loadedElement).appendTo($element);
            $scope.selectedItemsCount += 1;
            return $scope.selectedItemsData[selectButtonDomId] = selectScope.getCustomData();
          };
          $scope.deselectSelectedItem = function(selectedItemScope) {
            $scope.selectedItemsCount -= 1;
            delete $scope.selectedItemsData[selectedItemScope.selectButtonDomId];
            return djangoCradminMultiselect2Coordinator.onDeselect(selectedItemScope.selectButtonDomId);
          };
          $scope.isSelected = function(selectScope) {
            var selectButtonDomId;
            selectButtonDomId = selectScope.getDomId();
            return $element.find("#" + selectButtonDomId + "_selected_item").length > 0;
          };
          $scope.hasItems = function() {
            return $scope.selectedItemsCount > 0;
          };
          $scope.getItemsCustomDataList = function() {
            var customData, customDataList, selectButtonDomId, _ref;
            customDataList = [];
            _ref = $scope.selectedItemsData;
            for (selectButtonDomId in _ref) {
              customData = _ref[selectButtonDomId];
              customDataList.push(customData);
            }
            return customDataList;
          };
        },
        link: function($scope, $element, attributes, targetCtrl) {
          targetCtrl.setSelectedItemsScope($scope);
        }
      };
    }
  ]).directive('djangoCradminMultiselect2TargetSelectedItem', [
    'djangoCradminMultiselect2Coordinator', function(djangoCradminMultiselect2Coordinator) {
      return {
        restrict: 'A',
        scope: true,
        controller: function($scope, $element) {
          $scope.deselect = function() {
            $element.remove();
            $scope.deselectSelectedItem($scope);
          };
        },
        link: function($scope, $element, attributes) {
          $scope.selectButtonDomId = attributes.djangoCradminMultiselect2TargetSelectedItem;
        }
      };
    }
  ]).directive('djangoCradminMultiselect2Select', [
    '$rootScope', 'djangoCradminMultiselect2Coordinator', function($rootScope, djangoCradminMultiselect2Coordinator) {
      var itemWrapperSelectedCssClass;
      itemWrapperSelectedCssClass = 'django-cradmin-multiselect2-item-wrapper-selected';
      return {
        restrict: 'A',
        scope: {
          options: '=djangoCradminMultiselect2Select'
        },
        controller: function($scope, $element) {
          var unregisterBgReplaceEventHandler;
          $scope.getPreviewHtml = function() {
            var $containerElement, $previewElement;
            $containerElement = $element.parents($scope.options.preview_container_css_selector);
            $previewElement = $containerElement.find($scope.options.preview_css_selector);
            return $previewElement.html();
          };
          $scope.getDomId = function() {
            return $element.attr('id');
          };
          $scope.getListElementCssSelector = function() {
            return $scope.options.listelement_css_selector;
          };
          $scope.onDeselect = function() {
            /*
            Called by djangoCradminMultiselect2Coordinator when the item is deselected.
            */

            return $scope.getItemWrapperElement().removeClass(itemWrapperSelectedCssClass);
          };
          $scope.markAsSelected = function() {
            return $scope.getItemWrapperElement().addClass(itemWrapperSelectedCssClass);
          };
          $scope.getItemWrapperElement = function() {
            return $element.closest($scope.options.item_wrapper_css_selector);
          };
          $scope.getTargetDomId = function() {
            return $scope.options.target_dom_id;
          };
          $scope.getCustomData = function() {
            if ($scope.options.custom_data != null) {
              return $scope.options.custom_data;
            } else {
              return {};
            }
          };
          unregisterBgReplaceEventHandler = $scope.$on('djangoCradminBgReplaceElementEvent', function(event, options) {
            var targetDomId;
            if ($element.closest(options.remoteElementSelector).length > 0) {
              targetDomId = $scope.options.target_dom_id;
              if (djangoCradminMultiselect2Coordinator.isSelected(targetDomId, $scope)) {
                return $scope.markAsSelected();
              }
            }
          });
          djangoCradminMultiselect2Coordinator.registerSelectScope($scope);
          $scope.$on('$destroy', function() {
            unregisterBgReplaceEventHandler();
            return djangoCradminMultiselect2Coordinator.unregisterSelectScope($scope);
          });
        },
        link: function($scope, $element, attributes) {
          var select, targetScopeExistsWatcherCancel;
          select = function() {
            return djangoCradminMultiselect2Coordinator.select($scope);
          };
          if ($scope.options.is_selected) {
            if (djangoCradminMultiselect2Coordinator.targetScopeExists($scope.getTargetDomId())) {
              select();
            } else {
              targetScopeExistsWatcherCancel = $scope.$watch(function() {
                return djangoCradminMultiselect2Coordinator.targetScopeExists($scope.getTargetDomId());
              }, function(newValue, oldValue) {
                if (newValue) {
                  select();
                  return targetScopeExistsWatcherCancel();
                }
              });
            }
          }
          $element.on('click', function(e) {
            e.preventDefault();
            return select();
          });
        }
      };
    }
  ]).directive('djangoCradminMultiselect2Selectall', [
    '$rootScope', 'djangoCradminMultiselect2Coordinator', function($rootScope, djangoCradminMultiselect2Coordinator) {
      return {
        restrict: 'A',
        scope: true,
        controller: function($scope, $element) {},
        link: function($scope, $element, attributes) {
          var selectAll, targetDomId;
          $scope.options = angular.fromJson(attributes.djangoCradminMultiselect2Selectall);
          targetDomId = $scope.options.target_dom_id;
          selectAll = function() {
            return djangoCradminMultiselect2Coordinator.selectAll(targetDomId);
          };
          $element.on('click', function(e) {
            e.preventDefault();
            return $scope.pagerLoad({
              onSuccess: function() {
                return selectAll();
              }
            });
          });
        }
      };
    }
  ]).directive('djangoCradminMultiselect2UseThis', [
    '$window', function($window) {
      /*
      The ``django-cradmin-multiselect2-use-this`` directive is used to select elements for
      the ``django-cradmin-model-choice-field`` directive. You add this directive
      to a button or a-element within an iframe, and this directive will use
      ``window.postMessage`` to send the needed information to the
      ``django-cradmin-model-choice-field-wrapper``.
      
      You may also use this if you create your own custom iframe communication
      receiver directive where a "use this" button within an iframe is needed.
      
      Example
      =======
      ```
        <button type="button"
                class="btn btn-default"
                django-cradmin-multiselect2-use-this='{"fieldid": "id_name"}'>
            Use this
        </button>
      ```
      
      How it works
      ============
      When the user clicks an element with this directive, the click
      is captured, the default action is prevented, and we decode the
      given JSON encoded value and add ``postmessageid='django-cradmin-use-this'``
      to the object making it look something like this::
      
        ```
        {
          postmessageid: 'django-cradmin-use-this',
          value: '<JSON encoded data for the selected items>',
          preview: '<preview HTML for the selected items>'
          <all options provided to the directive>
        }
        ```
      
      We assume there is a event listener listening for the ``message`` event on
      the message in the parent of the iframe where this was clicked, but no checks
      ensuring this is made.
      */

      return {
        restrict: 'A',
        require: '^djangoCradminMultiselect2Target',
        scope: {
          data: '@djangoCradminMultiselect2UseThis'
        },
        link: function($scope, $element, attributes, targetCtrl) {
          var getSelectedItemsData;
          getSelectedItemsData = function() {
            var allData, itemData, _i, _len, _ref;
            allData = {
              values: [],
              preview: ""
            };
            _ref = targetCtrl.getSelectedItemsScope().getItemsCustomDataList();
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              itemData = _ref[_i];
              allData.values.push(itemData.value);
              allData.preview += itemData.preview;
            }
            return allData;
          };
          $element.on('click', function(e) {
            var data, selectedItemsData;
            e.preventDefault();
            data = angular.fromJson($scope.data);
            data.postmessageid = 'django-cradmin-use-this';
            selectedItemsData = getSelectedItemsData();
            data.value = angular.toJson(selectedItemsData.values);
            data.preview = selectedItemsData.preview;
            return $window.parent.postMessage(angular.toJson(data), window.parent.location.href);
          });
        }
      };
    }
  ]);

}).call(this);
