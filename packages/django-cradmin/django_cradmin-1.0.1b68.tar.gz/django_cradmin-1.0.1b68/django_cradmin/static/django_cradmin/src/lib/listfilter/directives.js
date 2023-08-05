(function() {
  angular.module('djangoCradmin.listfilter.directives', []).directive('djangoCradminListfilter', [
    '$window', '$timeout', 'djangoCradminBgReplaceElement', function($window, $timeout, djangoCradminBgReplaceElement) {
      return {
        restrict: 'A',
        scope: {
          options: '=djangoCradminListfilter'
        },
        controller: function($scope, $element) {
          var $messageElement, filterListDomId, filterScopes, hideMessage, loadInProgress, onLoadSuccess, queueMessage, setLoadFinished, setLoadInProgress, showMessage, showMessageTimer;
          filterListDomId = $element.attr('id');
          filterScopes = [];
          loadInProgress = false;
          $messageElement = null;
          showMessageTimer = null;
          this.loadIsInProgress = function() {
            return loadInProgress;
          };
          setLoadInProgress = function(options) {
            var filterScope, _i, _len, _results;
            loadInProgress = true;
            $scope.targetElement.attr('aria-busy', 'true');
            _results = [];
            for (_i = 0, _len = filterScopes.length; _i < _len; _i++) {
              filterScope = filterScopes[_i];
              _results.push(filterScope.onLoadInProgress(options.filterDomId));
            }
            return _results;
          };
          setLoadFinished = function(options) {
            var filterScope, _i, _len;
            loadInProgress = false;
            for (_i = 0, _len = filterScopes.length; _i < _len; _i++) {
              filterScope = filterScopes[_i];
              filterScope.onLoadFinished(options.filterDomId);
            }
            return $scope.targetElement.attr('aria-busy', 'false');
          };
          onLoadSuccess = function($remoteHtmlDocument, remoteUrl) {
            var $remoteFilterList, filterScope, parsedRemoteUrl, title, _i, _len, _results;
            $remoteFilterList = $remoteHtmlDocument.find('#' + filterListDomId);
            title = $window.document.title;
            parsedRemoteUrl = URI(remoteUrl);
            parsedRemoteUrl.removeSearch('cradmin-bgreplaced').normalizeQuery();
            console.log(parsedRemoteUrl.toString());
            $window.history.pushState("list filter change", title, parsedRemoteUrl.toString());
            _results = [];
            for (_i = 0, _len = filterScopes.length; _i < _len; _i++) {
              filterScope = filterScopes[_i];
              _results.push(filterScope.syncWithRemoteFilterList($remoteFilterList));
            }
            return _results;
          };
          showMessage = function(variant, message) {
            var aria_role, loadspinner;
            hideMessage();
            $scope.targetElement.removeClass('django-cradmin-listfilter-target-loaderror');
            loadspinner = "";
            aria_role = 'alert';
            if (variant === 'error') {
              $scope.targetElement.addClass('django-cradmin-listfilter-target-loaderror');
              aria_role = 'alert';
            } else if (variant === 'loading') {
              $scope.targetElement.addClass('django-cradmin-listfilter-target-loading');
              aria_role = 'progressbar';
              if ($scope.options.loadspinner_css_class != null) {
                loadspinner = "<span class='django-cradmin-listfilter-message-loadspinner " + ("" + $scope.options.loadspinner_css_class + "' aria-hidden='true'></span>");
              }
            } else {
              throw new Error("Invalid message variant: " + variant);
            }
            $messageElement = angular.element(("<div aria-role='" + aria_role + "' ") + ("class='django-cradmin-listfilter-message django-cradmin-listfilter-message-" + variant + "'>") + ("" + loadspinner) + ("<span class='django-cradmin-listfilter-message-text'>" + message + "</span></div>"));
            return $messageElement.prependTo($scope.targetElement);
          };
          queueMessage = function(variant, message) {
            if (showMessageTimer != null) {
              $timeout.cancel(showMessageTimer);
            }
            return showMessageTimer = $timeout(function() {
              return showMessage(variant, message);
            }, $scope.options.loadingmessage_delay_milliseconds);
          };
          hideMessage = function() {
            if (showMessageTimer != null) {
              $timeout.cancel(showMessageTimer);
            }
            if ($messageElement) {
              $messageElement.remove();
              $messageElement = null;
            }
            return $scope.targetElement.removeClass('django-cradmin-listfilter-target-loading');
          };
          this.load = function(options) {
            setLoadInProgress(options);
            queueMessage('loading', options.loadingmessage);
            return djangoCradminBgReplaceElement.load({
              parameters: {
                method: 'GET',
                url: options.remoteUrl
              },
              remoteElementSelector: '#' + $scope.options.target_dom_id,
              targetElement: $scope.targetElement,
              $scope: $scope,
              replace: true,
              onHttpError: function(response) {
                if (typeof console !== "undefined" && console !== null) {
                  if (typeof console.error === "function") {
                    console.error('Error while filtering', response);
                  }
                }
                return showMessage('error', $scope.options.loaderror_message);
              },
              onSuccess: function($remoteHtmlDocument) {
                onLoadSuccess($remoteHtmlDocument, options.remoteUrl);
                if (options.onLoadSuccess != null) {
                  return options.onLoadSuccess(options.onLoadSuccessData);
                }
              },
              onFinish: function() {
                setLoadFinished(options);
                return hideMessage();
              }
            });
          };
          this.addFilterScope = function(filterScope) {
            return filterScopes.push(filterScope);
          };
        },
        link: function($scope, $element, attributes) {
          $scope.targetElement = angular.element('#' + $scope.options.target_dom_id);
          angular.element($window).on('popstate', function(e) {
            var state;
            state = e.originalEvent.state;
            if (state) {
              return $window.location.reload();
            }
          });
        }
      };
    }
  ]).directive('djangoCradminListfilterSelect', [
    function() {
      return {
        restrict: 'A',
        require: '^djangoCradminListfilter',
        scope: {
          options: '=djangoCradminListfilterSelect'
        },
        controller: function($scope, $element) {
          /*
          Replace all <option>-elements with new <option>-elements from the server.
          */

          $scope.syncWithRemoteFilterList = function($remoteFilterList) {
            var $remoteElement, domId;
            domId = $element.attr('id');
            $remoteElement = $remoteFilterList.find('#' + domId);
            $element.empty();
            return $element.append(angular.element($remoteElement.html()));
          };
          $scope.onLoadInProgress = function(filterDomId) {
            return $element.prop('disabled', true);
          };
          $scope.onLoadFinished = function(filterDomId) {
            return $element.prop('disabled', false);
          };
        },
        link: function($scope, $element, attributes, listfilterCtrl) {
          var getValue;
          listfilterCtrl.addFilterScope($scope);
          getValue = function() {
            return $element.find("option:selected").attr('value');
          };
          $element.on('change', function() {
            var remoteUrl;
            remoteUrl = getValue();
            return listfilterCtrl.load({
              remoteUrl: remoteUrl,
              filterDomId: $element.attr('id'),
              loadingmessage: $scope.options.loadingmessage,
              onLoadSuccess: function() {
                return $element.focus();
              }
            });
          });
        }
      };
    }
  ]).directive('djangoCradminListfilterTextinput', [
    '$timeout', function($timeout) {
      var emptyvalueUrlAttribute, urlpatternAttribute, urlpatternReplaceText;
      urlpatternAttribute = 'django-cradmin-listfilter-urlpattern';
      emptyvalueUrlAttribute = 'django-cradmin-listfilter-emptyvalue-url';
      urlpatternReplaceText = '_-_TEXTINPUT_-_VALUE_-_';
      return {
        restrict: 'A',
        require: '^djangoCradminListfilter',
        scope: {
          options: '=djangoCradminListfilterTextinput'
        },
        controller: function($scope, $element) {
          /*
          Update the "django-cradmin-listfilter-urlpattern"-attribute with
          the one from the server.
          */

          $scope.syncWithRemoteFilterList = function($remoteFilterList) {
            var $remoteElement, domId;
            domId = $element.attr('id');
            $remoteElement = $remoteFilterList.find('#' + domId);
            $element.attr(urlpatternAttribute, $remoteElement.attr(urlpatternAttribute));
            return $element.attr(emptyvalueUrlAttribute, $remoteElement.attr(emptyvalueUrlAttribute));
          };
          $scope.onLoadInProgress = function(filterDomId) {
            if (filterDomId !== $element.attr('id')) {
              return $element.prop('disabled', true);
            }
          };
          $scope.onLoadFinished = function(filterDomId) {
            return $element.prop('disabled', false);
          };
        },
        link: function($scope, $element, attributes, listfilterCtrl) {
          var applySearchTimer, buildUrl, loadSearch, loadedValue, onLoadSearchSuccess, onValueChange, timeoutMilliseconds;
          listfilterCtrl.addFilterScope($scope);
          applySearchTimer = null;
          loadedValue = $element.val();
          timeoutMilliseconds = $scope.options.timeout_milliseconds;
          if (timeoutMilliseconds == null) {
            timeoutMilliseconds = 500;
          }
          buildUrl = function(value) {
            var encodedValue, urlpattern;
            value = value.trim();
            if (value === '') {
              return $element.attr(emptyvalueUrlAttribute);
            } else {
              urlpattern = $element.attr(urlpatternAttribute);
              encodedValue = URI.encodeQuery(value);
              console.log(value);
              console.log(encodedValue);
              return urlpattern.replace($scope.options.urlpattern_replace_text, encodedValue);
            }
          };
          onLoadSearchSuccess = function(data) {
            var currentValue;
            currentValue = $element.val();
            if (data.value !== currentValue) {
              onValueChange(true);
            }
            return loadedValue = data.value;
          };
          loadSearch = function() {
            var remoteUrl, value;
            if (listfilterCtrl.loadIsInProgress()) {
              return;
            }
            value = $element.val();
            if (loadedValue === value) {
              return;
            }
            remoteUrl = buildUrl(value);
            loadedValue = value;
            return listfilterCtrl.load({
              remoteUrl: remoteUrl,
              onLoadSuccess: onLoadSearchSuccess,
              onLoadSuccessData: {
                value: value
              },
              filterDomId: $element.attr('id'),
              loadingmessage: $scope.options.loadingmessage
            });
          };
          onValueChange = function(useTimeout) {
            if (applySearchTimer != null) {
              $timeout.cancel(applySearchTimer);
            }
            if (!listfilterCtrl.loadIsInProgress()) {
              if (useTimeout) {
                return applySearchTimer = $timeout(loadSearch, timeoutMilliseconds);
              } else {
                return loadSearch();
              }
            }
          };
          $element.on('change', function() {
            return onValueChange(false);
          });
          $element.on('keydown', function(e) {
            if (e.which === 13) {
              return onValueChange(false);
            } else {
              return onValueChange(true);
            }
          });
        }
      };
    }
  ]).directive('djangoCradminListfilterCheckboxlist', [
    function() {
      return {
        restrict: 'A',
        require: '^djangoCradminListfilter',
        scope: {
          options: '=djangoCradminListfilterCheckboxlist'
        },
        controller: function($scope, $element) {
          /*
          Replace all contents with new elements from the server.
          */

          $scope.syncWithRemoteFilterList = function($remoteFilterList) {
            var $remoteElement, domId;
            domId = $element.attr('id');
            $remoteElement = $remoteFilterList.find('#' + domId);
            $element.empty();
            $element.append(angular.element($remoteElement.html()));
            return $scope.registerCheckboxChangeListeners(true);
          };
          $scope.onLoadInProgress = function(filterDomId) {
            return $element.find('input').prop('disabled', true);
          };
          $scope.onLoadFinished = function(filterDomId) {
            return $element.find('input').prop('disabled', false);
          };
        },
        link: function($scope, $element, attributes, listfilterCtrl) {
          var getUrl, onLoadSuccess;
          listfilterCtrl.addFilterScope($scope);
          getUrl = function($inputElement) {
            return $inputElement.attr('data-url');
          };
          onLoadSuccess = function(data) {
            return $element.find('#' + data.checkboxId).focus();
          };
          $scope.onCheckboxChange = function(e) {
            var checkboxId, remoteUrl;
            remoteUrl = getUrl(angular.element(e.target));
            checkboxId = angular.element(e.target).attr('id');
            return listfilterCtrl.load({
              remoteUrl: remoteUrl,
              filterDomId: $element.attr('id'),
              onLoadSuccess: onLoadSuccess,
              onLoadSuccessData: {
                checkboxId: checkboxId
              },
              loadingmessage: $scope.options.loadingmessage
            });
          };
          $scope.registerCheckboxChangeListeners = function(removeFirst) {
            if (removeFirst) {
              $element.find('input').off('change', $scope.onCheckboxChange);
            }
            return $element.find('input').on('change', $scope.onCheckboxChange);
          };
          $scope.registerCheckboxChangeListeners(false);
        }
      };
    }
  ]).directive('djangoCradminListfilterRadiolist', [
    function() {
      return {
        restrict: 'A',
        require: '^djangoCradminListfilter',
        scope: {
          options: '=djangoCradminListfilterRadiolist'
        },
        controller: function($scope, $element) {
          /*
          Replace all contents with new elements from the server.
          */

          $scope.syncWithRemoteFilterList = function($remoteFilterList) {
            var $remoteElement, domId;
            domId = $element.attr('id');
            $remoteElement = $remoteFilterList.find('#' + domId);
            $element.empty();
            $element.append(angular.element($remoteElement.html()));
            return $scope.registerCheckboxChangeListeners(true);
          };
          $scope.onLoadInProgress = function(filterDomId) {
            return $element.find('input').prop('disabled', true);
          };
          $scope.onLoadFinished = function(filterDomId) {
            return $element.find('input').prop('disabled', false);
          };
        },
        link: function($scope, $element, attributes, listfilterCtrl) {
          var getUrl, onLoadSuccess;
          listfilterCtrl.addFilterScope($scope);
          getUrl = function($inputElement) {
            return $inputElement.attr('data-url');
          };
          onLoadSuccess = function(data) {
            return $element.find('#' + data.checkboxId).focus();
          };
          $scope.onRadioChange = function(e) {
            var checkboxId, remoteUrl;
            remoteUrl = getUrl(angular.element(e.target));
            checkboxId = angular.element(e.target).attr('id');
            return listfilterCtrl.load({
              remoteUrl: remoteUrl,
              filterDomId: $element.attr('id'),
              onLoadSuccess: onLoadSuccess,
              onLoadSuccessData: {
                checkboxId: checkboxId
              },
              loadingmessage: $scope.options.loadingmessage
            });
          };
          $scope.registerCheckboxChangeListeners = function(removeFirst) {
            if (removeFirst) {
              $element.find('input').off('change', $scope.onRadioChange);
            }
            return $element.find('input').on('change', $scope.onRadioChange);
          };
          $scope.registerCheckboxChangeListeners(false);
        }
      };
    }
  ]);

}).call(this);
