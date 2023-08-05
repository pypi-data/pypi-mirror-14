(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  angular.module('djangoCradmin.providers', []).provider('djangoCradminWindowDimensions', function() {
    /** Provider that makes it easy to listen for window resize.
    
    How it works
    ============
    You register a ``scope`` with the provider. Each time the window
    is resized, the provider will call ``scope.onWindowResize()``.
    The provider uses a ``300ms`` timeout before it triggers a
    resize, so your ``onWindowResize`` method will not be flooded
    with every pixel change.
    
    Example
    =======
    
    ```coffeescript
    mymodule.directive('myDirective', [
      'djangoCradminWindowDimensions'
      (djangoCradminWindowDimensions) ->
        return {
          controller: ($scope) ->
            $scope.onWindowResize = (newWindowDimensions) ->
              console.log 'Window was resized to', newWindowDimensions
            return
    
          link: ($scope, element, attrs) ->
            djangoCradminWindowDimensions.register $scope
            $scope.$on '$destroy', ->
              djangoCradminWindowDimensions.unregister $scope
            return
        }
    ])
    ```
    */

    var WindowDimensionsProvider;
    WindowDimensionsProvider = (function() {
      function WindowDimensionsProvider($window, timeout) {
        this.timeout = timeout;
        this._onWindowResize = __bind(this._onWindowResize, this);
        this.mainWindow = angular.element($window);
        this.deviceMinWidths = {
          tablet: 768,
          mediumDesktop: 992,
          largeDesktop: 1200
        };
        this.windowDimensions = this._getWindowDimensions();
        this.applyResizeTimer = null;
        this.applyResizeTimerTimeoutMs = 300;
        this.listeningScopes = [];
      }

      WindowDimensionsProvider.prototype._triggerResizeEventsForScope = function(scope) {
        return scope.onWindowResize(this.windowDimensions);
      };

      WindowDimensionsProvider.prototype.register = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex !== -1) {
          console.error('Trying to register a scope that is already registered with ' + 'djangoCradminWindowDimensions. Scope:', scope);
          return;
        }
        if (this.listeningScopes.length < 1) {
          this.mainWindow.bind('resize', this._onWindowResize);
        }
        return this.listeningScopes.push(scope);
      };

      WindowDimensionsProvider.prototype.unregister = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex === -1) {
          console.error('Trying to unregister a scope that is not registered with ' + 'djangoCradminWindowDimensions. Scope:', scope);
        }
        this.listeningScopes.splice(scopeIndex, 1);
        if (this.listeningScopes.length < 1) {
          return this.mainWindow.unbind('resize', this._onWindowResize);
        }
      };

      WindowDimensionsProvider.prototype._getWindowDimensions = function() {
        return {
          height: this.mainWindow.height(),
          width: this.mainWindow.width()
        };
      };

      WindowDimensionsProvider.prototype.getDeviceFromWindowDimensions = function(windowDimensions) {
        if (windowDimensions < this.deviceMinWidths.tablet) {
          return 'phone';
        } else if (windowDimensions < this.deviceMinWidths.mediumDesktop) {
          return 'tablet';
        } else if (windowDimensions < this.deviceMinWidths.largeDesktop) {
          return 'medium-desktop';
        } else {
          return 'large-desktop';
        }
      };

      WindowDimensionsProvider.prototype._updateWindowDimensions = function(newWindowDimensions) {
        this.windowDimensions = newWindowDimensions;
        return this._onWindowDimensionsChange();
      };

      WindowDimensionsProvider.prototype._setWindowDimensions = function() {
        var newWindowDimensions;
        newWindowDimensions = this._getWindowDimensions();
        if (!angular.equals(newWindowDimensions, this.windowDimensions)) {
          return this._updateWindowDimensions(newWindowDimensions);
        }
      };

      WindowDimensionsProvider.prototype._onWindowDimensionsChange = function() {
        var scope, _i, _len, _ref, _results;
        _ref = this.listeningScopes;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          scope = _ref[_i];
          _results.push(this._triggerResizeEventsForScope(scope));
        }
        return _results;
      };

      WindowDimensionsProvider.prototype.triggerWindowResizeEvent = function() {
        return this._onWindowDimensionsChange();
      };

      WindowDimensionsProvider.prototype._onWindowResize = function() {
        var _this = this;
        this.timeout.cancel(this.applyResizeTimer);
        return this.applyResizeTimer = this.timeout(function() {
          return _this._setWindowDimensions();
        }, this.applyResizeTimerTimeoutMs);
      };

      return WindowDimensionsProvider;

    })();
    this.$get = [
      '$window', '$timeout', function($window, $timeout) {
        return new WindowDimensionsProvider($window, $timeout);
      }
    ];
    return this;
  }).provider('djangoCradminWindowScrollTop', function() {
    /** Provider that makes it easy to listen for scrolling on the main window.
    
    How it works
    ============
    You register a ``scope`` with the provider. Each time the window
    is scrolled, the provider will call ``scope.onWindowScrollTop()``.
    The provider uses a ``100ms`` timeout before it triggers a
    resize, so your ``onWindowScrollTop`` method will not be flooded
    with every pixel change.
    
    Example
    =======
    
    ```coffeescript
    mymodule.directive('myDirective', [
      'djangoCradminWindowScrollTop'
      (djangoCradminWindowScrollTop) ->
        return {
          controller: ($scope) ->
            $scope.onWindowScrollTop = (newTopPosition) ->
              console.log 'Window was scrolled to', newTopPosition
            return
    
          link: ($scope, element, attrs) ->
            djangoCradminWindowScrollTop.register $scope
            $scope.$on '$destroy', ->
              djangoCradminWindowScrollTop.unregister $scope
            return
        }
    ])
    ```
    */

    var WindowScrollProvider;
    WindowScrollProvider = (function() {
      function WindowScrollProvider($window, timeout) {
        this.timeout = timeout;
        this._onScroll = __bind(this._onScroll, this);
        this.mainWindow = angular.element($window);
        this.scrollTopPosition = this._getScrollTopPosition();
        this.applyScrollTimer = null;
        this.applyScrollTimerTimeoutMs = 50;
        this.listeningScopes = [];
        this.isScrolling = false;
      }

      WindowScrollProvider.prototype.register = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex !== -1) {
          console.error('Trying to register a scope that is already registered with ' + 'djangoCradminWindowScrollTop. Scope:', scope);
          return;
        }
        if (this.listeningScopes.length < 1) {
          this.mainWindow.bind('scroll', this._onScroll);
        }
        this.listeningScopes.push(scope);
        return scope.onWindowScrollTop(this.scrollTopPosition, true);
      };

      WindowScrollProvider.prototype.unregister = function(scope) {
        var scopeIndex;
        scopeIndex = this.listeningScopes.indexOf(scope);
        if (scopeIndex === -1) {
          console.error('Trying to unregister a scope that is not registered with ' + 'djangoCradminWindowScrollTop. Scope:', scope);
        }
        this.listeningScopes.splice(scopeIndex, 1);
        if (this.listeningScopes.length < 1) {
          return this.mainWindow.unbind('scroll', this._onScroll);
        }
      };

      WindowScrollProvider.prototype._getScrollTopPosition = function() {
        return this.mainWindow.scrollTop();
      };

      WindowScrollProvider.prototype._setScrollTopPosition = function() {
        var scrollTopPosition;
        scrollTopPosition = this._getScrollTopPosition();
        if (scrollTopPosition !== this.scrollTopPosition) {
          this.scrollTopPosition = scrollTopPosition;
          return this._onScrollTopChange();
        }
      };

      WindowScrollProvider.prototype._onScrollTopChange = function() {
        var scope, _i, _len, _ref, _results;
        _ref = this.listeningScopes;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          scope = _ref[_i];
          _results.push(scope.onWindowScrollTop(this.scrollTopPosition));
        }
        return _results;
      };

      WindowScrollProvider.prototype._notifyScrollStarted = function() {
        var scope, scrollTopPosition, _i, _len, _ref, _results;
        scrollTopPosition = this._getScrollTopPosition();
        if (scrollTopPosition !== this.scrollTopPosition) {
          _ref = this.listeningScopes;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            scope = _ref[_i];
            if (scope.onWindowScrollTopStart != null) {
              _results.push(scope.onWindowScrollTopStart());
            } else {
              _results.push(void 0);
            }
          }
          return _results;
        }
      };

      WindowScrollProvider.prototype._onScroll = function() {
        var _this = this;
        this.timeout.cancel(this.applyScrollTimer);
        if (!this.isScrolling) {
          this._notifyScrollStarted();
        }
        this.isScrolling = true;
        return this.applyScrollTimer = this.timeout(function() {
          _this._setScrollTopPosition();
          return _this.isScrolling = false;
        }, this.applyScrollTimerTimeoutMs);
      };

      return WindowScrollProvider;

    })();
    this.$get = [
      '$window', '$timeout', function($window, $timeout) {
        return new WindowScrollProvider($window, $timeout);
      }
    ];
    return this;
  });

}).call(this);
