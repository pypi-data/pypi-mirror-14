(function() {
  angular.module('djangoCradmin.loadmorepager.directives', []).directive('djangoCradminLoadMorePager', [
    '$timeout', 'djangoCradminBgReplaceElement', 'djangoCradminLoadmorepagerCoordinator', function($timeout, djangoCradminBgReplaceElement, djangoCradminLoadmorepagerCoordinator) {
      var pagerWrapperCssSelector;
      pagerWrapperCssSelector = '.django-cradmin-loadmorepager';
      return {
        restrict: 'A',
        scope: true,
        controller: function($scope, $element) {
          $scope.loadmorePagerIsLoading = false;
          $scope.getNextPageNumber = function() {
            return $scope.loadmorePagerOptions.nextPageNumber;
          };
          $scope.pagerLoad = function(options) {
            var $targetElement, nextPageUrl, replaceMode, updatedQueryDictAttributes;
            options = angular.extend({}, $scope.loadmorePagerOptions, options);
            $scope.loadmorePagerIsLoading = true;
            $targetElement = angular.element(options.targetElementCssSelector);
            replaceMode = false;
            nextPageUrl = URI();
            updatedQueryDictAttributes = {};
            if (options.mode === "reloadPageOneOnLoad") {
              replaceMode = true;
            } else if (options.mode === "loadAllOnClick") {
              replaceMode = true;
              nextPageUrl.setSearch('disablePaging', "true");
            } else {
              nextPageUrl.setSearch(options.pageQueryStringAttribute, $scope.getNextPageNumber());
            }
            return djangoCradminBgReplaceElement.load({
              parameters: {
                method: 'GET',
                url: nextPageUrl.toString()
              },
              remoteElementSelector: options.targetElementCssSelector,
              targetElement: $targetElement,
              $scope: $scope,
              replace: replaceMode,
              onHttpError: function(response) {
                return typeof console !== "undefined" && console !== null ? typeof console.error === "function" ? console.error('ERROR loading page', response) : void 0 : void 0;
              },
              onSuccess: function($remoteHtmlDocument) {
                if (options.mode === "reloadPageOneOnLoad") {
                  $targetElement.removeClass('django-cradmin-loadmorepager-target-reloading-page1');
                } else {
                  $element.addClass('django-cradmin-loadmorepager-hidden');
                }
                if (options.onSuccess != null) {
                  return options.onSuccess();
                }
              },
              onFinish: function() {
                return $scope.loadmorePagerIsLoading = false;
              }
            });
          };
        },
        link: function($scope, $element, attributes) {
          var domId;
          $scope.loadmorePagerOptions = {
            pageQueryStringAttribute: "page",
            mode: "loadMoreOnClick"
          };
          if ((attributes.djangoCradminLoadMorePager != null) && attributes.djangoCradminLoadMorePager !== '') {
            angular.extend($scope.loadmorePagerOptions, angular.fromJson(attributes.djangoCradminLoadMorePager));
          }
          if ($scope.loadmorePagerOptions.targetElementCssSelector == null) {
            throw Error('Missing required option: targetElementCssSelector');
          }
          domId = $element.attr('id');
          djangoCradminLoadmorepagerCoordinator.registerPager(domId, $scope);
          $scope.$on("$destroy", function() {
            return djangoCradminLoadmorepagerCoordinator.unregisterPager(domId, $scope);
          });
          if ($scope.loadmorePagerOptions.mode === "reloadPageOneOnLoad") {
            $timeout(function() {
              return $scope.pagerLoad();
            }, 500);
          }
        }
      };
    }
  ]);

}).call(this);
