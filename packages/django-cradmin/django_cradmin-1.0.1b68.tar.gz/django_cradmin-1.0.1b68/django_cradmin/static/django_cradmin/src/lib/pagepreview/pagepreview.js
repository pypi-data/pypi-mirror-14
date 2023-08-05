(function() {
  angular.module('djangoCradmin.pagepreview', []).provider('djangoCradminPagePreview', function() {
    var PagePreview;
    PagePreview = (function() {
      function PagePreview() {
        this.pagePreviewWrapper = null;
        this.bodyContentWrapperElement = angular.element('#django_cradmin_bodycontentwrapper');
        this.bodyElement = angular.element('body');
      }

      PagePreview.prototype.registerPagePreviewWrapper = function(pagePreviewWrapper) {
        return this.pagePreviewWrapper = pagePreviewWrapper;
      };

      PagePreview.prototype.setPreviewConfig = function(previewConfig) {
        return this.pagePreviewWrapper.setPreviewConfig(previewConfig);
      };

      PagePreview.prototype.addBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.addClass(cssclass);
      };

      PagePreview.prototype.removeBodyContentWrapperClass = function(cssclass) {
        return this.bodyContentWrapperElement.removeClass(cssclass);
      };

      PagePreview.prototype.disableBodyScrolling = function() {
        return this.bodyElement.addClass('django-cradmin-noscroll');
      };

      PagePreview.prototype.enableBodyScrolling = function() {
        return this.bodyElement.removeClass('django-cradmin-noscroll');
      };

      return PagePreview;

    })();
    this.$get = function() {
      return new PagePreview();
    };
    return this;
  }).directive('djangoCradminPagePreviewWrapper', [
    '$window', '$timeout', 'djangoCradminPagePreview', function($window, $timeout, djangoCradminPagePreview) {
      /*
      A directive that shows a preview of a page in an iframe.
      value.
      
      Components:
      
        - A DIV using this directive (``django-cradmin-page-preview-wrapper``)
          with the following child elements:
          - A child DIV using the ``django-cradmin-page-preview-iframe-wrapper``
            directive with the following child elements:
            - A "Close" link/button using the ``django-cradmin-page-preview-iframe-closebutton`` directive.
            - A IFRAME element using the ``django-cradmin-page-preview-iframe`` directive.
          - A child element with one of the following directives:
            - ``django-cradmin-page-preview-open-on-page-load`` to show the preview when the page loads.
            - ``django-cradmin-page-preview-open-on-click`` to show the preview when the element is clicked.
      
      The outer wrapper (``django-cradmin-page-preview-wrapper``) coordinates everything.
      
      You can have one wrapper with many ``django-cradmin-page-preview-open-on-click`` directives.
      This is typically used in listings where each item in the list has its own preview button.
      Just wrap the entire list in a ``django-cradmin-page-preview-wrapper``, add the
      ``django-cradmin-page-preview-iframe-wrapper`` before the list, and a button/link with
      the ``django-cradmin-page-preview-open-on-click``-directive for each entry in the list.
      
      
      Example:
      
      ```
      <div django-cradmin-page-preview-wrapper>
          <div class="django-cradmin-floating-fullsize-iframe-wrapper"
               django-cradmin-page-preview-iframe-wrapper>
              <a href="#" class="django-cradmin-floating-fullsize-iframe-closebutton"
                 django-cradmin-page-preview-iframe-closebutton>
                  <span class="fa fa-close"></span>
                  <span class="sr-only">Close preview</span>
              </a>
              <div class="ng-hide django-cradmin-floating-fullsize-loadspinner">
                  <span class="fa fa-spinner fa-spin"></span>
              </div>
              <div class="django-cradmin-floating-fullsize-iframe-inner">
                  <iframe django-cradmin-page-preview-iframe></iframe>
              </div>
          </div>
      
          <div django-cradmin-page-preview-open-on-page-load="'/some/view'"></div>
      </div>
      ```
      */

      return {
        restrict: 'A',
        scope: {},
        controller: function($scope, djangoCradminPagePreview) {
          var previewConfigWaitingForStartup;
          djangoCradminPagePreview.registerPagePreviewWrapper(this);
          $scope.origin = "" + window.location.protocol + "//" + window.location.host;
          $scope.mainWindow = angular.element($window);
          $scope.windowDimensions = null;
          previewConfigWaitingForStartup = null;
          this.setIframeWrapper = function(iframeWrapperScope) {
            $scope.iframeWrapperScope = iframeWrapperScope;
            return this._readyCheck();
          };
          this.setIframe = function(iframeScope) {
            $scope.iframeScope = iframeScope;
            return this._readyCheck();
          };
          this.setNavbar = function(navbarScope) {
            $scope.navbarScope = navbarScope;
            return this._readyCheck();
          };
          this.setLoadSpinner = function(loadSpinnerScope) {
            $scope.loadSpinnerScope = loadSpinnerScope;
            return this._readyCheck();
          };
          this.setIframeWrapperInner = function(iframeInnerScope) {
            return $scope.iframeInnerScope = iframeInnerScope;
          };
          this.showNavbar = function() {
            return $scope.iframeWrapperScope.showNavbar();
          };
          this.setUrl = function(url) {
            $scope.loadSpinnerScope.show();
            $scope.iframeInnerScope.scrollToTop();
            return $scope.iframeScope.setUrl(url);
          };
          this._readyCheck = function() {
            var isReady;
            isReady = ($scope.iframeInnerScope != null) && ($scope.loadSpinnerScope != null) && ($scope.navbarScope != null) && ($scope.iframeScope != null) && ($scope.iframeWrapperScope != null);
            if (isReady) {
              return this._onReady();
            }
          };
          this._onReady = function() {
            if (previewConfigWaitingForStartup != null) {
              return this._applyPreviewConfig();
            }
          };
          this._applyPreviewConfig = function() {
            var url;
            url = previewConfigWaitingForStartup.urls[0].url;
            $scope.navbarScope.setConfig(previewConfigWaitingForStartup);
            $scope.iframeInnerScope.hide();
            previewConfigWaitingForStartup = null;
            this.showPreview();
            return this.setUrl(url);
          };
          this.setPreviewConfig = function(previewConfig) {
            /*
            Called once on startup
            */

            previewConfigWaitingForStartup = previewConfig;
            return this._readyCheck();
          };
          this.showPreview = function() {
            djangoCradminPagePreview.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
            $scope.iframeWrapperScope.show();
            return $scope.mainWindow.bind('resize', $scope.onWindowResize);
          };
          this.hidePreview = function() {
            $scope.iframeWrapperScope.hide();
            $scope.mainWindow.unbind('resize', $scope.onWindowResize);
            return djangoCradminPagePreview.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper');
          };
          this.onIframeLoaded = function() {
            $scope.iframeInnerScope.show();
            return $scope.loadSpinnerScope.hide();
          };
          $scope.getWindowDimensions = function() {
            return {
              height: $scope.mainWindow.height(),
              width: $scope.mainWindow.width()
            };
          };
          $scope.$watch('windowDimensions', (function(newSize, oldSize) {
            $scope.iframeScope.setIframeSize();
          }), true);
          $scope.onWindowResize = function() {
            $timeout.cancel($scope.applyResizeTimer);
            $scope.applyResizeTimer = $timeout(function() {
              $scope.windowDimensions = $scope.getWindowDimensions();
              return $scope.$apply();
            }, 300);
          };
        },
        link: function(scope, element) {}
      };
    }
  ]).directive('djangoCradminPagePreviewIframeWrapper', [
    '$window', 'djangoCradminPagePreview', function($window, djangoCradminPagePreview) {
      return {
        require: '^^djangoCradminPagePreviewWrapper',
        restrict: 'A',
        scope: {},
        controller: function($scope) {
          $scope.show = function() {
            $scope.iframeWrapperElement.addClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminPagePreview.disableBodyScrolling();
            return djangoCradminPagePreview.addBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
          };
          $scope.hide = function() {
            $scope.iframeWrapperElement.removeClass('django-cradmin-floating-fullsize-iframe-wrapper-show');
            djangoCradminPagePreview.enableBodyScrolling();
            return djangoCradminPagePreview.removeBodyContentWrapperClass('django-cradmin-floating-fullsize-iframe-bodycontentwrapper-push');
          };
          $scope.showNavbar = function() {
            return $scope.iframeWrapperElement.addClass('django-cradmin-floating-fullsize-iframe-wrapper-with-navbar');
          };
          $scope.scrollToTop = function() {
            return $scope.iframeWrapperElement.scrollTop(0);
          };
          this.hide = function() {
            return $scope.hide();
          };
          this.show = function() {
            return $scope.show();
          };
        },
        link: function(scope, element, attrs, wrapperCtrl) {
          scope.iframeWrapperElement = element;
          wrapperCtrl.setIframeWrapper(scope);
        }
      };
    }
  ]).directive('djangoCradminPagePreviewIframeWrapperInner', [
    '$window', function($window) {
      return {
        require: '^^djangoCradminPagePreviewWrapper',
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
  ]).directive('djangoCradminPagePreviewIframeClosebutton', function() {
    return {
      require: '^^djangoCradminPagePreviewWrapper',
      restrict: 'A',
      scope: {},
      link: function(scope, element, attrs, wrapperCtrl) {
        element.on('click', function(e) {
          e.preventDefault();
          return wrapperCtrl.hidePreview();
        });
      }
    };
  }).directive('djangoCradminPagePreviewLoadSpinner', function() {
    return {
      require: '^^djangoCradminPagePreviewWrapper',
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
  }).directive('djangoCradminPagePreviewNavbar', function() {
    return {
      require: '^^djangoCradminPagePreviewWrapper',
      restrict: 'A',
      scope: {
        mobileMenuHeader: '@djangoCradminPagePreviewNavbarMobileMenuHeader'
      },
      templateUrl: 'pagepreview/navbar.tpl.html',
      controller: function($scope) {
        $scope.activeIndex = 0;
        $scope.activeUrlConfig = null;
        $scope.setConfig = function(previewConfig) {
          if (previewConfig.urls.length > 1) {
            $scope.previewConfig = previewConfig;
            $scope.setActive(0);
            $scope.$apply();
            return $scope.wrapperCtrl.showNavbar();
          }
        };
        return $scope.setActive = function(index) {
          $scope.activeIndex = index;
          return $scope.activeUrlConfig = $scope.previewConfig.urls[$scope.activeIndex];
        };
      },
      link: function($scope, element, attrs, wrapperCtrl) {
        $scope.element = element;
        $scope.wrapperCtrl = wrapperCtrl;
        $scope.wrapperCtrl.setNavbar($scope);
        $scope.onNavlinkClick = function(e, index) {
          e.preventDefault();
          $scope.setActive(index);
          $scope.wrapperCtrl.setUrl($scope.previewConfig.urls[index].url);
        };
      }
    };
  }).directive('djangoCradminPagePreviewIframe', function() {
    return {
      require: '^^djangoCradminPagePreviewWrapper',
      restrict: 'A',
      scope: {},
      controller: function($scope) {
        $scope.setUrl = function(url) {
          $scope.element.attr('src', url);
          return $scope.resetIframeSize();
        };
        $scope.setIframeSize = function() {
          var iframeBodyHeight, iframeDocument, iframeWindow;
          iframeWindow = $scope.element.contents();
          iframeDocument = iframeWindow[0];
          if (iframeDocument != null) {
            iframeBodyHeight = iframeDocument.body.offsetHeight;
            return $scope.element.height(iframeBodyHeight + 60);
          }
        };
        return $scope.resetIframeSize = function() {
          return $scope.element.height('40px');
        };
      },
      link: function(scope, element, attrs, wrapperCtrl) {
        scope.element = element;
        wrapperCtrl.setIframe(scope);
        scope.element.on('load', function() {
          wrapperCtrl.onIframeLoaded();
          return scope.setIframeSize();
        });
      }
    };
  }).directive('djangoCradminPagePreviewOpenOnPageLoad', [
    'djangoCradminPagePreview', function(djangoCradminPagePreview) {
      /*
      A directive that opens the given URL in an iframe overlay instantly (on page load).
      */

      return {
        restrict: 'A',
        scope: {
          previewConfig: '=djangoCradminPagePreviewOpenOnPageLoad'
        },
        link: function(scope, element, attrs) {
          djangoCradminPagePreview.setPreviewConfig(scope.previewConfig);
        }
      };
    }
  ]).directive('djangoCradminPagePreviewOpenOnClick', [
    'djangoCradminPagePreview', function(djangoCradminPagePreview) {
      /*
      A directive that opens the given URL in an iframe overlay on click.
      */

      return {
        restrict: 'A',
        scope: {
          previewConfig: '=djangoCradminPagePreviewOpenOnClick'
        },
        link: function(scope, element, attrs) {
          element.on('click', function(e) {
            e.preventDefault();
            return djangoCradminPagePreview.setPreviewConfig(scope.previewConfig);
          });
        }
      };
    }
  ]);

}).call(this);
