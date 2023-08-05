(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  angular.module('djangoCradmin.backgroundreplace_element.providers', []).provider('djangoCradminBgReplaceElement', function() {
    /*
    Makes a request to a an URL, and replaces or extends a DOM element
    on the current page with the same DOM element within
    the requested URL.
    
    Can be used for many things, such as:
    
    - Infinite scroll (append content from ``?page=<pagenumber>``).
    - Live filtering (replace the filtered list when a filter changes).
    */

    var BgReplace;
    BgReplace = (function() {
      function BgReplace($http, $compile, $rootScope) {
        this.updateTargetElement = __bind(this.updateTargetElement, this);
        this.http = $http;
        this.compile = $compile;
        this.rootScope = $rootScope;
      }

      BgReplace.prototype.loadUrlAndExtractRemoteElementHtml = function(options, onSuccess) {
        var parsedUrl, url;
        url = options.parameters.url;
        parsedUrl = URI(url);
        parsedUrl.setSearch("cradmin-bgreplaced", 'true');
        options.parameters.url = parsedUrl.toString();
        return this.http(options.parameters).then(function(response) {
          var $remoteHtmlDocument, html, remoteElement, remoteElementInnerHtml;
          html = response.data;
          $remoteHtmlDocument = angular.element(html);
          remoteElement = $remoteHtmlDocument.find(options.remoteElementSelector);
          remoteElementInnerHtml = remoteElement.html();
          return onSuccess(remoteElementInnerHtml, $remoteHtmlDocument);
        }, function(response) {
          if (options.onFinish != null) {
            options.onFinish();
          }
          if (options.onHttpError != null) {
            return options.onHttpError(response);
          } else {
            return typeof console !== "undefined" && console !== null ? typeof console.error === "function" ? console.error("Failed to load", options.parameters) : void 0 : void 0;
          }
        });
      };

      BgReplace.prototype.__removeElement = function($element) {
        var $childElement, childDomElement, isolatedScope, _i, _len, _ref;
        _ref = $element.children();
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          childDomElement = _ref[_i];
          $childElement = angular.element(childDomElement);
          this.__removeElement($childElement);
        }
        isolatedScope = $element.isolateScope();
        if (isolatedScope != null) {
          isolatedScope.$destroy();
        }
        return $element.remove();
      };

      BgReplace.prototype.__removeAllChildren = function($element) {
        var $childElement, childDomElement, _i, _len, _ref, _results;
        _ref = $element.children();
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          childDomElement = _ref[_i];
          $childElement = angular.element(childDomElement);
          _results.push(this.__removeElement($childElement));
        }
        return _results;
      };

      BgReplace.prototype.updateTargetElement = function(options, remoteElementInnerHtml, $remoteHtmlDocument) {
        var $compile, linkingFunction, loadedElement;
        if (options.replace) {
          this.__removeAllChildren(options.targetElement);
        }
        $compile = this.compile;
        linkingFunction = $compile(remoteElementInnerHtml);
        loadedElement = linkingFunction(options.$scope);
        options.targetElement.append(loadedElement);
        if (options.onFinish != null) {
          options.onFinish();
        }
        if (options.onSuccess) {
          options.onSuccess($remoteHtmlDocument);
        }
        return this.rootScope.$broadcast('djangoCradminBgReplaceElementEvent', options);
      };

      BgReplace.prototype.load = function(options) {
        var me;
        me = this;
        return this.loadUrlAndExtractRemoteElementHtml(options, function(remoteElementInnerHtml, $remoteHtmlDocument) {
          return me.updateTargetElement(options, remoteElementInnerHtml, $remoteHtmlDocument);
        });
      };

      return BgReplace;

    })();
    this.$get = [
      '$http', '$compile', '$rootScope', function($http, $compile, $rootScope) {
        return new BgReplace($http, $compile, $rootScope);
      }
    ];
    return this;
  });

}).call(this);
