(function() {
  var app;

  app = angular.module('djangoCradmin.forms.datetimewidget', ['cfp.hotkeys']);

  app.directive('djangoCradminDatetimeSelector', [
    '$timeout', '$compile', '$rootScope', 'hotkeys', 'djangoCradminCalendarApi', 'djangoCradminWindowDimensions', function($timeout, $compile, $rootScope, hotkeys, djangoCradminCalendarApi, djangoCradminWindowDimensions) {
      return {
        scope: {
          config: "=djangoCradminDatetimeSelector"
        },
        templateUrl: 'forms/dateselector.tpl.html',
        controller: function($scope, $element) {
          var __addCommonHotkeys, __addPage1Hotkeys, __getFirstFocusableItemInCurrentPage, __getFocusItemAfterHide, __getInitialFocusItemForCurrentPage, __getLastFocusableItemInCurrentPage, __removeHotkeys;
          $scope.page = null;
          /*
          Handles keyboard navigation.
          */

          $scope.__keyboardNavigation = function(event, direction) {
            var activeElement, lastFocusedElement, newFocusTd, nextSibling, nextTr, previousSibling, previousTr;
            if (direction === 'pageup' || direction === 'pagedown') {
              event.preventDefault();
            }
            if ($element.find('.django-cradmin-datetime-selector-table').is(':visible')) {
              activeElement = angular.element(document.activeElement);
              if (activeElement.hasClass('django-cradmin-datetime-selector-daybuttoncell-button')) {
                event.preventDefault();
                if (direction === 'right') {
                  nextSibling = activeElement.parent().next();
                  if (nextSibling.length > 0) {
                    newFocusTd = nextSibling;
                  }
                }
                if (direction === 'left') {
                  previousSibling = activeElement.parent().prev();
                  if (previousSibling.length > 0) {
                    newFocusTd = previousSibling;
                  }
                }
                if (direction === 'up') {
                  previousTr = activeElement.parent().parent().prev();
                  if (previousTr.length > 0) {
                    newFocusTd = angular.element(previousTr.children().get(activeElement.parent().index()));
                  }
                }
                if (direction === 'down') {
                  nextTr = activeElement.parent().parent().next();
                  if (nextTr.length > 0) {
                    newFocusTd = angular.element(nextTr.children().get(activeElement.parent().index()));
                  }
                }
                if ((newFocusTd != null) && newFocusTd.length > 0) {
                  newFocusTd.find('button').focus();
                }
                if (direction === 'home') {
                  activeElement.parent().parent().parent().find('button:enabled').first().focus();
                }
                if (direction === 'end') {
                  activeElement.parent().parent().parent().find('button:enabled').last().focus();
                }
                if (direction === 'pageup') {
                  return $element.find('.django-cradmin-datetime-selector-monthselect').focus();
                }
              } else if (direction === 'pagedown') {
                if (activeElement.parent().hasClass('django-cradmin-datetime-selector-dateselectors')) {
                  lastFocusedElement = $element.find('.django-cradmin-datetime-selector-daybuttoncell-lastfocused button');
                  if (lastFocusedElement.is(':visible')) {
                    return lastFocusedElement.focus();
                  } else {
                    return angular.element($element.find('.django-cradmin-datetime-selector-daybuttoncell-in-current-month button').first()).focus();
                  }
                }
              }
            }
          };
          /*
          Called when enter is pressed in any of the select fields.
          
          If we have a visible use-button, we do the same as if the user
          pressed that. If we are on page1, on desktop (no use-button),
          we move the focus into the first day of the current month
          in the day select table, or to the selected day if that is visible.
          */

          $scope.__onSelectEnterPressed = function() {
            var selectedButton, tableElement, useButton;
            if ($scope.page === 1) {
              useButton = $element.find('.django-cradmin-datetime-selector-dateview ' + '.django-cradmin-datetime-selector-use-button');
              if (useButton.is(":visible")) {
                return $scope.onClickUseTime();
              } else {
                tableElement = $element.find('.django-cradmin-datetime-selector-table');
                selectedButton = tableElement.find('.django-cradmin-datetime-selector-daybuttoncell-selected button');
                if (selectedButton.length > 0) {
                  return selectedButton.focus();
                } else {
                  return tableElement.find('.django-cradmin-datetime-selector-daybuttoncell-in-current-month button').first().focus();
                }
              }
            } else if ($scope.page === 2) {
              return $scope.onClickUseTime();
            }
          };
          /*
          Returns the item we want to focus on when we tab forward from the last
          focusable item on the current page.
          */

          __getFirstFocusableItemInCurrentPage = function() {
            if ($scope.page === 1) {
              return $element.find('.django-cradmin-datetime-selector-dateview ' + '.django-cradmin-datetime-selector-closebutton');
            } else if ($scope.page === 2) {
              return $element.find('.django-cradmin-datetime-selector-timeview ' + '.django-cradmin-datetime-selector-closebutton');
            }
          };
          /*
          Returns the item we want to focus on when we tab back from the first
          focusable item on the current page.
          */

          __getLastFocusableItemInCurrentPage = function() {
            var useButton;
            if ($scope.page === 1) {
              useButton = $element.find('.django-cradmin-datetime-selector-dateview ' + '.django-cradmin-datetime-selector-use-button');
              if (useButton.is(":visible")) {
                return useButton;
              } else {
                return $element.find('.django-cradmin-datetime-selector-table ' + 'td.django-cradmin-datetime-selector-daybuttoncell-in-current-month button').last();
              }
            } else if ($scope.page === 2) {
              return $element.find('.django-cradmin-datetime-selector-timeview ' + '.django-cradmin-datetime-selector-use-button');
            }
          };
          /*
          Get the initial item to focus on when we open/show a page.
          */

          __getInitialFocusItemForCurrentPage = function() {
            var dayselectElement;
            if ($scope.page === 1) {
              dayselectElement = $element.find('.django-cradmin-datetime-selector-dayselect');
              if (dayselectElement.is(':visible')) {
                return dayselectElement;
              } else {
                return $element.find('.django-cradmin-datetime-selector-monthselect');
              }
            } else if ($scope.page === 2) {
              return $element.find('.django-cradmin-datetime-selector-timeview ' + '.django-cradmin-datetime-selector-hourselect');
            }
          };
          /*
          Get the item to focus on when we close the datetime picker.
          */

          __getFocusItemAfterHide = function() {
            return $scope.triggerButton;
          };
          /*
          Triggered when the user focuses on the hidden (sr-only) button we have
          added to the start of the datetime-selector div.
          */

          $scope.onFocusHead = function() {
            if ($scope.page !== null) {
              __getLastFocusableItemInCurrentPage().focus();
            }
          };
          /*
          Triggered when the user focuses on the hidden (sr-only) button we have
          added to the end of the datetime-selector div.
          */

          $scope.onFocusTail = function() {
            if ($scope.page !== null) {
              __getFirstFocusableItemInCurrentPage().focus();
            }
          };
          /*
          Called when a users selects a date using the mobile-only <select>
          menu to select a day.
          */

          $scope.onSelectDayNumber = function() {
            $scope.monthlyCalendarCoordinator.handleCurrentDayObjectChange();
          };
          /*
          Called when a user selects a date by clicking on a day
          in the calendar table.
          */

          $scope.onClickCalendarDay = function(calendarDay) {
            $scope.monthlyCalendarCoordinator.handleCalendarDayChange(calendarDay);
            if ($scope.config.include_time) {
              $scope.showPage2();
            } else {
              $scope.__useShownValue();
            }
          };
          /*
          Called when a users focuses a date in the calendar table.
          */

          $scope.onFocusCalendayDay = function(calendarDay) {
            $scope.monthlyCalendarCoordinator.handleFocusOnCalendarDay(calendarDay);
          };
          /*
          Called when a users selects a month using the month <select>
          menu.
          */

          $scope.onSelectMonth = function() {
            $scope.monthlyCalendarCoordinator.handleCurrentMonthChange();
          };
          /*
          Called when a users selects a year using the year <select>
          menu.
          */

          $scope.onSelectYear = function() {
            $scope.monthlyCalendarCoordinator.handleCurrentYearChange();
          };
          /*
          Called when a users selects an hour using the hour <select>
          menu.
          */

          $scope.onSelectHour = function() {
            $scope.monthlyCalendarCoordinator.handleCurrentHourChange();
          };
          /*
          Called when a users selects a minute using the minute <select>
          menu.
          */

          $scope.onSelectMinute = function() {
            $scope.monthlyCalendarCoordinator.handleCurrentMinuteChange();
          };
          /*
          Called when a user clicks the "Use" button on the time page.
          */

          $scope.onClickUseTime = function() {
            $scope.__useShownValue();
          };
          /*
          Used to get the preview of the selected date on page2 (above the time selector).
          */

          $scope.getTimeselectorDatepreview = function() {
            return $scope.calendarCoordinator.shownMomentObject.format($scope.config.timeselector_datepreview_momentjs_format);
          };
          /*
          This is used to get the aria-label attribute for the "Use" button.
          */

          $scope.getUseButtonAriaLabel = function() {
            var formattedDate;
            if ($scope.monthlyCalendarCoordinator != null) {
              formattedDate = $scope.calendarCoordinator.shownMomentObject.format($scope.config.usebutton_arialabel_momentjs_format);
              return ("" + $scope.config.usebutton_arialabel_prefix + " ") + ("" + formattedDate);
            } else {

            }
            return '';
          };
          /*
          Get day-button (button in the calendar table) aria-label attribute.
          */

          $scope.getDaybuttonAriaLabel = function(calendarDay) {
            var isSelected, label;
            label = "" + (calendarDay.momentObject.format('MMMM D'));
            if ($scope.config.today_label_text !== '' && calendarDay.isToday()) {
              label = "" + label + " (" + $scope.config.today_label_text + ")";
            } else {
              isSelected = calendarDay.momentObject.isSame($scope.calendarCoordinator.selectedMomentObject, 'day');
              if ($scope.config.selected_day_label_text !== '' && isSelected) {
                label = "" + label + " (" + $scope.config.selected_day_label_text + ")";
              }
            }
            return label;
          };
          /*
          Returns ``true`` if we have any buttons in the buttonrow.
          */

          $scope.hasShortcuts = function() {
            if ($scope.calendarCoordinator.nowIsValidValue()) {
              return true;
            } else if (!$scope.config.required) {
              return true;
            } else {
              return false;
            }
          };
          $scope.onClickTodayButton = function() {
            $scope.monthlyCalendarCoordinator.setToToday();
            if ($scope.config.include_time) {
              $scope.showPage2();
            } else {
              $scope.__useShownValue();
            }
          };
          $scope.onClickNowButton = function() {
            $scope.calendarCoordinator.setToNow();
            return $scope.__useShownValue();
          };
          $scope.onClickClearButton = function() {
            return $scope.__clearSelectedValue();
          };
          $scope.getTabindexForCalendarDay = function(calendarDay) {
            if (calendarDay.isInCurrentMonth) {
              return "0";
            } else {

            }
            return "-1";
          };
          /*
          Update the preview text to reflect the selected value.
          */

          $scope.__updatePreviewText = function() {
            var preview, templateScope;
            if ($scope.calendarCoordinator.selectedMomentObject != null) {
              templateScope = $rootScope.$new(true);
              templateScope.momentObject = $scope.calendarCoordinator.selectedMomentObject.clone();
              preview = $compile($scope.previewAngularjsTemplate)(templateScope);
              $scope.previewElement.empty();
              $scope.previewElement.append(preview);
              return $scope.previewElement.show();
            } else {
              if (($scope.config.no_value_preview_text != null) && $scope.config.no_value_preview_text !== '') {
                $scope.previewElement.html($scope.config.no_value_preview_text);
                return $scope.previewElement.show();
              } else {
                return $scope.previewElement.hide();
              }
            }
          };
          /*
          Apply a css animation to indicate that the preview text has
          changed.
          
          The ``delay_milliseconds`` parameter is the number of milliseonds
          to delay starting the animation.
          */

          $scope.__animatePreviewText = function(delay_milliseconds) {
            if ($scope.config.preview_change_animation_cssclass != null) {
              $scope.previewElement.addClass($scope.config.preview_change_animation_cssclass);
              return $timeout(function() {
                return $timeout(function() {
                  $scope.previewElement.removeClass($scope.config.preview_change_animation_cssclass);
                  return $scope.previewElement.first().offsetWidth = $scope.previewElement.first().offsetWidth;
                }, $scope.config.preview_change_animation_duration_milliseconds);
              }, delay_milliseconds);
            }
          };
          /*
          Update the trigger button label to reflect the selected value.
          */

          $scope.__updateTriggerButtonLabel = function() {
            var label;
            if ($scope.calendarCoordinator.selectedMomentObject != null) {
              label = $scope.config.buttonlabel;
            } else {
              label = $scope.config.buttonlabel_novalue;
            }
            return $scope.triggerButton.html(label);
          };
          /*
          Update the value of the destination field to reflect the selected value.
          */

          $scope.__updateDestinationFieldValue = function() {
            var destinationFieldValue;
            if ($scope.calendarCoordinator.selectedMomentObject != null) {
              destinationFieldValue = $scope.calendarCoordinator.selectedMomentObject.format($scope.config.destinationfield_momentjs_format);
            } else {
              destinationFieldValue = '';
            }
            return $scope.destinationField.val(destinationFieldValue);
          };
          /*
          Update destination field value, preview text and trigger button label,
          and hide the datetime selector.
          */

          $scope.__hideWithSelectedValueApplied = function() {
            $scope.__updateDestinationFieldValue();
            $scope.__updatePreviewText();
            $scope.__updateTriggerButtonLabel();
            return $scope.hide();
          };
          /*
          Make the shown value the selected value and call
          ``$scope.__hideWithSelectedValueApplied()``.
          */

          $scope.__useShownValue = function() {
            $scope.calendarCoordinator.selectShownValue();
            return $scope.__hideWithSelectedValueApplied();
          };
          /*
          Clear the selected value and call ``$scope.__hideWithSelectedValueApplied()``.
          */

          $scope.__clearSelectedValue = function() {
            $scope.calendarCoordinator.clearSelectedMomentObject();
            return $scope.__hideWithSelectedValueApplied();
          };
          __addCommonHotkeys = function() {
            hotkeys.add({
              combo: 'esc',
              callback: function(event) {
                return $scope.hide();
              },
              allowIn: ['BUTTON', 'SELECT', 'INPUT']
            });
            hotkeys.add({
              combo: 'up',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'up');
              }
            });
            hotkeys.add({
              combo: 'down',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'down');
              }
            });
            hotkeys.add({
              combo: 'left',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'left');
              }
            });
            hotkeys.add({
              combo: 'right',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'right');
              }
            });
            hotkeys.add({
              combo: 'home',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'home');
              }
            });
            hotkeys.add({
              combo: 'end',
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'end');
              }
            });
            hotkeys.add({
              combo: 'pagedown',
              allowIn: ['BUTTON', 'SELECT', 'INPUT'],
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'pagedown');
              }
            });
            return hotkeys.add({
              combo: 'pageup',
              allowIn: ['BUTTON', 'SELECT', 'INPUT', 'BUTTON'],
              callback: function(event) {
                return $scope.__keyboardNavigation(event, 'pageup');
              }
            });
          };
          __addPage1Hotkeys = function() {};
          __removeHotkeys = function() {
            hotkeys.del('esc');
            hotkeys.del('up');
            hotkeys.del('down');
            hotkeys.del('left');
            hotkeys.del('right');
            hotkeys.del('home');
            hotkeys.del('end');
            hotkeys.del('pagedown');
            return hotkeys.del('pageup');
          };
          $scope.__onMouseWheel = function(e) {
            e.preventDefault();
            return e.stopPropagation();
          };
          $scope.__adjustPosition = function() {
            var contentWrapperElement, scrollTop, windowHeight;
            contentWrapperElement = $element.find('.django-cradmin-datetime-selector-contentwrapper');
            scrollTop = angular.element(window).scrollTop();
            windowHeight = angular.element(window).height();
            return $scope.datetimeSelectorElement.css({
              top: scrollTop,
              height: "" + windowHeight + "px"
            });
          };
          $scope.onWindowResize = function() {
            return $scope.__adjustPosition();
          };
          $scope.__show = function() {
            __removeHotkeys();
            __addCommonHotkeys();
            return $scope.__adjustPosition();
          };
          $scope.showPage1 = function() {
            angular.element('body').on('mousewheel touchmove', $scope.__onMouseWheel);
            $scope.page = 1;
            $timeout(function() {
              return __getInitialFocusItemForCurrentPage().focus();
            }, 150);
            $scope.__show();
            __addPage1Hotkeys();
          };
          $scope.showPage2 = function() {
            $scope.page = 2;
            $scope.calendarCoordinator.selectShownValue();
            $timeout(function() {
              return __getInitialFocusItemForCurrentPage().focus();
            }, 150);
            $scope.__show();
          };
          $scope.hide = function() {
            angular.element('body').off('mousewheel touchmove', $scope.__onMouseWheel);
            if ($scope.page === 2) {
              $scope.page = 3;
              $timeout(function() {
                return $scope.page = null;
              }, $scope.config.hide_animation_duration_milliseconds);
            } else {
              $scope.page = null;
            }
            __removeHotkeys();
            $timeout(function() {
              return $scope.__animatePreviewText();
            }, $scope.config.hide_animation_duration_milliseconds);
            $timeout(function() {
              return __getFocusItemAfterHide().focus();
            }, 150);
          };
          return $scope.initialize = function() {
            var currentDateIsoString, maximumDatetime, minimumDatetime, selectedMomentObject;
            currentDateIsoString = $scope.destinationField.val();
            if ((currentDateIsoString != null) && currentDateIsoString !== '') {
              selectedMomentObject = moment(currentDateIsoString);
              $scope.triggerButton.html($scope.config.buttonlabel);
            } else {
              selectedMomentObject = null;
              $scope.triggerButton.html($scope.config.buttonlabel_novalue);
            }
            minimumDatetime = null;
            maximumDatetime = null;
            if ($scope.config.minimum_datetime != null) {
              minimumDatetime = moment($scope.config.minimum_datetime);
            }
            if ($scope.config.maximum_datetime != null) {
              maximumDatetime = moment($scope.config.maximum_datetime);
            }
            $scope.calendarCoordinator = new djangoCradminCalendarApi.CalendarCoordinator({
              selectedMomentObject: selectedMomentObject,
              minimumDatetime: minimumDatetime,
              maximumDatetime: maximumDatetime,
              nowMomentObject: moment($scope.config.now)
            });
            $scope.monthlyCalendarCoordinator = new djangoCradminCalendarApi.MonthlyCalendarCoordinator({
              calendarCoordinator: $scope.calendarCoordinator,
              yearselectValues: $scope.config.yearselect_values,
              hourselectValues: $scope.config.hourselect_values,
              minuteselectValues: $scope.config.minuteselect_values,
              yearFormat: $scope.config.yearselect_momentjs_format,
              monthFormat: $scope.config.monthselect_momentjs_format,
              dayOfMonthSelectFormat: $scope.config.dayofmonthselect_momentjs_format,
              dayOfMonthTableCellFormat: $scope.config.dayofmonthtablecell_momentjs_format,
              hourFormat: $scope.config.hourselect_momentjs_format,
              minuteFormat: $scope.config.minuteselect_momentjs_format
            });
            return $scope.__updatePreviewText();
          };
        },
        link: function($scope, $element) {
          var body, configname, configvalue, labelElement, previewTemplateScriptElement, required_config_attributes, _i, _len;
          body = angular.element('body');
          $element.appendTo(body);
          djangoCradminWindowDimensions.register($scope);
          $scope.$on('$destroy', function() {
            return djangoCradminWindowDimensions.unregister($scope);
          });
          if ($scope.config.no_value_preview_text == null) {
            $scope.config.no_value_preview_text = '';
          }
          required_config_attributes = ['now', 'destinationfieldid', 'triggerbuttonid', 'previewid', 'previewtemplateid', 'required', 'usebuttonlabel', 'usebutton_arialabel_prefix', 'usebutton_arialabel_momentjs_format', 'close_icon', 'back_icon', 'back_to_datepicker_screenreader_text', 'destinationfield_momentjs_format', 'timeselector_datepreview_momentjs_format', 'year_screenreader_text', 'month_screenreader_text', 'day_screenreader_text', 'hour_screenreader_text', 'minute_screenreader_text', 'dateselector_table_screenreader_caption', 'today_label_text', 'selected_day_label_text', 'yearselect_values', 'hourselect_values', 'yearselect_momentjs_format', 'monthselect_momentjs_format', 'dayofmonthselect_momentjs_format', 'dayofmonthtablecell_momentjs_format', 'hourselect_momentjs_format', 'minuteselect_momentjs_format', 'minuteselect_values', 'now_button_text', 'today_button_text', 'clear_button_text', 'hide_animation_duration_milliseconds'];
          for (_i = 0, _len = required_config_attributes.length; _i < _len; _i++) {
            configname = required_config_attributes[_i];
            configvalue = $scope.config[configname];
            if ((configvalue == null) || configvalue === '') {
              if (typeof console !== "undefined" && console !== null) {
                if (typeof console.error === "function") {
                  console.error("The " + configname + " config is required!");
                }
              }
            }
          }
          $scope.destinationField = angular.element("#" + $scope.config.destinationfieldid);
          if ($scope.destinationField.length === 0) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.error === "function") {
                console.error("Could not find the destinationField element with ID: " + $scope.config.destinationfieldid);
              }
            }
          }
          $scope.triggerButton = angular.element("#" + $scope.config.triggerbuttonid);
          if ($scope.triggerButton.length > 0) {
            $scope.triggerButton.on('click', function() {
              $scope.initialize();
              $scope.showPage1();
              $scope.$apply();
            });
            labelElement = angular.element("label[for=" + $scope.config.destinationfieldid + "]");
            if (labelElement.length > 0) {
              if (!labelElement.attr('id')) {
                labelElement.attr('id', "" + $scope.config.destinationfieldid + "_label");
              }
              $scope.triggerButton.attr('aria-labeledby', "" + (labelElement.attr('id')) + " " + $scope.config.previewid);
            }
          } else {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.warn === "function") {
                console.warn("Could not find the triggerButton element with ID: " + $scope.config.triggerbuttonid);
              }
            }
          }
          $scope.previewElement = angular.element("#" + $scope.config.previewid);
          if ($scope.previewElement.length === 0) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.warn === "function") {
                console.warn("Could not find the previewElement element with ID: " + $scope.config.previewid);
              }
            }
          }
          previewTemplateScriptElement = angular.element("#" + $scope.config.previewtemplateid);
          if (previewTemplateScriptElement.length === 0) {
            if (typeof console !== "undefined" && console !== null) {
              if (typeof console.warn === "function") {
                console.warn("Could not find the previewTemplateScriptElement element " + ("with ID: " + $scope.config.previewtemplateid));
              }
            }
          } else {
            $scope.previewAngularjsTemplate = previewTemplateScriptElement.html();
          }
          $scope.datetimeSelectorElement = $element.find('.django-cradmin-datetime-selector');
          $scope.initialize();
          $scope.destinationField.on('change', function() {
            $scope.initialize();
            $scope.$apply();
            return $scope.__animatePreviewText(0);
          });
          $timeout(function() {
            return $element.find('select').on('keydown', function(e) {
              if (e.which === 13) {
                $scope.__onSelectEnterPressed();
                e.preventDefault();
              }
            });
          }, 100);
        }
      };
    }
  ]);

}).call(this);
