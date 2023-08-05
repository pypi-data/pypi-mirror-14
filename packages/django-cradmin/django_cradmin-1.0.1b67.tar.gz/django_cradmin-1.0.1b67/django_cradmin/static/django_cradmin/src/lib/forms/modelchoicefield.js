(function() {
  angular.module('djangoCradmin.forms.modelchoicefield', []).provider('djangoCradminModelChoiceFieldCoordinator', function() {
    var ModelChoiceFieldOverlay;
    ModelChoiceFieldOverlay = (function() {
      function ModelChoiceFieldOverlay(djangoCradminWindowDimensions) {
        this.djangoCradminWindowDimensions = djangoCradminWindowDimensions;
        this.modelChoiceFieldIframeWrapper = null;
        this.bodyContentWrapperElement = angular.element('#django_cradmin_bodycontentwrapper');
        this.bodyElement = angular.element('body');
      }

      ModelChoiceFieldOverlay.prototype.registerModeChoiceFieldIframeWrapper = function(modelChoiceFieldIframeWrapper) {
        return this.modelChoiceFieldIframeWrapper = modelChoiceFieldIframeWrapper;
      };

      ModelChoiceFieldOverlay.prototype.onChangeValueBegin = function(fieldWrapperScope) {
        return this.modelChoiceFieldIframeWrapper.onChangeValueBegin(fieldWrapperScope);
      };

      ModelChoiceFieldOverlay.prototype.addBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.addClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.removeBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.removeClass(cssclass);
      };

      ModelChoiceFieldOverlay.prototype.disableBodyScrolling = function() {
        return this.bodyElement.addClass('django-cradmin-noscroll');
      };

      ModelChoiceFieldOverlay.prototype.enableBodyScrolling = function() {
        this.bodyElement.removeClass('django-cradmin-noscroll');
        return this.djangoCradminWindowDimensions.triggerWindowResizeEvent();
      };

      return ModelChoiceFieldOverlay;

    })();
    this.$get = [
      'djangoCradminWindowDimensions', function(djangoCradminWindowDimensions) {
        return new ModelChoiceFieldOverlay(djangoCradminWindowDimensions);
      }
    ];
    return this;
  }).directive('djangoCradminModelChoiceFieldIframeWrapper', [
    '$window', '$timeout', 'djangoCradminModelChoiceFieldCoordinator', 'djangoCradminWindowDimensions', function($window, $timeout, djangoCradminModelChoiceFieldCoordinator, djangoCradminWindowDimensions) {
      return {
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.origin = "" + window.location.protocol + "//" + window.location.host;
          $scope.bodyElement = angular.element($window.document.body);
          djangoCradminModelChoiceFieldCoordinator.registerModeChoiceFieldIframeWrapper(this);
          this.setIframe = function(iframeScope) {
            return $scope.iframeScope = iframeScope;
          };
          this._setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this._setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.setLoadSpinner = function(loadSpinnerScope) {
            return $scope.loadSpinnerScope = loadSpinnerScope;
          };
          this.setIframeWrapperInner = function(iframeInnerScope) {
            return $scope.iframeInnerScope = iframeInnerScope;
          };
          this.onChangeValueBegin = function(fieldWrapperScope) {
            this._setField(fieldWrapperScope.fieldScope);
            this._setPreviewElement(fieldWrapperScope.previewElementScope);
            $scope.iframeScope.beforeShowingIframe(fieldWrapperScope.iframeSrc);
            return $scope.show();
          };
          this.onIframeLoadBegin = function() {
            return $scope.loadSpinnerScope.show();
          };
          this.onIframeLoaded = function() {
            $scope.iframeInnerScope.show();
            return $scope.loadSpinnerScope.hide();
          };
          $scope.onChangeValue = function(event) {
            var data;
            if (event.origin !== $scope.origin) {
              console.error("Message origin '" + event.origin + "' does not match current origin '" + $scope.origin + "'.");
              return;
            }
            data = angular.fromJson(event.data);
            if ($scope.fieldScope.fieldid !== data.fieldid) {
              return;
            }
            $scope.fieldScope.setValue(data.value);
            $scope.previewElementScope.setPreviewHtml(data.preview);
            $scope.hide();
            return $scope.iframeScope.afterFieldValueChange();
          };
          $window.addEventListener('message', $scope.onChangeValue, false);
          $scope.onWindowResize = function(newWindowDimensions) {
            return $scope.iframeScope.setIframeSize();
          };
          $scope.show = function() {
            $scope.iframeWrapperElement.addClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminModelChoiceFieldCoordinator.disableBodyScrolling();
            djangoCradminModelChoiceFieldCoordinator.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
            djangoCradminModelChoiceFieldCoordinator.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
            return djangoCradminWindowDimensions.register($scope);
          };
          $scope.hide = function() {
            $scope.iframeWrapperElement.removeClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminModelChoiceFieldCoordinator.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
            djangoCradminModelChoiceFieldCoordinator.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
            djangoCradminModelChoiceFieldCoordinator.enableBodyScrolling();
            $scope.iframeScope.onHide();
            return djangoCradminWindowDimensions.unregister($scope);
          };
          this.closeIframe = function() {
            return $scope.hide();
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.iframeWrapperElement = element;
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldIframeWrapperInner', [
    '$window', function($window) {
      return {
        require: '^^djangoCradminModelChoiceFieldIframeWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.scrollToTop = function() {
            return $scope.element.scrollTop(0);
          };
          $scope.show = function() {
            return $scope.element.removeClass('ng-hide');
          };
          $scope.hide = function() {
            return $scope.element.addClass('ng-hide');
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.element = element;
          wrapperCtrl.setIframeWrapperInner(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldIframeClosebutton', function() {
    return {
      require: '^djangoCradminModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      link: function(scope, element, attrs, iframeWrapperCtrl) {
        element.on('click', function(e) {
          e.preventDefault();
          return iframeWrapperCtrl.closeIframe();
        });
      }
    };
  }).directive('djangoCradminModelChoiceFieldLoadSpinner', function() {
    return {
      require: '^^djangoCradminModelChoiceFieldIframeWrapper',
      restrict: 'A',
      scope: {},
      controller: function($scope) {
        $scope.hide = function() {
          return $scope.element.addClass('ng-hide');
        };
        return $scope.show = function() {
          return $scope.element.removeClass('ng-hide');
        };
      },
      link: function(scope, element, attrs, wrapperCtrl) {
        scope.element = element;
        wrapperCtrl.setLoadSpinner(scope);
      }
    };
  }).directive('djangoCradminModelChoiceFieldIframe', [
    '$interval', function($interval) {
      return {
        require: '^djangoCradminModelChoiceFieldIframeWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          var currentScrollHeight, getIframeDocument, getIframeScrollHeight, getIframeWindow, resizeIfScrollHeightChanges, scrollHeightInterval, startScrollHeightInterval, stopScrollHeightInterval;
          scrollHeightInterval = null;
          currentScrollHeight = 0;
          getIframeWindow = function() {
            return $scope.element.contents();
          };
          getIframeDocument = function() {
            return getIframeWindow()[0];
          };
          getIframeScrollHeight = function() {
            var iframeDocument;
            iframeDocument = getIframeDocument();
            if ((iframeDocument != null ? iframeDocument.body : void 0) != null) {
              return iframeDocument.body.scrollHeight;
            } else {
              return 0;
            }
          };
          resizeIfScrollHeightChanges = function() {
            var newScrollHeight;
            newScrollHeight = getIframeScrollHeight();
            if (newScrollHeight !== currentScrollHeight) {
              currentScrollHeight = newScrollHeight;
              return $scope.setIframeSize();
            }
          };
          startScrollHeightInterval = function() {
            if (scrollHeightInterval == null) {
              return scrollHeightInterval = $interval(resizeIfScrollHeightChanges, 500);
            }
          };
          stopScrollHeightInterval = function() {
            if (scrollHeightInterval != null) {
              $interval.cancel(scrollHeightInterval);
              return scrollHeightInterval = null;
            }
          };
          $scope.onHide = function() {
            return stopScrollHeightInterval();
          };
          $scope.afterFieldValueChange = function() {
            return stopScrollHeightInterval();
          };
          $scope.beforeShowingIframe = function(iframeSrc) {
            var currentSrc;
            currentSrc = $scope.element.attr('src');
            if ((currentSrc == null) || currentSrc === '' || currentSrc !== iframeSrc) {
              $scope.loadedSrc = currentSrc;
              $scope.wrapperCtrl.onIframeLoadBegin();
              $scope.resetIframeSize();
              $scope.element.attr('src', iframeSrc);
            }
            return startScrollHeightInterval();
          };
          $scope.setIframeSize = function() {};
          $scope.resetIframeSize = function() {};
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.element = element;
          scope.wrapperCtrl = wrapperCtrl;
          wrapperCtrl.setIframe(scope);
          scope.element.on('load', function() {
            wrapperCtrl.onIframeLoaded();
            return scope.setIframeSize();
          });
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldWrapper', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        restrict: 'A',
        scope: {
          iframeSrc: '@djangoCradminModelChoiceFieldWrapper'
        },
        controller: function($scope) {
          this.setField = function(fieldScope) {
            return $scope.fieldScope = fieldScope;
          };
          this.setPreviewElement = function(previewElementScope) {
            return $scope.previewElementScope = previewElementScope;
          };
          this.onChangeValueBegin = function() {
            return djangoCradminModelChoiceFieldCoordinator.onChangeValueBegin($scope);
          };
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldInput', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setValue = function(value) {
            return $scope.inputElement.val(value);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.inputElement = element;
          scope.fieldid = attrs['id'];
          wrapperCtrl.setField(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldPreview', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.setPreviewHtml = function(previewHtml) {
            return $scope.previewElement.html(previewHtml);
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.previewElement = element;
          wrapperCtrl.setPreviewElement(scope);
        }
      };
    }
  ]).directive('djangoCradminModelChoiceFieldChangebeginButton', [
    'djangoCradminModelChoiceFieldCoordinator', function(djangoCradminModelChoiceFieldCoordinator) {
      return {
        require: '^^djangoCradminModelChoiceFieldWrapper',
        restrict: 'A',
        scope: {},
        link: function(scope, element, attrs, wrapperCtrl) {
          element.on('click', function(e) {
            e.preventDefault();
            return wrapperCtrl.onChangeValueBegin();
          });
        }
      };
    }
  ]);

}).call(this);
