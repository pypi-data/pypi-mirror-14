(function() {
  var app;

  app = angular.module('djangoCradmin.calendar.providers', []);

  app.provider('djangoCradminCalendarApi', function() {
    /**
    Get an array of the short names for all the weekdays
    in the current locale, in the the correct order for the
    current locale.
    */

    var CalendarCoordinator, CalendarDay, CalendarMonth, CalendarWeek, Month, MonthlyCalendarCoordinator, getWeekdaysShortForCurrentLocale;
    getWeekdaysShortForCurrentLocale = function() {
      var firstDayOfWeek, index, weekday, weekdays, weekdaysWithSundayFirst, _i, _ref;
      weekdays = [];
      weekdaysWithSundayFirst = moment.weekdaysShort();
      firstDayOfWeek = moment.localeData().firstDayOfWeek();
      for (index = _i = firstDayOfWeek, _ref = firstDayOfWeek + 6; firstDayOfWeek <= _ref ? _i <= _ref : _i >= _ref; index = firstDayOfWeek <= _ref ? ++_i : --_i) {
        if (index > 6) {
          index = Math.abs(7 - index);
        }
        weekday = weekdaysWithSundayFirst[index];
        weekdays.push(weekday);
      }
      return weekdays;
    };
    Month = (function() {
      function Month(firstDayOfMonth) {
        this.firstDayOfMonth = firstDayOfMonth;
        this.lastDayOfMonth = this.firstDayOfMonth.clone().add({
          days: this.firstDayOfMonth.daysInMonth() - 1
        });
      }

      Month.prototype.getDaysInMonth = function() {
        return this.firstDayOfMonth.daysInMonth();
      };

      return Month;

    })();
    CalendarDay = (function() {
      function CalendarDay(momentObject, isInCurrentMonth, isDisabled, nowMomentObject) {
        this.momentObject = momentObject;
        this.isInCurrentMonth = isInCurrentMonth;
        this.nowMomentObject = nowMomentObject;
        this._isDisabled = isDisabled;
      }

      CalendarDay.prototype.getNumberInMonth = function() {
        return this.momentObject.format('D');
      };

      CalendarDay.prototype.isToday = function() {
        return this.momentObject.isSame(this.nowMomentObject, 'day');
      };

      CalendarDay.prototype.isDisabled = function() {
        return this._isDisabled;
      };

      return CalendarDay;

    })();
    CalendarWeek = (function() {
      function CalendarWeek() {
        this.calendarDays = [];
      }

      CalendarWeek.prototype.addDay = function(calendarDay) {
        return this.calendarDays.push(calendarDay);
      };

      CalendarWeek.prototype.getDayCount = function() {
        return this.calendarDays.length;
      };

      CalendarWeek.prototype.prettyOneLineFormat = function() {
        var calendarDay, formattedDay, formattedDays, _i, _len, _ref;
        formattedDays = [];
        _ref = this.calendarDays;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          calendarDay = _ref[_i];
          formattedDay = calendarDay.momentObject.format('DD');
          if (calendarDay.isInCurrentMonth) {
            formattedDay = " " + formattedDay + " ";
          } else {
            formattedDay = "(" + formattedDay + ")";
          }
          formattedDays.push(formattedDay);
        }
        return formattedDays.join(' ');
      };

      return CalendarWeek;

    })();
    CalendarMonth = (function() {
      function CalendarMonth(calendarCoordinator, momentObject) {
        this.calendarCoordinator = calendarCoordinator;
        this.changeMonth(momentObject);
      }

      CalendarMonth.prototype.changeMonth = function(momentObject) {
        var firstDayOfMonthMomentObject;
        firstDayOfMonthMomentObject = momentObject.clone().set({
          date: 1,
          hour: 0,
          minute: 0,
          second: 0,
          millisecond: 0
        });
        this.month = new Month(firstDayOfMonthMomentObject);
        this.calendarWeeks = [new CalendarWeek()];
        this.currentWeekIndex = 0;
        this.daysPerWeek = 7;
        this.totalWeeks = 6;
        this.currentDayCount = 0;
        this.lastDay = null;
        return this.__build();
      };

      CalendarMonth.prototype.__buildPrefixedDays = function() {
        var index, momentObject, _i, _ref, _results;
        if (this.month.firstDayOfMonth.weekday() > 0) {
          _results = [];
          for (index = _i = _ref = this.month.firstDayOfMonth.weekday(); _ref <= 1 ? _i <= 1 : _i >= 1; index = _ref <= 1 ? ++_i : --_i) {
            momentObject = this.month.firstDayOfMonth.clone().subtract({
              days: index
            });
            _results.push(this.__addMomentObject(momentObject, false));
          }
          return _results;
        }
      };

      CalendarMonth.prototype.__buildSuffixedDays = function() {
        var momentObject, totalDayCount, _results;
        totalDayCount = this.totalWeeks * this.daysPerWeek;
        _results = [];
        while (this.currentDayCount < totalDayCount) {
          momentObject = this.lastDay.momentObject.clone().add({
            days: 1
          });
          _results.push(this.__addMomentObject(momentObject, false));
        }
        return _results;
      };

      CalendarMonth.prototype.__buildDaysBelongingInMonth = function() {
        var dayIndex, momentObject, _i, _ref, _results;
        _results = [];
        for (dayIndex = _i = 1, _ref = this.month.getDaysInMonth(); 1 <= _ref ? _i <= _ref : _i >= _ref; dayIndex = 1 <= _ref ? ++_i : --_i) {
          momentObject = this.month.firstDayOfMonth.clone().date(dayIndex);
          _results.push(this.__addMomentObject(momentObject, true));
        }
        return _results;
      };

      CalendarMonth.prototype.__build = function(momentFirstDayOfMonth) {
        this.__buildPrefixedDays();
        this.__buildDaysBelongingInMonth();
        return this.__buildSuffixedDays();
      };

      CalendarMonth.prototype.__addMomentObject = function(momentObject, isInCurrentMonth) {
        var calendarDay, isDisabled, week;
        week = this.calendarWeeks[this.currentWeekIndex];
        if (week.getDayCount() >= this.daysPerWeek) {
          this.calendarWeeks.push(new CalendarWeek());
          this.currentWeekIndex += 1;
          week = this.calendarWeeks[this.currentWeekIndex];
        }
        isDisabled = !this.calendarCoordinator.momentObjectIsAllowed(momentObject);
        calendarDay = new CalendarDay(momentObject, isInCurrentMonth, isDisabled, this.calendarCoordinator.nowMomentObject);
        week.addDay(calendarDay);
        this.currentDayCount += 1;
        return this.lastDay = calendarDay;
      };

      CalendarMonth.prototype.prettyprint = function() {
        var rowFormatted, week, _i, _len, _ref, _results;
        _ref = this.calendarWeeks;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          week = _ref[_i];
          rowFormatted = [];
          _results.push(typeof console !== "undefined" && console !== null ? typeof console.log === "function" ? console.log(week.prettyOneLineFormat()) : void 0 : void 0);
        }
        return _results;
      };

      return CalendarMonth;

    })();
    /**
    Coordinates the common calendar data no matter what kind of
    view we present.
    */

    CalendarCoordinator = (function() {
      function CalendarCoordinator(_arg) {
        this.selectedMomentObject = _arg.selectedMomentObject, this.minimumDatetime = _arg.minimumDatetime, this.maximumDatetime = _arg.maximumDatetime, this.nowMomentObject = _arg.nowMomentObject;
        if (this.selectedMomentObject != null) {
          this.shownMomentObject = this.selectedMomentObject.clone();
        } else {
          this.setToNow();
          if (!this.momentObjectIsAllowed(this.shownMomentObject)) {
            this.shownMomentObject = this.minimumDatetime.clone();
          }
        }
      }

      CalendarCoordinator.prototype.selectShownValue = function() {
        return this.selectedMomentObject = this.shownMomentObject.clone();
      };

      CalendarCoordinator.prototype.clearSelectedMomentObject = function() {
        return this.selectedMomentObject = null;
      };

      CalendarCoordinator.prototype.momentObjectIsAllowed = function(momentObject, ignoreTime) {
        var isAllowed, maximumDatetime, minimumDatetime;
        if (ignoreTime == null) {
          ignoreTime = true;
        }
        isAllowed = true;
        if (this.minimumDatetime != null) {
          minimumDatetime = this.minimumDatetime;
          if (ignoreTime) {
            minimumDatetime = minimumDatetime.clone().set({
              hour: 0,
              minute: 0,
              second: 0
            });
          }
          isAllowed = !momentObject.isBefore(minimumDatetime);
        }
        if (isAllowed && (this.maximumDatetime != null)) {
          maximumDatetime = this.maximumDatetime;
          if (ignoreTime) {
            maximumDatetime = maximumDatetime.clone().set({
              hour: 23,
              minute: 59,
              second: 59
            });
          }
          isAllowed = !momentObject.isAfter(maximumDatetime);
        }
        return isAllowed;
      };

      CalendarCoordinator.prototype.todayIsValidValue = function() {
        return this.momentObjectIsAllowed(this.nowMomentObject);
      };

      CalendarCoordinator.prototype.nowIsValidValue = function() {
        return this.momentObjectIsAllowed(this.nowMomentObject, false);
      };

      CalendarCoordinator.prototype.shownDateIsToday = function() {
        return this.shownMomentObject.isSame(this.nowMomentObject, 'day');
      };

      CalendarCoordinator.prototype.shownDateIsTodayAndNowIsValid = function() {
        return this.shownDateIsToday() && this.nowIsValidValue();
      };

      CalendarCoordinator.prototype.setToNow = function() {
        return this.shownMomentObject = this.nowMomentObject.clone();
      };

      return CalendarCoordinator;

    })();
    /**
    Coordinates the common calendar data for a month-view.
    */

    MonthlyCalendarCoordinator = (function() {
      function MonthlyCalendarCoordinator(_arg) {
        this.calendarCoordinator = _arg.calendarCoordinator, this.yearselectValues = _arg.yearselectValues, this.hourselectValues = _arg.hourselectValues, this.minuteselectValues = _arg.minuteselectValues, this.yearFormat = _arg.yearFormat, this.monthFormat = _arg.monthFormat, this.dayOfMonthSelectFormat = _arg.dayOfMonthSelectFormat, this.dayOfMonthTableCellFormat = _arg.dayOfMonthTableCellFormat, this.hourFormat = _arg.hourFormat, this.minuteFormat = _arg.minuteFormat;
        this.dayobjects = null;
        this.__initWeekdays();
        this.__initMonthObjects();
        this.__initYearObjects();
        this.__initHourObjects();
        this.__initMinuteObjects();
        this.__changeSelectedDate();
      }

      MonthlyCalendarCoordinator.prototype.__sortConfigObjectsByValue = function(configObjects) {
        var compareFunction;
        compareFunction = function(a, b) {
          if (a.value < b.value) {
            return -1;
          }
          if (a.value > b.value) {
            return 1;
          }
          return 0;
        };
        return configObjects.sort(compareFunction);
      };

      MonthlyCalendarCoordinator.prototype.__initWeekdays = function() {
        return this.shortWeekdays = getWeekdaysShortForCurrentLocale();
      };

      MonthlyCalendarCoordinator.prototype.__initYearObjects = function() {
        var formatMomentObject, hasSelectedYearValue, label, selectedYearValue, year, yearConfig, _i, _len, _ref;
        selectedYearValue = this.calendarCoordinator.shownMomentObject.year();
        hasSelectedYearValue = false;
        formatMomentObject = this.calendarCoordinator.shownMomentObject.clone().set({
          month: 0,
          date: 0,
          hour: 0,
          minute: 0,
          second: 0
        });
        this.__yearsMap = {};
        this.yearselectConfig = [];
        _ref = this.yearselectValues;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          year = _ref[_i];
          label = formatMomentObject.set({
            year: year
          }).format(this.yearFormat);
          yearConfig = {
            value: year,
            label: label
          };
          this.yearselectConfig.push(yearConfig);
          this.__yearsMap[year] = yearConfig;
          if (year === selectedYearValue) {
            hasSelectedYearValue = true;
          }
        }
        if (!hasSelectedYearValue) {
          label = formatMomentObject.set({
            year: selectedYearValue
          }).format(this.yearFormat);
          yearConfig = {
            value: selectedYearValue,
            label: label
          };
          this.yearselectConfig.push(yearConfig);
          this.__yearsMap[yearConfig.value] = yearConfig;
          return this.__sortConfigObjectsByValue(this.yearselectConfig);
        }
      };

      MonthlyCalendarCoordinator.prototype.__initMonthObjects = function() {
        var formatMomentObject, label, monthObject, monthnumber, _i, _results;
        this.monthselectConfig = [];
        this.__monthsMap = {};
        formatMomentObject = this.calendarCoordinator.shownMomentObject.clone().set({
          month: 0,
          date: 0,
          hour: 0,
          minute: 0,
          second: 0
        });
        _results = [];
        for (monthnumber = _i = 0; _i <= 11; monthnumber = ++_i) {
          label = formatMomentObject.set({
            month: monthnumber
          }).format(this.monthFormat);
          monthObject = {
            value: monthnumber,
            label: label
          };
          this.monthselectConfig.push(monthObject);
          _results.push(this.__monthsMap[monthnumber] = monthObject);
        }
        return _results;
      };

      MonthlyCalendarCoordinator.prototype.__initHourObjects = function() {
        var formatMomentObject, hasSelectedHourValue, hour, hourConfig, label, selectedHourValue, _i, _len, _ref;
        selectedHourValue = this.calendarCoordinator.shownMomentObject.hour();
        hasSelectedHourValue = false;
        formatMomentObject = this.calendarCoordinator.shownMomentObject.clone().set({
          minute: 0,
          second: 0
        });
        this.__hoursMap = {};
        this.hourselectConfig = [];
        _ref = this.hourselectValues;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          hour = _ref[_i];
          label = formatMomentObject.set({
            hour: hour
          }).format(this.hourFormat);
          hourConfig = {
            value: hour,
            label: label
          };
          this.hourselectConfig.push(hourConfig);
          this.__hoursMap[hourConfig.value] = hourConfig;
          if (hourConfig.value === selectedHourValue) {
            hasSelectedHourValue = true;
          }
        }
        if (!hasSelectedHourValue) {
          label = formatMomentObject.set({
            hour: selectedHourValue
          }).format(this.hourFormat);
          hourConfig = {
            value: selectedHourValue,
            label: label
          };
          this.hourselectConfig.push(hourConfig);
          this.__hoursMap[hourConfig.value] = hourConfig;
          return this.__sortConfigObjectsByValue(this.hourselectConfig);
        }
      };

      MonthlyCalendarCoordinator.prototype.__initMinuteObjects = function() {
        var formatMomentObject, hasSelectedMinuteValue, label, minute, minuteConfig, selectedMinuteValue, _i, _len, _ref;
        selectedMinuteValue = this.calendarCoordinator.shownMomentObject.minute();
        hasSelectedMinuteValue = false;
        formatMomentObject = this.calendarCoordinator.shownMomentObject.clone().set({
          second: 0
        });
        this.__minutesMap = {};
        this.minuteselectConfig = [];
        _ref = this.minuteselectValues;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          minute = _ref[_i];
          label = formatMomentObject.set({
            minute: minute
          }).format(this.minuteFormat);
          minuteConfig = {
            value: minute,
            label: label
          };
          this.minuteselectConfig.push(minuteConfig);
          this.__minutesMap[minuteConfig.value] = minuteConfig;
          if (minuteConfig.value === selectedMinuteValue) {
            hasSelectedMinuteValue = true;
          }
        }
        if (!hasSelectedMinuteValue) {
          label = formatMomentObject.set({
            minute: selectedMinuteValue
          }).format(this.minuteFormat);
          minuteConfig = {
            value: selectedMinuteValue,
            label: label
          };
          this.minuteselectConfig.push(minuteConfig);
          this.__minutesMap[minuteConfig.value] = minuteConfig;
          return this.__sortConfigObjectsByValue(this.minuteselectConfig);
        }
      };

      MonthlyCalendarCoordinator.prototype.__setCurrentYear = function() {
        var currentYearNumber;
        currentYearNumber = this.calendarMonth.month.firstDayOfMonth.year();
        this.currentYearObject = this.__yearsMap[currentYearNumber];
        if (this.currentYearObject == null) {
          return typeof console !== "undefined" && console !== null ? typeof console.warn === "function" ? console.warn("The given year, " + currentYearNumber + " is not one of the available choices") : void 0 : void 0;
        }
      };

      MonthlyCalendarCoordinator.prototype.__setCurrentMonth = function() {
        var currentMonthNumber;
        currentMonthNumber = this.calendarMonth.month.firstDayOfMonth.month();
        this.currentMonthObject = this.__monthsMap[currentMonthNumber];
        if (this.currentMonthObject == null) {
          return typeof console !== "undefined" && console !== null ? typeof console.warn === "function" ? console.warn("The given month number, " + currentMonthNumber + " is not one of the available choices") : void 0 : void 0;
        }
      };

      MonthlyCalendarCoordinator.prototype.__setCurrentHour = function() {
        var currentHourNumber;
        currentHourNumber = this.calendarCoordinator.shownMomentObject.hour();
        this.currentHourObject = this.__hoursMap[currentHourNumber];
        if (this.currentHourObject == null) {
          return typeof console !== "undefined" && console !== null ? typeof console.warn === "function" ? console.warn("The given hour, " + currentHourNumber + " is not one of the available choices") : void 0 : void 0;
        }
      };

      MonthlyCalendarCoordinator.prototype.__setCurrentMinute = function() {
        var currentMinuteNumber;
        currentMinuteNumber = this.calendarCoordinator.shownMomentObject.minute();
        this.currentMinuteObject = this.__minutesMap[currentMinuteNumber];
        if (this.currentMinuteObject == null) {
          return typeof console !== "undefined" && console !== null ? typeof console.warn === "function" ? console.warn("The given minute, " + currentMinuteNumber + " is not one of the available choices") : void 0 : void 0;
        }
      };

      MonthlyCalendarCoordinator.prototype.__updateDayObjects = function() {
        var dayNumberObject, daynumber, formatMomentObject, label, _i, _ref, _results;
        formatMomentObject = this.calendarCoordinator.shownMomentObject.clone().set({
          hour: 0,
          minute: 0,
          second: 0
        });
        this.dayobjects = [];
        _results = [];
        for (daynumber = _i = 1, _ref = this.calendarMonth.month.getDaysInMonth(); 1 <= _ref ? _i <= _ref : _i >= _ref; daynumber = 1 <= _ref ? ++_i : --_i) {
          label = formatMomentObject.set({
            date: daynumber
          }).format(this.dayOfMonthSelectFormat);
          dayNumberObject = {
            value: daynumber,
            label: label
          };
          _results.push(this.dayobjects.push(dayNumberObject));
        }
        return _results;
      };

      /*
      Change month to the month containing the given momentObject,
      and select the date.
      
      As long as you change ``@calendarCoordinator.shownMomentObject``, this
      will update everything to mirror the change (selected day, month, year, ...).
      */


      MonthlyCalendarCoordinator.prototype.__changeSelectedDate = function() {
        this.calendarMonth = new CalendarMonth(this.calendarCoordinator, this.calendarCoordinator.shownMomentObject);
        this.__setCurrentYear();
        this.__setCurrentMonth();
        this.__setCurrentHour();
        this.__setCurrentMinute();
        this.__updateDayObjects();
        return this.currentDayObject = this.dayobjects[this.calendarCoordinator.shownMomentObject.date() - 1];
      };

      MonthlyCalendarCoordinator.prototype.handleDayChange = function(momentObject) {
        this.calendarCoordinator.shownMomentObject = momentObject.clone().set({
          hour: this.currentHourObject.value,
          minute: this.currentMinuteObject.value
        });
        return this.__changeSelectedDate();
      };

      MonthlyCalendarCoordinator.prototype.handleCurrentDayObjectChange = function() {
        var momentObject;
        momentObject = moment({
          year: this.currentYearObject.value,
          month: this.currentMonthObject.value,
          day: this.currentDayObject.value
        });
        return this.handleDayChange(momentObject);
      };

      MonthlyCalendarCoordinator.prototype.handleCalendarDayChange = function(calendarDay) {
        return this.handleDayChange(calendarDay.momentObject);
      };

      MonthlyCalendarCoordinator.prototype.handleCurrentMonthChange = function() {
        this.calendarCoordinator.shownMomentObject.set({
          month: this.currentMonthObject.value
        });
        return this.__changeSelectedDate();
      };

      MonthlyCalendarCoordinator.prototype.handleCurrentYearChange = function() {
        this.calendarCoordinator.shownMomentObject.set({
          year: this.currentYearObject.value
        });
        return this.__changeSelectedDate();
      };

      MonthlyCalendarCoordinator.prototype.handleCurrentHourChange = function() {
        this.calendarCoordinator.shownMomentObject.set({
          hour: this.currentHourObject.value
        });
        return this.__changeSelectedDate();
      };

      MonthlyCalendarCoordinator.prototype.handleCurrentMinuteChange = function() {
        this.calendarCoordinator.shownMomentObject.set({
          minute: this.currentMinuteObject.value
        });
        return this.__changeSelectedDate();
      };

      MonthlyCalendarCoordinator.prototype.handleFocusOnCalendarDay = function(calendarDay) {
        return this.lastFocusedMomentObject = calendarDay.momentObject;
      };

      MonthlyCalendarCoordinator.prototype.getLastFocusedMomentObject = function() {
        if (this.lastFocusedMomentObject != null) {
          return this.lastFocusedMomentObject;
        } else {
          return this.calendarCoordinator.shownMomentObject;
        }
      };

      MonthlyCalendarCoordinator.prototype.getDayOfMonthLabelForTableCell = function(calendarDay) {
        return calendarDay.momentObject.format(this.dayOfMonthTableCellFormat);
      };

      MonthlyCalendarCoordinator.prototype.setToToday = function() {
        return this.handleDayChange(this.calendarCoordinator.nowMomentObject.clone());
      };

      return MonthlyCalendarCoordinator;

    })();
    this.$get = function() {
      return {
        MonthlyCalendarCoordinator: MonthlyCalendarCoordinator,
        CalendarCoordinator: CalendarCoordinator
      };
    };
    return this;
  });

}).call(this);
