(function() {
  angular.module('djangoCradmin.bulkfileupload', ['angularFileUpload', 'ngCookies']).provider('cradminBulkfileuploadCoordinator', function() {
    var FileUploadCoordinator;
    FileUploadCoordinator = (function() {
      function FileUploadCoordinator($window) {
        this.hiddenfieldnameToScopeMap = {};
        this.window = $window;
      }

      FileUploadCoordinator.prototype.register = function(hiddenfieldname, scope) {
        var existingScope;
        existingScope = this.hiddenfieldnameToScopeMap[hiddenfieldname];
        if (existingScope != null) {
          console.error('Trying to register a fieldname that is already registered with ' + 'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname);
          return;
        }
        return this.hiddenfieldnameToScopeMap[hiddenfieldname] = scope;
      };

      FileUploadCoordinator.prototype.unregister = function(hiddenfieldname) {
        var scope;
        scope = this.hiddenfieldnameToScopeMap[hiddenfieldname];
        if (scope == null) {
          console.error('Trying to unregister a field that is not registered with ' + 'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname);
        }
        return this.hiddenfieldnameToScopeMap[hiddenfieldname] = void 0;
      };

      FileUploadCoordinator.prototype._getScope = function(hiddenfieldname) {
        var scope;
        scope = this.hiddenfieldnameToScopeMap[hiddenfieldname];
        if (scope == null) {
          console.error('Trying to get a field that is not registered with ' + 'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname);
        }
        return scope;
      };

      FileUploadCoordinator.prototype.showOverlayForm = function(hiddenfieldname) {
        var scope;
        scope = this._getScope(hiddenfieldname);
        return scope.formController.showOverlay();
      };

      return FileUploadCoordinator;

    })();
    this.$get = [
      '$window', function($window) {
        return new FileUploadCoordinator($window);
      }
    ];
    return this;
  }).factory('cradminBulkfileupload', function() {
    var FileInfo;
    FileInfo = (function() {
      function FileInfo(options) {
        this.file = options.file;
        this.autosubmit = options.autosubmit;
        this.i18nStrings = options.i18nStrings;
        this.temporaryfileid = options.temporaryfileid;
        if (this.file != null) {
          this.name = this.file.name;
        } else {
          this.name = options.name;
        }
        this.isRemoving = false;
        this.percent = options.percent;
        if (options.finished) {
          this.finished = true;
        } else {
          this.finished = false;
        }
        if (options.hasErrors) {
          this.hasErrors = true;
        } else {
          this.hasErrors = false;
        }
        this.errors = options.errors;
      }

      FileInfo.prototype.markAsIsRemoving = function() {
        return this.isRemoving = true;
      };

      FileInfo.prototype.markAsIsNotRemoving = function() {
        return this.isRemoving = false;
      };

      FileInfo.prototype.updatePercent = function(percent) {
        return this.percent = percent;
      };

      FileInfo.prototype.finish = function(temporaryfile, singlemode) {
        var index;
        this.finished = true;
        index = 0;
        this.file = void 0;
        this.temporaryfileid = temporaryfile.id;
        return this.name = temporaryfile.filename;
      };

      FileInfo.prototype.setErrors = function(errors) {
        this.hasErrors = true;
        return this.errors = errors;
      };

      FileInfo.prototype.indexOf = function(fileInfo) {
        return this.files.indexOf(fileInfo);
      };

      FileInfo.prototype.remove = function(index) {
        return this.files.splice(index, 1);
      };

      return FileInfo;

    })();
    return {
      createFileInfo: function(options) {
        return new FileInfo(options);
      }
    };
  }).directive('djangoCradminBulkfileuploadForm', [
    function() {
      /*
      A form containing ``django-cradmin-bulkfileupload`` fields
      must use this directive.
      */

      return {
        restrict: 'AE',
        scope: {},
        controller: function($scope) {
          $scope._inProgressCounter = 0;
          $scope._submitButtonScopes = [];
          $scope._setSubmitButtonsInProgress = function() {
            var buttonScope, _i, _len, _ref, _results;
            _ref = $scope._submitButtonScopes;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              buttonScope = _ref[_i];
              _results.push(buttonScope.setNotInProgress());
            }
            return _results;
          };
          $scope._setSubmitButtonsNotInProgress = function() {
            var buttonScope, _i, _len, _ref, _results;
            _ref = $scope._submitButtonScopes;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              buttonScope = _ref[_i];
              _results.push(buttonScope.setInProgress());
            }
            return _results;
          };
          this.addInProgress = function() {
            $scope._inProgressCounter += 1;
            if ($scope._inProgressCounter === 1) {
              return $scope._setSubmitButtonsInProgress();
            }
          };
          this.removeInProgress = function() {
            if ($scope._inProgressCounter === 0) {
              throw new Error("It should not be possible to get _inProgressCounter below 0");
            }
            $scope._inProgressCounter -= 1;
            if ($scope._inProgressCounter === 0) {
              return $scope._setSubmitButtonsNotInProgress();
            }
          };
          this.addSubmitButtonScope = function(submitButtonScope) {
            return $scope._submitButtonScopes.push(submitButtonScope);
          };
          this.addSubmitButtonScope = function(submitButtonScope) {
            return $scope._submitButtonScopes.push(submitButtonScope);
          };
          this.registerOverlayControls = function(overlayControlsScope) {
            return $scope._overlayControlsScope = overlayControlsScope;
          };
          this.registerOverlayUploadingmessageScope = function(overlayUploadingmessageScope) {
            return $scope._overlayUploadingmessageScope = overlayUploadingmessageScope;
          };
          this.submitForm = function() {
            if ($scope.overlay) {
              $scope._overlayUploadingmessageScope.onSubmitForm();
            }
            return $scope.element.submit();
          };
          $scope._showOverlay = function() {
            if ($scope.overlay) {
              return $scope.wrapperElement.addClass('django-cradmin-bulkfileupload-overlaywrapper-show');
            } else {
              throw new Error('Can only show the overlay if the form has the ' + 'django-cradmin-bulkfileupload-form-overlay="true" attribute.');
            }
          };
          this.showOverlay = function() {
            return $scope._showOverlay();
          };
          this.hideOverlay = function() {
            if ($scope.overlay) {
              return $scope.wrapperElement.removeClass('django-cradmin-bulkfileupload-overlaywrapper-show');
            } else {
              throw new Error('Can only hide the overlay if the form has the ' + 'django-cradmin-bulkfileupload-form-overlay="true" attribute.');
            }
          };
        },
        link: function($scope, element, attr, uploadController) {
          var body;
          $scope.overlay = attr.djangoCradminBulkfileuploadFormOverlay === 'true';
          $scope.preventWindowDragdrop = attr.djangoCradminBulkfileuploadFormPreventWindowDragdrop !== 'false';
          $scope.openOverlayOnWindowDragdrop = attr.djangoCradminBulkfileuploadFormOpenOverlayOnWindowDragdrop === 'true';
          $scope.element = element;
          if ($scope.overlay) {
            element.addClass('django-cradmin-bulkfileupload-form-overlay');
            body = angular.element('body');
            $scope.wrapperElement = angular.element('<div></div>');
            $scope.wrapperElement.addClass('django-cradmin-bulkfileupload-overlaywrapper');
            $scope.wrapperElement.appendTo(body);
            element.appendTo($scope.wrapperElement);
            $scope._overlayControlsScope.element.appendTo($scope.wrapperElement);
            if (element.find('.has-error').length > 0) {
              $scope._showOverlay();
            }
            if ($scope.preventWindowDragdrop) {
              window.addEventListener("dragover", function(e) {
                return e.preventDefault();
              }, false);
              window.addEventListener("drop", function(e) {
                return e.preventDefault();
              }, false);
            }
            window.addEventListener("dragover", function(e) {
              e.preventDefault();
              $scope.wrapperElement.addClass('django-cradmin-bulkfileupload-overlaywrapper-window-dragover');
              if ($scope.openOverlayOnWindowDragdrop) {
                return $scope._showOverlay();
              }
            }, false);
            window.addEventListener("drop", function(e) {
              e.preventDefault();
              return $scope.wrapperElement.removeClass('django-cradmin-bulkfileupload-overlaywrapper-window-dragover');
            }, false);
            angular.element('body').on('mouseleave', function(e) {
              return $scope.wrapperElement.removeClass('django-cradmin-bulkfileupload-overlaywrapper-window-dragover');
            });
          }
          element.on('submit', function(evt) {
            if ($scope._inProgressCounter !== 0) {
              return evt.preventDefault();
            }
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadSubmit', [
    function() {
      return {
        require: '^djangoCradminBulkfileuploadForm',
        restrict: 'A',
        scope: true,
        controller: function($scope) {
          $scope.inProgress = false;
          $scope.setInProgress = function() {
            $scope.element.prop('disabled', false);
            return $scope.inProgress = false;
          };
          return $scope.setNotInProgress = function() {
            $scope.element.prop('disabled', true);
            return $scope.inProgress = true;
          };
        },
        link: function(scope, element, attr, formController) {
          scope.element = element;
          formController.addSubmitButtonScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileupload', [
    '$upload', '$cookies', 'cradminDetectize', 'cradminBulkfileuploadCoordinator', function($upload, $cookies, cradminDetectize, cradminBulkfileuploadCoordinator) {
      return {
        require: '^djangoCradminBulkfileuploadForm',
        restrict: 'AE',
        scope: true,
        controller: function($scope) {
          var validateSelectedFiles;
          $scope.collectionid = null;
          $scope.cradminLastFilesSelectedByUser = [];
          $scope.fileUploadQueue = [];
          $scope.firstUploadInProgress = false;
          $scope.simpleWidgetScope = null;
          $scope.advancedWidgetScope = null;
          $scope.rejectedFilesScope = null;
          this.setInProgressOrFinishedScope = function(inProgressOrFinishedScope) {
            return $scope.inProgressOrFinishedScope = inProgressOrFinishedScope;
          };
          this.setFileUploadFieldScope = function(fileUploadFieldScope, fieldname) {
            $scope.fileUploadFieldScope = fileUploadFieldScope;
            return cradminBulkfileuploadCoordinator.register(fileUploadFieldScope.fieldname, $scope);
          };
          this.setSimpleWidgetScope = function(simpleWidgetScope) {
            $scope.simpleWidgetScope = simpleWidgetScope;
            return $scope._showAppropriateWidget();
          };
          this.setAdvancedWidgetScope = function(advancedWidgetScope) {
            $scope.advancedWidgetScope = advancedWidgetScope;
            return $scope._showAppropriateWidget();
          };
          this.setRejectFilesScope = function(rejectedFilesScope) {
            return $scope.rejectedFilesScope = rejectedFilesScope;
          };
          this.getUploadUrl = function() {
            return $scope.uploadapiurl;
          };
          this.getCollectionId = function() {
            return $scope.collectionid;
          };
          this.onAdvancedWidgetDragLeave = function() {
            return $scope.formController.onAdvancedWidgetDragLeave();
          };
          $scope._hideUploadWidget = function() {
            $scope.simpleWidgetScope.hide();
            return $scope.advancedWidgetScope.hide();
          };
          $scope._showAppropriateWidget = function() {
            var deviceType;
            if ($scope.advancedWidgetScope && $scope.simpleWidgetScope) {
              deviceType = cradminDetectize.device.type;
              if (deviceType === 'desktop') {
                $scope.simpleWidgetScope.hide();
                return $scope.advancedWidgetScope.show();
              } else {
                $scope.advancedWidgetScope.hide();
                return $scope.simpleWidgetScope.show();
              }
            }
          };
          $scope.filesDropped = function(files, evt, rejectedFiles) {
            /*
            Called when a file is draggen&dropped into the widget.
            */

            if (rejectedFiles.length > 0) {
              return $scope.rejectedFilesScope.setRejectedFiles(rejectedFiles, 'invalid_filetype', $scope.i18nStrings);
            }
          };
          validateSelectedFiles = function() {
            var file, filesToUpload, _i, _len, _ref;
            filesToUpload = [];
            _ref = $scope.cradminLastFilesSelectedByUser;
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              file = _ref[_i];
              if ($scope.apiparameters.max_filesize_bytes) {
                if (file.size > $scope.apiparameters.max_filesize_bytes) {
                  $scope.rejectedFilesScope.addRejectedFile(file, 'max_filesize_bytes_exceeded', $scope.i18nStrings);
                  continue;
                }
              }
              filesToUpload.push(file);
            }
            if ($scope.rejectedFilesScope.hasRejectedFiles() && $scope.autosubmit) {
              return [];
            }
            return filesToUpload;
          };
          $scope.$watch('cradminLastFilesSelectedByUser', function() {
            var file, filesToUpload, _i, _len;
            if ($scope.cradminLastFilesSelectedByUser.length > 0) {
              $scope.rejectedFilesScope.clearRejectedFiles();
              filesToUpload = validateSelectedFiles();
              if (filesToUpload.length > 0) {
                if ($scope.autosubmit) {
                  $scope._hideUploadWidget();
                }
                for (_i = 0, _len = filesToUpload.length; _i < _len; _i++) {
                  file = filesToUpload[_i];
                  $scope._addFileToQueue(file);
                  if ($scope.apiparameters.singlemode) {
                    break;
                  }
                }
              }
              return $scope.cradminLastFilesSelectedByUser = [];
            }
          });
          $scope._addFileToQueue = function(file) {
            var progressFileInfo;
            if ($scope.apiparameters.singlemode) {
              $scope.inProgressOrFinishedScope.clear();
            }
            progressFileInfo = $scope.inProgressOrFinishedScope.addFileInfo({
              percent: 0,
              file: file,
              autosubmit: $scope.autosubmit,
              i18nStrings: $scope.i18nStrings
            });
            $scope.fileUploadQueue.push(progressFileInfo);
            if ($scope.firstUploadInProgress) {
              return;
            }
            if ($scope.collectionid === null) {
              $scope.firstUploadInProgress = true;
            }
            return $scope._processFileUploadQueue();
          };
          $scope._onFileUploadComplete = function(successful) {
            /*
            Called both on file upload success and error
            */

            $scope.firstUploadInProgress = false;
            $scope.formController.removeInProgress();
            if ($scope.fileUploadQueue.length > 0) {
              return $scope._processFileUploadQueue();
            } else if ($scope.autosubmit) {
              if (successful) {
                return $scope.formController.submitForm();
              } else {
                return $scope._showAppropriateWidget();
              }
            }
          };
          $scope._processFileUploadQueue = function() {
            var apidata, progressFileInfo;
            progressFileInfo = $scope.fileUploadQueue.shift();
            apidata = angular.extend({}, $scope.apiparameters, {
              collectionid: $scope.collectionid
            });
            $scope.formController.addInProgress();
            return $scope.upload = $upload.upload({
              url: $scope.uploadapiurl,
              method: 'POST',
              data: apidata,
              file: progressFileInfo.file,
              fileFormDataName: 'file',
              headers: {
                'X-CSRFToken': $cookies.get('csrftoken'),
                'Content-Type': 'multipart/form-data'
              }
            }).progress(function(evt) {
              return progressFileInfo.updatePercent(parseInt(100.0 * evt.loaded / evt.total));
            }).success(function(data, status, headers, config) {
              progressFileInfo.finish(data.temporaryfiles[0], $scope.apiparameters.singlemode);
              $scope._setCollectionId(data.collectionid);
              return $scope._onFileUploadComplete(true);
            }).error(function(data, status) {
              console.log(data);
              if (status === 503) {
                progressFileInfo.setErrors({
                  file: [
                    {
                      message: $scope.errormessage503
                    }
                  ]
                });
              } else {
                progressFileInfo.setErrors(data);
              }
              $scope.inProgressOrFinishedScope.removeFileInfo(progressFileInfo);
              $scope.rejectedFilesScope.addRejectedFileInfo(progressFileInfo);
              return $scope._onFileUploadComplete(false);
            });
          };
          $scope._setCollectionId = function(collectionid) {
            $scope.collectionid = collectionid;
            return $scope.fileUploadFieldScope.setCollectionId(collectionid);
          };
        },
        link: function($scope, element, attributes, formController) {
          var options;
          options = angular.fromJson(attributes.djangoCradminBulkfileupload);
          $scope.uploadapiurl = options.uploadapiurl;
          $scope.apiparameters = options.apiparameters;
          $scope.errormessage503 = options.errormessage503;
          $scope.autosubmit = options.autosubmit;
          $scope.i18nStrings = {
            close_errormessage_label: options.close_errormessage_label,
            remove_file_label: options.remove_file_label,
            removing_file_message: options.removing_file_message
          };
          $scope.formController = formController;
          $scope.$on('$destroy', function() {
            if ($scope.fileUploadFieldScope != null) {
              return cradminBulkfileuploadCoordinator.unregister($scope.fileUploadFieldScope.fieldname);
            }
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadRejectedFiles', [
    'cradminBulkfileupload', function(cradminBulkfileupload) {
      /*
      This directive is used to show files that are rejected on drop because
      of wrong mimetype. Each time a user drops one or more file with invalid
      mimetype, this template is re-rendered and displayed.
      */

      return {
        restrict: 'A',
        require: '^djangoCradminBulkfileupload',
        templateUrl: 'bulkfileupload/rejectedfiles.tpl.html',
        transclude: true,
        scope: {
          errorMessageMap: '=djangoCradminBulkfileuploadRejectedFiles'
        },
        controller: function($scope) {
          $scope.rejectedFiles = [];
          $scope.clearRejectedFiles = function() {
            return $scope.rejectedFiles = [];
          };
          $scope.addRejectedFileInfo = function(fileInfo, errormessagecode) {
            return $scope.rejectedFiles.push(fileInfo);
          };
          $scope.addRejectedFile = function(file, errormessagecode, i18nStrings) {
            return $scope.addRejectedFileInfo(cradminBulkfileupload.createFileInfo({
              file: file,
              hasErrors: true,
              i18nStrings: i18nStrings,
              errors: {
                files: [
                  {
                    message: $scope.errorMessageMap[errormessagecode]
                  }
                ]
              }
            }));
          };
          $scope.hasRejectedFiles = function() {
            return $scope.rejectedFiles.length > 0;
          };
          $scope.setRejectedFiles = function(rejectedFiles, errormessagecode, i18nStrings) {
            var file, _i, _len, _results;
            $scope.clearRejectedFiles();
            _results = [];
            for (_i = 0, _len = rejectedFiles.length; _i < _len; _i++) {
              file = rejectedFiles[_i];
              _results.push($scope.addRejectedFile(file, errormessagecode, i18nStrings));
            }
            return _results;
          };
          return $scope.closeMessage = function(fileInfo) {
            var index;
            index = $scope.rejectedFiles.indexOf(fileInfo);
            if (index !== -1) {
              return $scope.rejectedFiles.splice(index, 1);
            }
          };
        },
        link: function(scope, element, attr, bulkfileuploadController) {
          bulkfileuploadController.setRejectFilesScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadProgress', [
    'cradminBulkfileupload', '$http', '$cookies', function(cradminBulkfileupload, $http, $cookies) {
      return {
        restrict: 'AE',
        require: '^djangoCradminBulkfileupload',
        templateUrl: 'bulkfileupload/progress.tpl.html',
        scope: {},
        controller: function($scope) {
          $scope.fileInfoArray = [];
          $scope.removeFileInfo = function(fileInfo) {
            var fileInfoIndex;
            fileInfoIndex = $scope.fileInfoArray.indexOf(fileInfo);
            if (fileInfoIndex !== -1) {
              return $scope.fileInfoArray.splice(fileInfoIndex, 1);
            } else {
              throw new Error("Could not find requested fileInfo with temporaryfileid=" + fileInfo.temporaryfileid + ".");
            }
          };
          this.removeFile = function(fileInfo) {
            if (fileInfo.temporaryfileid == null) {
              throw new Error("Can not remove files without a temporaryfileid");
            }
            fileInfo.markAsIsRemoving();
            $scope.$apply();
            return $http({
              url: $scope.uploadController.getUploadUrl(),
              method: 'DELETE',
              headers: {
                'X-CSRFToken': $cookies.get('csrftoken')
              },
              data: {
                collectionid: $scope.uploadController.getCollectionId(),
                temporaryfileid: fileInfo.temporaryfileid
              }
            }).success(function(data, status, headers, config) {
              return $scope.removeFileInfo(fileInfo);
            }).error(function(data, status, headers, config) {
              if (typeof console !== "undefined" && console !== null) {
                if (typeof console.error === "function") {
                  console.error('ERROR', data);
                }
              }
              alert('An error occurred while removing the file. Please try again.');
              return fileInfo.markAsIsNotRemoving();
            });
          };
          $scope.addFileInfo = function(options) {
            var fileInfo;
            fileInfo = cradminBulkfileupload.createFileInfo(options);
            $scope.fileInfoArray.push(fileInfo);
            return fileInfo;
          };
          $scope.clear = function(options) {
            return $scope.fileInfoArray = [];
          };
          $scope.clearErrors = function() {
            var fileInfo, index, _i, _ref, _results;
            _results = [];
            for (index = _i = _ref = $scope.fileInfoArray.length - 1; _i >= 0; index = _i += -1) {
              fileInfo = $scope.fileInfoArray[index];
              if (fileInfo.hasErrors) {
                _results.push($scope.fileInfoArray.splice(index, 1));
              } else {
                _results.push(void 0);
              }
            }
            return _results;
          };
        },
        link: function(scope, element, attr, uploadController) {
          scope.uploadController = uploadController;
          uploadController.setInProgressOrFinishedScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkFileInfo', [
    function() {
      /**
      Renders a single file info with progress info, errors, etc.
      
      Used both the djangoCradminBulkfileuploadProgress directive.
      */

      return {
        restrict: 'AE',
        scope: {
          fileInfo: '=djangoCradminBulkFileInfo'
        },
        templateUrl: 'bulkfileupload/fileinfo.tpl.html',
        transclude: true,
        controller: function($scope) {
          this.close = function() {
            return $scope.element.remove();
          };
        },
        link: function(scope, element, attr) {
          scope.element = element;
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadErrorCloseButton', [
    function() {
      return {
        restrict: 'A',
        require: '^djangoCradminBulkFileInfo',
        scope: {},
        link: function(scope, element, attr, fileInfoController) {
          element.on('click', function(evt) {
            evt.preventDefault();
            return fileInfoController.close();
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadRemoveFileButton', [
    function() {
      return {
        restrict: 'A',
        require: '^djangoCradminBulkfileuploadProgress',
        scope: {
          'fileInfo': '=djangoCradminBulkfileuploadRemoveFileButton'
        },
        link: function(scope, element, attr, progressController) {
          element.on('click', function(evt) {
            evt.preventDefault();
            return progressController.removeFile(scope.fileInfo);
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadCollectionidField', [
    function() {
      return {
        require: '^djangoCradminBulkfileupload',
        restrict: 'AE',
        scope: {},
        controller: function($scope) {
          $scope.setCollectionId = function(collectionid) {
            return $scope.element.val("" + collectionid);
          };
        },
        link: function(scope, element, attr, uploadController) {
          scope.element = element;
          scope.fieldname = attr.name;
          uploadController.setFileUploadFieldScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadAdvancedWidget', [
    '$timeout', function($timeout) {
      return {
        require: '^djangoCradminBulkfileupload',
        restrict: 'AE',
        scope: {},
        link: function(scope, element, attr, uploadController) {
          scope.hide = function() {
            return element.css('display', 'none');
          };
          scope.show = function() {
            return element.css('display', 'block');
          };
          uploadController.setAdvancedWidgetScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadSimpleWidget', [
    function() {
      return {
        require: '^djangoCradminBulkfileupload',
        restrict: 'AE',
        scope: {},
        link: function(scope, element, attr, uploadController) {
          scope.hide = function() {
            return element.css('display', 'none');
          };
          scope.show = function() {
            return element.css('display', 'block');
          };
          uploadController.setSimpleWidgetScope(scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadShowOverlay', [
    'cradminBulkfileuploadCoordinator', function(cradminBulkfileuploadCoordinator) {
      return {
        restrict: 'AE',
        scope: {
          hiddenfieldname: '@djangoCradminBulkfileuploadShowOverlay'
        },
        link: function($scope, element, attr) {
          element.on('click', function() {
            return cradminBulkfileuploadCoordinator.showOverlayForm($scope.hiddenfieldname);
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadHideOverlay', [
    function() {
      return {
        restrict: 'AE',
        require: '^djangoCradminBulkfileuploadForm',
        scope: {
          hiddenfieldname: '@djangoCradminBulkfileuploadHideOverlay'
        },
        link: function($scope, element, attr, uploadFormController) {
          element.on('click', function() {
            return uploadFormController.hideOverlay();
          });
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadOverlayControls', [
    function() {
      return {
        restrict: 'AE',
        require: '^djangoCradminBulkfileuploadForm',
        scope: {},
        link: function($scope, element, attr, uploadFormController) {
          $scope.element = element;
          uploadFormController.registerOverlayControls($scope);
        }
      };
    }
  ]).directive('djangoCradminBulkfileuploadOverlayUploadingmessage', [
    function() {
      return {
        restrict: 'AE',
        require: '^djangoCradminBulkfileuploadForm',
        scope: {},
        controller: function($scope) {
          $scope.onSubmitForm = function() {
            return $scope.element.addClass('django-cradmin-bulkfileupload-overlay-uploadingmessage-visible');
          };
        },
        link: function($scope, element, attr, uploadFormController) {
          $scope.element = element;
          uploadFormController.registerOverlayUploadingmessageScope($scope);
        }
      };
    }
  ]);

}).call(this);
