(function() {
  angular.module('djangoCradmin.multiselect2.services', []).factory('djangoCradminMultiselect2Coordinator', function() {
    /*
    Coordinates between djangoCradminMultiselect2Select
    and djangoCradminMultiselect2Target.
    */

    var Coordinator;
    Coordinator = (function() {
      function Coordinator() {
        this.targets = {};
        this.selectScopes = {};
      }

      Coordinator.prototype.registerTarget = function(targetDomId, targetScope) {
        return this.targets[targetDomId] = targetScope;
      };

      Coordinator.prototype.unregisterTarget = function(targetDomId, targetScope) {
        return delete this.targets[targetDomId];
      };

      Coordinator.prototype.__getTargetScope = function(targetDomId) {
        var targetScope;
        targetScope = this.targets[targetDomId];
        if (targetScope == null) {
          throw Error("No target with ID '" + targetDomId + "' registered with djangoCradminMultiselect2Coordinator.");
        }
        return targetScope;
      };

      Coordinator.prototype.targetScopeExists = function(targetDomId) {
        return this.targets[targetDomId] != null;
      };

      Coordinator.prototype.select = function(selectScope) {
        var targetScope;
        targetScope = this.__getTargetScope(selectScope.getTargetDomId());
        if (!targetScope.isSelected(selectScope)) {
          targetScope.select(selectScope);
          return selectScope.markAsSelected();
        }
      };

      Coordinator.prototype.onDeselect = function(selectButtonDomId) {
        var $selectElement, selectScope;
        $selectElement = angular.element('#' + selectButtonDomId);
        if ($selectElement != null) {
          selectScope = $selectElement.isolateScope();
          if (selectScope != null) {
            return selectScope.onDeselect();
          }
        }
      };

      Coordinator.prototype.isSelected = function(targetDomId, selectScope) {
        var targetScope;
        targetScope = this.__getTargetScope(targetDomId);
        return targetScope.isSelected(selectScope);
      };

      Coordinator.prototype.registerSelectScope = function(selectScope) {
        var listIndex, _ref;
        if (((_ref = this.selectScopes[selectScope.getTargetDomId()]) != null ? _ref.map[selectScope.getDomId()] : void 0) != null) {
          return console.log(("selectScope with id=" + (selectScope.getDomId()) + " is already ") + ("registered for target " + (selectScope.getTargetDomId())));
        } else {
          if (this.selectScopes[selectScope.getTargetDomId()] == null) {
            this.selectScopes[selectScope.getTargetDomId()] = {
              map: {},
              list: []
            };
          }
          listIndex = this.selectScopes[selectScope.getTargetDomId()].list.push(selectScope);
          return this.selectScopes[selectScope.getTargetDomId()].map[selectScope.getDomId()] = listIndex;
        }
      };

      Coordinator.prototype.unregisterSelectScope = function(selectScope) {
        var listIndex, _ref;
        if (((_ref = this.selectScopes[selectScope.getTargetDomId()]) != null ? _ref.map[selectScope.getDomId()] : void 0) != null) {
          listIndex = this.selectScopes[selectScope.getTargetDomId()][selectScope.getDomId()];
          this.selectScopes[selectScope.getTargetDomId()].list.splice(listIndex, 1);
          return delete this.selectScopes[selectScope.getTargetDomId()].map[selectScope.getDomId()];
        } else {
          throw Error(("selectScope with id=" + (selectScope.getDomId()) + " is not ") + ("registered for target " + (selectScope.getTargetDomId())));
        }
      };

      Coordinator.prototype.selectAll = function(targetDomId) {
        var selectScope, _i, _len, _ref, _results;
        _ref = this.selectScopes[targetDomId].list;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          selectScope = _ref[_i];
          _results.push(this.select(selectScope));
        }
        return _results;
      };

      return Coordinator;

    })();
    return new Coordinator();
  });

}).call(this);
