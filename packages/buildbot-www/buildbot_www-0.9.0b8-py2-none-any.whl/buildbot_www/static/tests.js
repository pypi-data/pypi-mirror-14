/**
 * @license AngularJS v1.4.7
 * (c) 2010-2015 Google, Inc. http://angularjs.org
 * License: MIT
 */
(function(window, angular, undefined) {

'use strict';

/**
 * @ngdoc object
 * @name angular.mock
 * @description
 *
 * Namespace from 'angular-mocks.js' which contains testing related code.
 */
angular.mock = {};

/**
 * ! This is a private undocumented service !
 *
 * @name $browser
 *
 * @description
 * This service is a mock implementation of {@link ng.$browser}. It provides fake
 * implementation for commonly used browser apis that are hard to test, e.g. setTimeout, xhr,
 * cookies, etc...
 *
 * The api of this service is the same as that of the real {@link ng.$browser $browser}, except
 * that there are several helper methods available which can be used in tests.
 */
angular.mock.$BrowserProvider = function() {
  this.$get = function() {
    return new angular.mock.$Browser();
  };
};

angular.mock.$Browser = function() {
  var self = this;

  this.isMock = true;
  self.$$url = "http://server/";
  self.$$lastUrl = self.$$url; // used by url polling fn
  self.pollFns = [];

  // TODO(vojta): remove this temporary api
  self.$$completeOutstandingRequest = angular.noop;
  self.$$incOutstandingRequestCount = angular.noop;


  // register url polling fn

  self.onUrlChange = function(listener) {
    self.pollFns.push(
      function() {
        if (self.$$lastUrl !== self.$$url || self.$$state !== self.$$lastState) {
          self.$$lastUrl = self.$$url;
          self.$$lastState = self.$$state;
          listener(self.$$url, self.$$state);
        }
      }
    );

    return listener;
  };

  self.$$applicationDestroyed = angular.noop;
  self.$$checkUrlChange = angular.noop;

  self.deferredFns = [];
  self.deferredNextId = 0;

  self.defer = function(fn, delay) {
    delay = delay || 0;
    self.deferredFns.push({time:(self.defer.now + delay), fn:fn, id: self.deferredNextId});
    self.deferredFns.sort(function(a, b) { return a.time - b.time;});
    return self.deferredNextId++;
  };


  /**
   * @name $browser#defer.now
   *
   * @description
   * Current milliseconds mock time.
   */
  self.defer.now = 0;


  self.defer.cancel = function(deferId) {
    var fnIndex;

    angular.forEach(self.deferredFns, function(fn, index) {
      if (fn.id === deferId) fnIndex = index;
    });

    if (angular.isDefined(fnIndex)) {
      self.deferredFns.splice(fnIndex, 1);
      return true;
    }

    return false;
  };


  /**
   * @name $browser#defer.flush
   *
   * @description
   * Flushes all pending requests and executes the defer callbacks.
   *
   * @param {number=} number of milliseconds to flush. See {@link #defer.now}
   */
  self.defer.flush = function(delay) {
    if (angular.isDefined(delay)) {
      self.defer.now += delay;
    } else {
      if (self.deferredFns.length) {
        self.defer.now = self.deferredFns[self.deferredFns.length - 1].time;
      } else {
        throw new Error('No deferred tasks to be flushed');
      }
    }

    while (self.deferredFns.length && self.deferredFns[0].time <= self.defer.now) {
      self.deferredFns.shift().fn();
    }
  };

  self.$$baseHref = '/';
  self.baseHref = function() {
    return this.$$baseHref;
  };
};
angular.mock.$Browser.prototype = {

/**
  * @name $browser#poll
  *
  * @description
  * run all fns in pollFns
  */
  poll: function poll() {
    angular.forEach(this.pollFns, function(pollFn) {
      pollFn();
    });
  },

  url: function(url, replace, state) {
    if (angular.isUndefined(state)) {
      state = null;
    }
    if (url) {
      this.$$url = url;
      // Native pushState serializes & copies the object; simulate it.
      this.$$state = angular.copy(state);
      return this;
    }

    return this.$$url;
  },

  state: function() {
    return this.$$state;
  },

  notifyWhenNoOutstandingRequests: function(fn) {
    fn();
  }
};


/**
 * @ngdoc provider
 * @name $exceptionHandlerProvider
 *
 * @description
 * Configures the mock implementation of {@link ng.$exceptionHandler} to rethrow or to log errors
 * passed to the `$exceptionHandler`.
 */

/**
 * @ngdoc service
 * @name $exceptionHandler
 *
 * @description
 * Mock implementation of {@link ng.$exceptionHandler} that rethrows or logs errors passed
 * to it. See {@link ngMock.$exceptionHandlerProvider $exceptionHandlerProvider} for configuration
 * information.
 *
 *
 * ```js
 *   describe('$exceptionHandlerProvider', function() {
 *
 *     it('should capture log messages and exceptions', function() {
 *
 *       module(function($exceptionHandlerProvider) {
 *         $exceptionHandlerProvider.mode('log');
 *       });
 *
 *       inject(function($log, $exceptionHandler, $timeout) {
 *         $timeout(function() { $log.log(1); });
 *         $timeout(function() { $log.log(2); throw 'banana peel'; });
 *         $timeout(function() { $log.log(3); });
 *         expect($exceptionHandler.errors).toEqual([]);
 *         expect($log.assertEmpty());
 *         $timeout.flush();
 *         expect($exceptionHandler.errors).toEqual(['banana peel']);
 *         expect($log.log.logs).toEqual([[1], [2], [3]]);
 *       });
 *     });
 *   });
 * ```
 */

angular.mock.$ExceptionHandlerProvider = function() {
  var handler;

  /**
   * @ngdoc method
   * @name $exceptionHandlerProvider#mode
   *
   * @description
   * Sets the logging mode.
   *
   * @param {string} mode Mode of operation, defaults to `rethrow`.
   *
   *   - `log`: Sometimes it is desirable to test that an error is thrown, for this case the `log`
   *            mode stores an array of errors in `$exceptionHandler.errors`, to allow later
   *            assertion of them. See {@link ngMock.$log#assertEmpty assertEmpty()} and
   *            {@link ngMock.$log#reset reset()}
   *   - `rethrow`: If any errors are passed to the handler in tests, it typically means that there
   *                is a bug in the application or test, so this mock will make these tests fail.
   *                For any implementations that expect exceptions to be thrown, the `rethrow` mode
   *                will also maintain a log of thrown errors.
   */
  this.mode = function(mode) {

    switch (mode) {
      case 'log':
      case 'rethrow':
        var errors = [];
        handler = function(e) {
          if (arguments.length == 1) {
            errors.push(e);
          } else {
            errors.push([].slice.call(arguments, 0));
          }
          if (mode === "rethrow") {
            throw e;
          }
        };
        handler.errors = errors;
        break;
      default:
        throw new Error("Unknown mode '" + mode + "', only 'log'/'rethrow' modes are allowed!");
    }
  };

  this.$get = function() {
    return handler;
  };

  this.mode('rethrow');
};


/**
 * @ngdoc service
 * @name $log
 *
 * @description
 * Mock implementation of {@link ng.$log} that gathers all logged messages in arrays
 * (one array per logging level). These arrays are exposed as `logs` property of each of the
 * level-specific log function, e.g. for level `error` the array is exposed as `$log.error.logs`.
 *
 */
angular.mock.$LogProvider = function() {
  var debug = true;

  function concat(array1, array2, index) {
    return array1.concat(Array.prototype.slice.call(array2, index));
  }

  this.debugEnabled = function(flag) {
    if (angular.isDefined(flag)) {
      debug = flag;
      return this;
    } else {
      return debug;
    }
  };

  this.$get = function() {
    var $log = {
      log: function() { $log.log.logs.push(concat([], arguments, 0)); },
      warn: function() { $log.warn.logs.push(concat([], arguments, 0)); },
      info: function() { $log.info.logs.push(concat([], arguments, 0)); },
      error: function() { $log.error.logs.push(concat([], arguments, 0)); },
      debug: function() {
        if (debug) {
          $log.debug.logs.push(concat([], arguments, 0));
        }
      }
    };

    /**
     * @ngdoc method
     * @name $log#reset
     *
     * @description
     * Reset all of the logging arrays to empty.
     */
    $log.reset = function() {
      /**
       * @ngdoc property
       * @name $log#log.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#log `log()`}.
       *
       * @example
       * ```js
       * $log.log('Some Log');
       * var first = $log.log.logs.unshift();
       * ```
       */
      $log.log.logs = [];
      /**
       * @ngdoc property
       * @name $log#info.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#info `info()`}.
       *
       * @example
       * ```js
       * $log.info('Some Info');
       * var first = $log.info.logs.unshift();
       * ```
       */
      $log.info.logs = [];
      /**
       * @ngdoc property
       * @name $log#warn.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#warn `warn()`}.
       *
       * @example
       * ```js
       * $log.warn('Some Warning');
       * var first = $log.warn.logs.unshift();
       * ```
       */
      $log.warn.logs = [];
      /**
       * @ngdoc property
       * @name $log#error.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#error `error()`}.
       *
       * @example
       * ```js
       * $log.error('Some Error');
       * var first = $log.error.logs.unshift();
       * ```
       */
      $log.error.logs = [];
        /**
       * @ngdoc property
       * @name $log#debug.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#debug `debug()`}.
       *
       * @example
       * ```js
       * $log.debug('Some Error');
       * var first = $log.debug.logs.unshift();
       * ```
       */
      $log.debug.logs = [];
    };

    /**
     * @ngdoc method
     * @name $log#assertEmpty
     *
     * @description
     * Assert that all of the logging methods have no logged messages. If any messages are present,
     * an exception is thrown.
     */
    $log.assertEmpty = function() {
      var errors = [];
      angular.forEach(['error', 'warn', 'info', 'log', 'debug'], function(logLevel) {
        angular.forEach($log[logLevel].logs, function(log) {
          angular.forEach(log, function(logItem) {
            errors.push('MOCK $log (' + logLevel + '): ' + String(logItem) + '\n' +
                        (logItem.stack || ''));
          });
        });
      });
      if (errors.length) {
        errors.unshift("Expected $log to be empty! Either a message was logged unexpectedly, or " +
          "an expected log message was not checked and removed:");
        errors.push('');
        throw new Error(errors.join('\n---------\n'));
      }
    };

    $log.reset();
    return $log;
  };
};


/**
 * @ngdoc service
 * @name $interval
 *
 * @description
 * Mock implementation of the $interval service.
 *
 * Use {@link ngMock.$interval#flush `$interval.flush(millis)`} to
 * move forward by `millis` milliseconds and trigger any functions scheduled to run in that
 * time.
 *
 * @param {function()} fn A function that should be called repeatedly.
 * @param {number} delay Number of milliseconds between each function call.
 * @param {number=} [count=0] Number of times to repeat. If not set, or 0, will repeat
 *   indefinitely.
 * @param {boolean=} [invokeApply=true] If set to `false` skips model dirty checking, otherwise
 *   will invoke `fn` within the {@link ng.$rootScope.Scope#$apply $apply} block.
 * @param {...*=} Pass additional parameters to the executed function.
 * @returns {promise} A promise which will be notified on each iteration.
 */
angular.mock.$IntervalProvider = function() {
  this.$get = ['$browser', '$rootScope', '$q', '$$q',
       function($browser,   $rootScope,   $q,   $$q) {
    var repeatFns = [],
        nextRepeatId = 0,
        now = 0;

    var $interval = function(fn, delay, count, invokeApply) {
      var hasParams = arguments.length > 4,
          args = hasParams ? Array.prototype.slice.call(arguments, 4) : [],
          iteration = 0,
          skipApply = (angular.isDefined(invokeApply) && !invokeApply),
          deferred = (skipApply ? $$q : $q).defer(),
          promise = deferred.promise;

      count = (angular.isDefined(count)) ? count : 0;
      promise.then(null, null, (!hasParams) ? fn : function() {
        fn.apply(null, args);
      });

      promise.$$intervalId = nextRepeatId;

      function tick() {
        deferred.notify(iteration++);

        if (count > 0 && iteration >= count) {
          var fnIndex;
          deferred.resolve(iteration);

          angular.forEach(repeatFns, function(fn, index) {
            if (fn.id === promise.$$intervalId) fnIndex = index;
          });

          if (angular.isDefined(fnIndex)) {
            repeatFns.splice(fnIndex, 1);
          }
        }

        if (skipApply) {
          $browser.defer.flush();
        } else {
          $rootScope.$apply();
        }
      }

      repeatFns.push({
        nextTime:(now + delay),
        delay: delay,
        fn: tick,
        id: nextRepeatId,
        deferred: deferred
      });
      repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});

      nextRepeatId++;
      return promise;
    };
    /**
     * @ngdoc method
     * @name $interval#cancel
     *
     * @description
     * Cancels a task associated with the `promise`.
     *
     * @param {promise} promise A promise from calling the `$interval` function.
     * @returns {boolean} Returns `true` if the task was successfully cancelled.
     */
    $interval.cancel = function(promise) {
      if (!promise) return false;
      var fnIndex;

      angular.forEach(repeatFns, function(fn, index) {
        if (fn.id === promise.$$intervalId) fnIndex = index;
      });

      if (angular.isDefined(fnIndex)) {
        repeatFns[fnIndex].deferred.reject('canceled');
        repeatFns.splice(fnIndex, 1);
        return true;
      }

      return false;
    };

    /**
     * @ngdoc method
     * @name $interval#flush
     * @description
     *
     * Runs interval tasks scheduled to be run in the next `millis` milliseconds.
     *
     * @param {number=} millis maximum timeout amount to flush up until.
     *
     * @return {number} The amount of time moved forward.
     */
    $interval.flush = function(millis) {
      now += millis;
      while (repeatFns.length && repeatFns[0].nextTime <= now) {
        var task = repeatFns[0];
        task.fn();
        task.nextTime += task.delay;
        repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});
      }
      return millis;
    };

    return $interval;
  }];
};


/* jshint -W101 */
/* The R_ISO8061_STR regex is never going to fit into the 100 char limit!
 * This directive should go inside the anonymous function but a bug in JSHint means that it would
 * not be enacted early enough to prevent the warning.
 */
var R_ISO8061_STR = /^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?:\:?(\d\d)(?:\:?(\d\d)(?:\.(\d{3}))?)?)?(Z|([+-])(\d\d):?(\d\d)))?$/;

function jsonStringToDate(string) {
  var match;
  if (match = string.match(R_ISO8061_STR)) {
    var date = new Date(0),
        tzHour = 0,
        tzMin  = 0;
    if (match[9]) {
      tzHour = toInt(match[9] + match[10]);
      tzMin = toInt(match[9] + match[11]);
    }
    date.setUTCFullYear(toInt(match[1]), toInt(match[2]) - 1, toInt(match[3]));
    date.setUTCHours(toInt(match[4] || 0) - tzHour,
                     toInt(match[5] || 0) - tzMin,
                     toInt(match[6] || 0),
                     toInt(match[7] || 0));
    return date;
  }
  return string;
}

function toInt(str) {
  return parseInt(str, 10);
}

function padNumber(num, digits, trim) {
  var neg = '';
  if (num < 0) {
    neg =  '-';
    num = -num;
  }
  num = '' + num;
  while (num.length < digits) num = '0' + num;
  if (trim) {
    num = num.substr(num.length - digits);
  }
  return neg + num;
}


/**
 * @ngdoc type
 * @name angular.mock.TzDate
 * @description
 *
 * *NOTE*: this is not an injectable instance, just a globally available mock class of `Date`.
 *
 * Mock of the Date type which has its timezone specified via constructor arg.
 *
 * The main purpose is to create Date-like instances with timezone fixed to the specified timezone
 * offset, so that we can test code that depends on local timezone settings without dependency on
 * the time zone settings of the machine where the code is running.
 *
 * @param {number} offset Offset of the *desired* timezone in hours (fractions will be honored)
 * @param {(number|string)} timestamp Timestamp representing the desired time in *UTC*
 *
 * @example
 * !!!! WARNING !!!!!
 * This is not a complete Date object so only methods that were implemented can be called safely.
 * To make matters worse, TzDate instances inherit stuff from Date via a prototype.
 *
 * We do our best to intercept calls to "unimplemented" methods, but since the list of methods is
 * incomplete we might be missing some non-standard methods. This can result in errors like:
 * "Date.prototype.foo called on incompatible Object".
 *
 * ```js
 * var newYearInBratislava = new TzDate(-1, '2009-12-31T23:00:00Z');
 * newYearInBratislava.getTimezoneOffset() => -60;
 * newYearInBratislava.getFullYear() => 2010;
 * newYearInBratislava.getMonth() => 0;
 * newYearInBratislava.getDate() => 1;
 * newYearInBratislava.getHours() => 0;
 * newYearInBratislava.getMinutes() => 0;
 * newYearInBratislava.getSeconds() => 0;
 * ```
 *
 */
angular.mock.TzDate = function(offset, timestamp) {
  var self = new Date(0);
  if (angular.isString(timestamp)) {
    var tsStr = timestamp;

    self.origDate = jsonStringToDate(timestamp);

    timestamp = self.origDate.getTime();
    if (isNaN(timestamp)) {
      throw {
        name: "Illegal Argument",
        message: "Arg '" + tsStr + "' passed into TzDate constructor is not a valid date string"
      };
    }
  } else {
    self.origDate = new Date(timestamp);
  }

  var localOffset = new Date(timestamp).getTimezoneOffset();
  self.offsetDiff = localOffset * 60 * 1000 - offset * 1000 * 60 * 60;
  self.date = new Date(timestamp + self.offsetDiff);

  self.getTime = function() {
    return self.date.getTime() - self.offsetDiff;
  };

  self.toLocaleDateString = function() {
    return self.date.toLocaleDateString();
  };

  self.getFullYear = function() {
    return self.date.getFullYear();
  };

  self.getMonth = function() {
    return self.date.getMonth();
  };

  self.getDate = function() {
    return self.date.getDate();
  };

  self.getHours = function() {
    return self.date.getHours();
  };

  self.getMinutes = function() {
    return self.date.getMinutes();
  };

  self.getSeconds = function() {
    return self.date.getSeconds();
  };

  self.getMilliseconds = function() {
    return self.date.getMilliseconds();
  };

  self.getTimezoneOffset = function() {
    return offset * 60;
  };

  self.getUTCFullYear = function() {
    return self.origDate.getUTCFullYear();
  };

  self.getUTCMonth = function() {
    return self.origDate.getUTCMonth();
  };

  self.getUTCDate = function() {
    return self.origDate.getUTCDate();
  };

  self.getUTCHours = function() {
    return self.origDate.getUTCHours();
  };

  self.getUTCMinutes = function() {
    return self.origDate.getUTCMinutes();
  };

  self.getUTCSeconds = function() {
    return self.origDate.getUTCSeconds();
  };

  self.getUTCMilliseconds = function() {
    return self.origDate.getUTCMilliseconds();
  };

  self.getDay = function() {
    return self.date.getDay();
  };

  // provide this method only on browsers that already have it
  if (self.toISOString) {
    self.toISOString = function() {
      return padNumber(self.origDate.getUTCFullYear(), 4) + '-' +
            padNumber(self.origDate.getUTCMonth() + 1, 2) + '-' +
            padNumber(self.origDate.getUTCDate(), 2) + 'T' +
            padNumber(self.origDate.getUTCHours(), 2) + ':' +
            padNumber(self.origDate.getUTCMinutes(), 2) + ':' +
            padNumber(self.origDate.getUTCSeconds(), 2) + '.' +
            padNumber(self.origDate.getUTCMilliseconds(), 3) + 'Z';
    };
  }

  //hide all methods not implemented in this mock that the Date prototype exposes
  var unimplementedMethods = ['getUTCDay',
      'getYear', 'setDate', 'setFullYear', 'setHours', 'setMilliseconds',
      'setMinutes', 'setMonth', 'setSeconds', 'setTime', 'setUTCDate', 'setUTCFullYear',
      'setUTCHours', 'setUTCMilliseconds', 'setUTCMinutes', 'setUTCMonth', 'setUTCSeconds',
      'setYear', 'toDateString', 'toGMTString', 'toJSON', 'toLocaleFormat', 'toLocaleString',
      'toLocaleTimeString', 'toSource', 'toString', 'toTimeString', 'toUTCString', 'valueOf'];

  angular.forEach(unimplementedMethods, function(methodName) {
    self[methodName] = function() {
      throw new Error("Method '" + methodName + "' is not implemented in the TzDate mock");
    };
  });

  return self;
};

//make "tzDateInstance instanceof Date" return true
angular.mock.TzDate.prototype = Date.prototype;
/* jshint +W101 */

angular.mock.animate = angular.module('ngAnimateMock', ['ng'])

  .config(['$provide', function($provide) {

    $provide.factory('$$forceReflow', function() {
      function reflowFn() {
        reflowFn.totalReflows++;
      }
      reflowFn.totalReflows = 0;
      return reflowFn;
    });

    $provide.factory('$$animateAsyncRun', function() {
      var queue = [];
      var queueFn = function() {
        return function(fn) {
          queue.push(fn);
        };
      };
      queueFn.flush = function() {
        if (queue.length === 0) return false;

        for (var i = 0; i < queue.length; i++) {
          queue[i]();
        }
        queue = [];

        return true;
      };
      return queueFn;
    });

    $provide.decorator('$animate', ['$delegate', '$timeout', '$browser', '$$rAF',
                                    '$$forceReflow', '$$animateAsyncRun', '$rootScope',
                            function($delegate,   $timeout,   $browser,   $$rAF,
                                     $$forceReflow,   $$animateAsyncRun,  $rootScope) {
      var animate = {
        queue: [],
        cancel: $delegate.cancel,
        on: $delegate.on,
        off: $delegate.off,
        pin: $delegate.pin,
        get reflows() {
          return $$forceReflow.totalReflows;
        },
        enabled: $delegate.enabled,
        flush: function() {
          $rootScope.$digest();

          var doNextRun, somethingFlushed = false;
          do {
            doNextRun = false;

            if ($$rAF.queue.length) {
              $$rAF.flush();
              doNextRun = somethingFlushed = true;
            }

            if ($$animateAsyncRun.flush()) {
              doNextRun = somethingFlushed = true;
            }
          } while (doNextRun);

          if (!somethingFlushed) {
            throw new Error('No pending animations ready to be closed or flushed');
          }

          $rootScope.$digest();
        }
      };

      angular.forEach(
        ['animate','enter','leave','move','addClass','removeClass','setClass'], function(method) {
        animate[method] = function() {
          animate.queue.push({
            event: method,
            element: arguments[0],
            options: arguments[arguments.length - 1],
            args: arguments
          });
          return $delegate[method].apply($delegate, arguments);
        };
      });

      return animate;
    }]);

  }]);


/**
 * @ngdoc function
 * @name angular.mock.dump
 * @description
 *
 * *NOTE*: this is not an injectable instance, just a globally available function.
 *
 * Method for serializing common angular objects (scope, elements, etc..) into strings, useful for
 * debugging.
 *
 * This method is also available on window, where it can be used to display objects on debug
 * console.
 *
 * @param {*} object - any object to turn into string.
 * @return {string} a serialized string of the argument
 */
angular.mock.dump = function(object) {
  return serialize(object);

  function serialize(object) {
    var out;

    if (angular.isElement(object)) {
      object = angular.element(object);
      out = angular.element('<div></div>');
      angular.forEach(object, function(element) {
        out.append(angular.element(element).clone());
      });
      out = out.html();
    } else if (angular.isArray(object)) {
      out = [];
      angular.forEach(object, function(o) {
        out.push(serialize(o));
      });
      out = '[ ' + out.join(', ') + ' ]';
    } else if (angular.isObject(object)) {
      if (angular.isFunction(object.$eval) && angular.isFunction(object.$apply)) {
        out = serializeScope(object);
      } else if (object instanceof Error) {
        out = object.stack || ('' + object.name + ': ' + object.message);
      } else {
        // TODO(i): this prevents methods being logged,
        // we should have a better way to serialize objects
        out = angular.toJson(object, true);
      }
    } else {
      out = String(object);
    }

    return out;
  }

  function serializeScope(scope, offset) {
    offset = offset ||  '  ';
    var log = [offset + 'Scope(' + scope.$id + '): {'];
    for (var key in scope) {
      if (Object.prototype.hasOwnProperty.call(scope, key) && !key.match(/^(\$|this)/)) {
        log.push('  ' + key + ': ' + angular.toJson(scope[key]));
      }
    }
    var child = scope.$$childHead;
    while (child) {
      log.push(serializeScope(child, offset + '  '));
      child = child.$$nextSibling;
    }
    log.push('}');
    return log.join('\n' + offset);
  }
};

/**
 * @ngdoc service
 * @name $httpBackend
 * @description
 * Fake HTTP backend implementation suitable for unit testing applications that use the
 * {@link ng.$http $http service}.
 *
 * *Note*: For fake HTTP backend implementation suitable for end-to-end testing or backend-less
 * development please see {@link ngMockE2E.$httpBackend e2e $httpBackend mock}.
 *
 * During unit testing, we want our unit tests to run quickly and have no external dependencies so
 * we don’t want to send [XHR](https://developer.mozilla.org/en/xmlhttprequest) or
 * [JSONP](http://en.wikipedia.org/wiki/JSONP) requests to a real server. All we really need is
 * to verify whether a certain request has been sent or not, or alternatively just let the
 * application make requests, respond with pre-trained responses and assert that the end result is
 * what we expect it to be.
 *
 * This mock implementation can be used to respond with static or dynamic responses via the
 * `expect` and `when` apis and their shortcuts (`expectGET`, `whenPOST`, etc).
 *
 * When an Angular application needs some data from a server, it calls the $http service, which
 * sends the request to a real server using $httpBackend service. With dependency injection, it is
 * easy to inject $httpBackend mock (which has the same API as $httpBackend) and use it to verify
 * the requests and respond with some testing data without sending a request to a real server.
 *
 * There are two ways to specify what test data should be returned as http responses by the mock
 * backend when the code under test makes http requests:
 *
 * - `$httpBackend.expect` - specifies a request expectation
 * - `$httpBackend.when` - specifies a backend definition
 *
 *
 * # Request Expectations vs Backend Definitions
 *
 * Request expectations provide a way to make assertions about requests made by the application and
 * to define responses for those requests. The test will fail if the expected requests are not made
 * or they are made in the wrong order.
 *
 * Backend definitions allow you to define a fake backend for your application which doesn't assert
 * if a particular request was made or not, it just returns a trained response if a request is made.
 * The test will pass whether or not the request gets made during testing.
 *
 *
 * <table class="table">
 *   <tr><th width="220px"></th><th>Request expectations</th><th>Backend definitions</th></tr>
 *   <tr>
 *     <th>Syntax</th>
 *     <td>.expect(...).respond(...)</td>
 *     <td>.when(...).respond(...)</td>
 *   </tr>
 *   <tr>
 *     <th>Typical usage</th>
 *     <td>strict unit tests</td>
 *     <td>loose (black-box) unit testing</td>
 *   </tr>
 *   <tr>
 *     <th>Fulfills multiple requests</th>
 *     <td>NO</td>
 *     <td>YES</td>
 *   </tr>
 *   <tr>
 *     <th>Order of requests matters</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Request required</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Response required</th>
 *     <td>optional (see below)</td>
 *     <td>YES</td>
 *   </tr>
 * </table>
 *
 * In cases where both backend definitions and request expectations are specified during unit
 * testing, the request expectations are evaluated first.
 *
 * If a request expectation has no response specified, the algorithm will search your backend
 * definitions for an appropriate response.
 *
 * If a request didn't match any expectation or if the expectation doesn't have the response
 * defined, the backend definitions are evaluated in sequential order to see if any of them match
 * the request. The response from the first matched definition is returned.
 *
 *
 * # Flushing HTTP requests
 *
 * The $httpBackend used in production always responds to requests asynchronously. If we preserved
 * this behavior in unit testing, we'd have to create async unit tests, which are hard to write,
 * to follow and to maintain. But neither can the testing mock respond synchronously; that would
 * change the execution of the code under test. For this reason, the mock $httpBackend has a
 * `flush()` method, which allows the test to explicitly flush pending requests. This preserves
 * the async api of the backend, while allowing the test to execute synchronously.
 *
 *
 * # Unit testing with mock $httpBackend
 * The following code shows how to setup and use the mock backend when unit testing a controller.
 * First we create the controller under test:
 *
  ```js
  // The module code
  angular
    .module('MyApp', [])
    .controller('MyController', MyController);

  // The controller code
  function MyController($scope, $http) {
    var authToken;

    $http.get('/auth.py').success(function(data, status, headers) {
      authToken = headers('A-Token');
      $scope.user = data;
    });

    $scope.saveMessage = function(message) {
      var headers = { 'Authorization': authToken };
      $scope.status = 'Saving...';

      $http.post('/add-msg.py', message, { headers: headers } ).success(function(response) {
        $scope.status = '';
      }).error(function() {
        $scope.status = 'Failed...';
      });
    };
  }
  ```
 *
 * Now we setup the mock backend and create the test specs:
 *
  ```js
    // testing controller
    describe('MyController', function() {
       var $httpBackend, $rootScope, createController, authRequestHandler;

       // Set up the module
       beforeEach(module('MyApp'));

       beforeEach(inject(function($injector) {
         // Set up the mock http service responses
         $httpBackend = $injector.get('$httpBackend');
         // backend definition common for all tests
         authRequestHandler = $httpBackend.when('GET', '/auth.py')
                                .respond({userId: 'userX'}, {'A-Token': 'xxx'});

         // Get hold of a scope (i.e. the root scope)
         $rootScope = $injector.get('$rootScope');
         // The $controller service is used to create instances of controllers
         var $controller = $injector.get('$controller');

         createController = function() {
           return $controller('MyController', {'$scope' : $rootScope });
         };
       }));


       afterEach(function() {
         $httpBackend.verifyNoOutstandingExpectation();
         $httpBackend.verifyNoOutstandingRequest();
       });


       it('should fetch authentication token', function() {
         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
       });


       it('should fail authentication', function() {

         // Notice how you can change the response even after it was set
         authRequestHandler.respond(401, '');

         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
         expect($rootScope.status).toBe('Failed...');
       });


       it('should send msg to server', function() {
         var controller = createController();
         $httpBackend.flush();

         // now you don’t care about the authentication, but
         // the controller will still send the request and
         // $httpBackend will respond without you having to
         // specify the expectation and response for this request

         $httpBackend.expectPOST('/add-msg.py', 'message content').respond(201, '');
         $rootScope.saveMessage('message content');
         expect($rootScope.status).toBe('Saving...');
         $httpBackend.flush();
         expect($rootScope.status).toBe('');
       });


       it('should send auth header', function() {
         var controller = createController();
         $httpBackend.flush();

         $httpBackend.expectPOST('/add-msg.py', undefined, function(headers) {
           // check if the header was sent, if it wasn't the expectation won't
           // match the request and the test will fail
           return headers['Authorization'] == 'xxx';
         }).respond(201, '');

         $rootScope.saveMessage('whatever');
         $httpBackend.flush();
       });
    });
   ```
 */
angular.mock.$HttpBackendProvider = function() {
  this.$get = ['$rootScope', '$timeout', createHttpBackendMock];
};

/**
 * General factory function for $httpBackend mock.
 * Returns instance for unit testing (when no arguments specified):
 *   - passing through is disabled
 *   - auto flushing is disabled
 *
 * Returns instance for e2e testing (when `$delegate` and `$browser` specified):
 *   - passing through (delegating request to real backend) is enabled
 *   - auto flushing is enabled
 *
 * @param {Object=} $delegate Real $httpBackend instance (allow passing through if specified)
 * @param {Object=} $browser Auto-flushing enabled if specified
 * @return {Object} Instance of $httpBackend mock
 */
function createHttpBackendMock($rootScope, $timeout, $delegate, $browser) {
  var definitions = [],
      expectations = [],
      responses = [],
      responsesPush = angular.bind(responses, responses.push),
      copy = angular.copy;

  function createResponse(status, data, headers, statusText) {
    if (angular.isFunction(status)) return status;

    return function() {
      return angular.isNumber(status)
          ? [status, data, headers, statusText]
          : [200, status, data, headers];
    };
  }

  // TODO(vojta): change params to: method, url, data, headers, callback
  function $httpBackend(method, url, data, callback, headers, timeout, withCredentials) {
    var xhr = new MockXhr(),
        expectation = expectations[0],
        wasExpected = false;

    function prettyPrint(data) {
      return (angular.isString(data) || angular.isFunction(data) || data instanceof RegExp)
          ? data
          : angular.toJson(data);
    }

    function wrapResponse(wrapped) {
      if (!$browser && timeout) {
        timeout.then ? timeout.then(handleTimeout) : $timeout(handleTimeout, timeout);
      }

      return handleResponse;

      function handleResponse() {
        var response = wrapped.response(method, url, data, headers);
        xhr.$$respHeaders = response[2];
        callback(copy(response[0]), copy(response[1]), xhr.getAllResponseHeaders(),
                 copy(response[3] || ''));
      }

      function handleTimeout() {
        for (var i = 0, ii = responses.length; i < ii; i++) {
          if (responses[i] === handleResponse) {
            responses.splice(i, 1);
            callback(-1, undefined, '');
            break;
          }
        }
      }
    }

    if (expectation && expectation.match(method, url)) {
      if (!expectation.matchData(data)) {
        throw new Error('Expected ' + expectation + ' with different data\n' +
            'EXPECTED: ' + prettyPrint(expectation.data) + '\nGOT:      ' + data);
      }

      if (!expectation.matchHeaders(headers)) {
        throw new Error('Expected ' + expectation + ' with different headers\n' +
                        'EXPECTED: ' + prettyPrint(expectation.headers) + '\nGOT:      ' +
                        prettyPrint(headers));
      }

      expectations.shift();

      if (expectation.response) {
        responses.push(wrapResponse(expectation));
        return;
      }
      wasExpected = true;
    }

    var i = -1, definition;
    while ((definition = definitions[++i])) {
      if (definition.match(method, url, data, headers || {})) {
        if (definition.response) {
          // if $browser specified, we do auto flush all requests
          ($browser ? $browser.defer : responsesPush)(wrapResponse(definition));
        } else if (definition.passThrough) {
          $delegate(method, url, data, callback, headers, timeout, withCredentials);
        } else throw new Error('No response defined !');
        return;
      }
    }
    throw wasExpected ?
        new Error('No response defined !') :
        new Error('Unexpected request: ' + method + ' ' + url + '\n' +
                  (expectation ? 'Expected ' + expectation : 'No more request expected'));
  }

  /**
   * @ngdoc method
   * @name $httpBackend#when
   * @description
   * Creates a new backend definition.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   *
   *  - respond –
   *      `{function([status,] data[, headers, statusText])
   *      | function(function(method, url, data, headers)}`
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (string), response
   *    headers (Object), and the text for the status (string). The respond method returns the
   *    `requestHandler` object for possible overrides.
   */
  $httpBackend.when = function(method, url, data, headers) {
    var definition = new MockHttpExpectation(method, url, data, headers),
        chain = {
          respond: function(status, data, headers, statusText) {
            definition.passThrough = undefined;
            definition.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    if ($browser) {
      chain.passThrough = function() {
        definition.response = undefined;
        definition.passThrough = true;
        return chain;
      };
    }

    definitions.push(definition);
    return chain;
  };

  /**
   * @ngdoc method
   * @name $httpBackend#whenGET
   * @description
   * Creates a new backend definition for GET requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenHEAD
   * @description
   * Creates a new backend definition for HEAD requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenDELETE
   * @description
   * Creates a new backend definition for DELETE requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPOST
   * @description
   * Creates a new backend definition for POST requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPUT
   * @description
   * Creates a new backend definition for PUT requests.  For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenJSONP
   * @description
   * Creates a new backend definition for JSONP requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */
  createShortMethods('when');


  /**
   * @ngdoc method
   * @name $httpBackend#expect
   * @description
   * Creates a new request expectation.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current expectation.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *  request is handled. You can save this object for later use and invoke `respond` again in
   *  order to change how a matched request is handled.
   *
   *  - respond –
   *    `{function([status,] data[, headers, statusText])
   *    | function(function(method, url, data, headers)}`
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (string), response
   *    headers (Object), and the text for the status (string). The respond method returns the
   *    `requestHandler` object for possible overrides.
   */
  $httpBackend.expect = function(method, url, data, headers) {
    var expectation = new MockHttpExpectation(method, url, data, headers),
        chain = {
          respond: function(status, data, headers, statusText) {
            expectation.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    expectations.push(expectation);
    return chain;
  };


  /**
   * @ngdoc method
   * @name $httpBackend#expectGET
   * @description
   * Creates a new request expectation for GET requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled. See #expect for more info.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectHEAD
   * @description
   * Creates a new request expectation for HEAD requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectDELETE
   * @description
   * Creates a new request expectation for DELETE requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPOST
   * @description
   * Creates a new request expectation for POST requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPUT
   * @description
   * Creates a new request expectation for PUT requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPATCH
   * @description
   * Creates a new request expectation for PATCH requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectJSONP
   * @description
   * Creates a new request expectation for JSONP requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives an url
   *   and returns true if the url matches the current definition.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */
  createShortMethods('expect');


  /**
   * @ngdoc method
   * @name $httpBackend#flush
   * @description
   * Flushes all pending requests using the trained responses.
   *
   * @param {number=} count Number of responses to flush (in the order they arrived). If undefined,
   *   all pending requests will be flushed. If there are no pending requests when the flush method
   *   is called an exception is thrown (as this typically a sign of programming error).
   */
  $httpBackend.flush = function(count, digest) {
    if (digest !== false) $rootScope.$digest();
    if (!responses.length) throw new Error('No pending request to flush !');

    if (angular.isDefined(count) && count !== null) {
      while (count--) {
        if (!responses.length) throw new Error('No more pending request to flush !');
        responses.shift()();
      }
    } else {
      while (responses.length) {
        responses.shift()();
      }
    }
    $httpBackend.verifyNoOutstandingExpectation(digest);
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingExpectation
   * @description
   * Verifies that all of the requests defined via the `expect` api were made. If any of the
   * requests were not made, verifyNoOutstandingExpectation throws an exception.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingExpectation);
   * ```
   */
  $httpBackend.verifyNoOutstandingExpectation = function(digest) {
    if (digest !== false) $rootScope.$digest();
    if (expectations.length) {
      throw new Error('Unsatisfied requests: ' + expectations.join(', '));
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingRequest
   * @description
   * Verifies that there are no outstanding requests that need to be flushed.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingRequest);
   * ```
   */
  $httpBackend.verifyNoOutstandingRequest = function() {
    if (responses.length) {
      throw new Error('Unflushed requests: ' + responses.length);
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#resetExpectations
   * @description
   * Resets all request expectations, but preserves all backend definitions. Typically, you would
   * call resetExpectations during a multiple-phase test when you want to reuse the same instance of
   * $httpBackend mock.
   */
  $httpBackend.resetExpectations = function() {
    expectations.length = 0;
    responses.length = 0;
  };

  return $httpBackend;


  function createShortMethods(prefix) {
    angular.forEach(['GET', 'DELETE', 'JSONP', 'HEAD'], function(method) {
     $httpBackend[prefix + method] = function(url, headers) {
       return $httpBackend[prefix](method, url, undefined, headers);
     };
    });

    angular.forEach(['PUT', 'POST', 'PATCH'], function(method) {
      $httpBackend[prefix + method] = function(url, data, headers) {
        return $httpBackend[prefix](method, url, data, headers);
      };
    });
  }
}

function MockHttpExpectation(method, url, data, headers) {

  this.data = data;
  this.headers = headers;

  this.match = function(m, u, d, h) {
    if (method != m) return false;
    if (!this.matchUrl(u)) return false;
    if (angular.isDefined(d) && !this.matchData(d)) return false;
    if (angular.isDefined(h) && !this.matchHeaders(h)) return false;
    return true;
  };

  this.matchUrl = function(u) {
    if (!url) return true;
    if (angular.isFunction(url.test)) return url.test(u);
    if (angular.isFunction(url)) return url(u);
    return url == u;
  };

  this.matchHeaders = function(h) {
    if (angular.isUndefined(headers)) return true;
    if (angular.isFunction(headers)) return headers(h);
    return angular.equals(headers, h);
  };

  this.matchData = function(d) {
    if (angular.isUndefined(data)) return true;
    if (data && angular.isFunction(data.test)) return data.test(d);
    if (data && angular.isFunction(data)) return data(d);
    if (data && !angular.isString(data)) {
      return angular.equals(angular.fromJson(angular.toJson(data)), angular.fromJson(d));
    }
    return data == d;
  };

  this.toString = function() {
    return method + ' ' + url;
  };
}

function createMockXhr() {
  return new MockXhr();
}

function MockXhr() {

  // hack for testing $http, $httpBackend
  MockXhr.$$lastInstance = this;

  this.open = function(method, url, async) {
    this.$$method = method;
    this.$$url = url;
    this.$$async = async;
    this.$$reqHeaders = {};
    this.$$respHeaders = {};
  };

  this.send = function(data) {
    this.$$data = data;
  };

  this.setRequestHeader = function(key, value) {
    this.$$reqHeaders[key] = value;
  };

  this.getResponseHeader = function(name) {
    // the lookup must be case insensitive,
    // that's why we try two quick lookups first and full scan last
    var header = this.$$respHeaders[name];
    if (header) return header;

    name = angular.lowercase(name);
    header = this.$$respHeaders[name];
    if (header) return header;

    header = undefined;
    angular.forEach(this.$$respHeaders, function(headerVal, headerName) {
      if (!header && angular.lowercase(headerName) == name) header = headerVal;
    });
    return header;
  };

  this.getAllResponseHeaders = function() {
    var lines = [];

    angular.forEach(this.$$respHeaders, function(value, key) {
      lines.push(key + ': ' + value);
    });
    return lines.join('\n');
  };

  this.abort = angular.noop;
}


/**
 * @ngdoc service
 * @name $timeout
 * @description
 *
 * This service is just a simple decorator for {@link ng.$timeout $timeout} service
 * that adds a "flush" and "verifyNoPendingTasks" methods.
 */

angular.mock.$TimeoutDecorator = ['$delegate', '$browser', function($delegate, $browser) {

  /**
   * @ngdoc method
   * @name $timeout#flush
   * @description
   *
   * Flushes the queue of pending tasks.
   *
   * @param {number=} delay maximum timeout amount to flush up until
   */
  $delegate.flush = function(delay) {
    $browser.defer.flush(delay);
  };

  /**
   * @ngdoc method
   * @name $timeout#verifyNoPendingTasks
   * @description
   *
   * Verifies that there are no pending tasks that need to be flushed.
   */
  $delegate.verifyNoPendingTasks = function() {
    if ($browser.deferredFns.length) {
      throw new Error('Deferred tasks to flush (' + $browser.deferredFns.length + '): ' +
          formatPendingTasksAsString($browser.deferredFns));
    }
  };

  function formatPendingTasksAsString(tasks) {
    var result = [];
    angular.forEach(tasks, function(task) {
      result.push('{id: ' + task.id + ', ' + 'time: ' + task.time + '}');
    });

    return result.join(', ');
  }

  return $delegate;
}];

angular.mock.$RAFDecorator = ['$delegate', function($delegate) {
  var rafFn = function(fn) {
    var index = rafFn.queue.length;
    rafFn.queue.push(fn);
    return function() {
      rafFn.queue.splice(index, 1);
    };
  };

  rafFn.queue = [];
  rafFn.supported = $delegate.supported;

  rafFn.flush = function() {
    if (rafFn.queue.length === 0) {
      throw new Error('No rAF callbacks present');
    }

    var length = rafFn.queue.length;
    for (var i = 0; i < length; i++) {
      rafFn.queue[i]();
    }

    rafFn.queue = rafFn.queue.slice(i);
  };

  return rafFn;
}];

/**
 *
 */
angular.mock.$RootElementProvider = function() {
  this.$get = function() {
    return angular.element('<div ng-app></div>');
  };
};

/**
 * @ngdoc service
 * @name $controller
 * @description
 * A decorator for {@link ng.$controller} with additional `bindings` parameter, useful when testing
 * controllers of directives that use {@link $compile#-bindtocontroller- `bindToController`}.
 *
 *
 * ## Example
 *
 * ```js
 *
 * // Directive definition ...
 *
 * myMod.directive('myDirective', {
 *   controller: 'MyDirectiveController',
 *   bindToController: {
 *     name: '@'
 *   }
 * });
 *
 *
 * // Controller definition ...
 *
 * myMod.controller('MyDirectiveController', ['log', function($log) {
 *   $log.info(this.name);
 * })];
 *
 *
 * // In a test ...
 *
 * describe('myDirectiveController', function() {
 *   it('should write the bound name to the log', inject(function($controller, $log) {
 *     var ctrl = $controller('MyDirectiveController', { /* no locals &#42;/ }, { name: 'Clark Kent' });
 *     expect(ctrl.name).toEqual('Clark Kent');
 *     expect($log.info.logs).toEqual(['Clark Kent']);
 *   });
 * });
 *
 * ```
 *
 * @param {Function|string} constructor If called with a function then it's considered to be the
 *    controller constructor function. Otherwise it's considered to be a string which is used
 *    to retrieve the controller constructor using the following steps:
 *
 *    * check if a controller with given name is registered via `$controllerProvider`
 *    * check if evaluating the string on the current scope returns a constructor
 *    * if $controllerProvider#allowGlobals, check `window[constructor]` on the global
 *      `window` object (not recommended)
 *
 *    The string can use the `controller as property` syntax, where the controller instance is published
 *    as the specified property on the `scope`; the `scope` must be injected into `locals` param for this
 *    to work correctly.
 *
 * @param {Object} locals Injection locals for Controller.
 * @param {Object=} bindings Properties to add to the controller before invoking the constructor. This is used
 *                           to simulate the `bindToController` feature and simplify certain kinds of tests.
 * @return {Object} Instance of given controller.
 */
angular.mock.$ControllerDecorator = ['$delegate', function($delegate) {
  return function(expression, locals, later, ident) {
    if (later && typeof later === 'object') {
      var create = $delegate(expression, locals, true, ident);
      angular.extend(create.instance, later);
      return create();
    }
    return $delegate(expression, locals, later, ident);
  };
}];


/**
 * @ngdoc module
 * @name ngMock
 * @packageName angular-mocks
 * @description
 *
 * # ngMock
 *
 * The `ngMock` module provides support to inject and mock Angular services into unit tests.
 * In addition, ngMock also extends various core ng services such that they can be
 * inspected and controlled in a synchronous manner within test code.
 *
 *
 * <div doc-module-components="ngMock"></div>
 *
 */
angular.module('ngMock', ['ng']).provider({
  $browser: angular.mock.$BrowserProvider,
  $exceptionHandler: angular.mock.$ExceptionHandlerProvider,
  $log: angular.mock.$LogProvider,
  $interval: angular.mock.$IntervalProvider,
  $httpBackend: angular.mock.$HttpBackendProvider,
  $rootElement: angular.mock.$RootElementProvider
}).config(['$provide', function($provide) {
  $provide.decorator('$timeout', angular.mock.$TimeoutDecorator);
  $provide.decorator('$$rAF', angular.mock.$RAFDecorator);
  $provide.decorator('$rootScope', angular.mock.$RootScopeDecorator);
  $provide.decorator('$controller', angular.mock.$ControllerDecorator);
}]);

/**
 * @ngdoc module
 * @name ngMockE2E
 * @module ngMockE2E
 * @packageName angular-mocks
 * @description
 *
 * The `ngMockE2E` is an angular module which contains mocks suitable for end-to-end testing.
 * Currently there is only one mock present in this module -
 * the {@link ngMockE2E.$httpBackend e2e $httpBackend} mock.
 */
angular.module('ngMockE2E', ['ng']).config(['$provide', function($provide) {
  $provide.decorator('$httpBackend', angular.mock.e2e.$httpBackendDecorator);
}]);

/**
 * @ngdoc service
 * @name $httpBackend
 * @module ngMockE2E
 * @description
 * Fake HTTP backend implementation suitable for end-to-end testing or backend-less development of
 * applications that use the {@link ng.$http $http service}.
 *
 * *Note*: For fake http backend implementation suitable for unit testing please see
 * {@link ngMock.$httpBackend unit-testing $httpBackend mock}.
 *
 * This implementation can be used to respond with static or dynamic responses via the `when` api
 * and its shortcuts (`whenGET`, `whenPOST`, etc) and optionally pass through requests to the
 * real $httpBackend for specific requests (e.g. to interact with certain remote apis or to fetch
 * templates from a webserver).
 *
 * As opposed to unit-testing, in an end-to-end testing scenario or in scenario when an application
 * is being developed with the real backend api replaced with a mock, it is often desirable for
 * certain category of requests to bypass the mock and issue a real http request (e.g. to fetch
 * templates or static files from the webserver). To configure the backend with this behavior
 * use the `passThrough` request handler of `when` instead of `respond`.
 *
 * Additionally, we don't want to manually have to flush mocked out requests like we do during unit
 * testing. For this reason the e2e $httpBackend flushes mocked out requests
 * automatically, closely simulating the behavior of the XMLHttpRequest object.
 *
 * To setup the application to run with this http backend, you have to create a module that depends
 * on the `ngMockE2E` and your application modules and defines the fake backend:
 *
 * ```js
 *   myAppDev = angular.module('myAppDev', ['myApp', 'ngMockE2E']);
 *   myAppDev.run(function($httpBackend) {
 *     phones = [{name: 'phone1'}, {name: 'phone2'}];
 *
 *     // returns the current list of phones
 *     $httpBackend.whenGET('/phones').respond(phones);
 *
 *     // adds a new phone to the phones array
 *     $httpBackend.whenPOST('/phones').respond(function(method, url, data) {
 *       var phone = angular.fromJson(data);
 *       phones.push(phone);
 *       return [200, phone, {}];
 *     });
 *     $httpBackend.whenGET(/^\/templates\//).passThrough();
 *     //...
 *   });
 * ```
 *
 * Afterwards, bootstrap your app with this new module.
 */

/**
 * @ngdoc method
 * @name $httpBackend#when
 * @module ngMockE2E
 * @description
 * Creates a new backend definition.
 *
 * @param {string} method HTTP method.
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
 *   object and returns true if the headers match the current definition.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 *
 *  - respond –
 *    `{function([status,] data[, headers, statusText])
 *    | function(function(method, url, data, headers)}`
 *    – The respond method takes a set of static data to be returned or a function that can return
 *    an array containing response status (number), response data (string), response headers
 *    (Object), and the text for the status (string).
 *  - passThrough – `{function()}` – Any request matching a backend definition with
 *    `passThrough` handler will be passed through to the real backend (an XHR request will be made
 *    to the server.)
 *  - Both methods return the `requestHandler` object for possible overrides.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenGET
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for GET requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenHEAD
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for HEAD requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenDELETE
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for DELETE requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPOST
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for POST requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPUT
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PUT requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPATCH
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PATCH requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenJSONP
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for JSONP requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */
angular.mock.e2e = {};
angular.mock.e2e.$httpBackendDecorator =
  ['$rootScope', '$timeout', '$delegate', '$browser', createHttpBackendMock];


/**
 * @ngdoc type
 * @name $rootScope.Scope
 * @module ngMock
 * @description
 * {@link ng.$rootScope.Scope Scope} type decorated with helper methods useful for testing. These
 * methods are automatically available on any {@link ng.$rootScope.Scope Scope} instance when
 * `ngMock` module is loaded.
 *
 * In addition to all the regular `Scope` methods, the following helper methods are available:
 */
angular.mock.$RootScopeDecorator = ['$delegate', function($delegate) {

  var $rootScopePrototype = Object.getPrototypeOf($delegate);

  $rootScopePrototype.$countChildScopes = countChildScopes;
  $rootScopePrototype.$countWatchers = countWatchers;

  return $delegate;

  // ------------------------------------------------------------------------------------------ //

  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countChildScopes
   * @module ngMock
   * @description
   * Counts all the direct and indirect child scopes of the current scope.
   *
   * The current scope is excluded from the count. The count includes all isolate child scopes.
   *
   * @returns {number} Total number of child scopes.
   */
  function countChildScopes() {
    // jshint validthis: true
    var count = 0; // exclude the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += 1;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }


  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countWatchers
   * @module ngMock
   * @description
   * Counts all the watchers of direct and indirect child scopes of the current scope.
   *
   * The watchers of the current scope are included in the count and so are all the watchers of
   * isolate child scopes.
   *
   * @returns {number} Total number of watchers.
   */
  function countWatchers() {
    // jshint validthis: true
    var count = this.$$watchers ? this.$$watchers.length : 0; // include the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += currentScope.$$watchers ? currentScope.$$watchers.length : 0;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }
}];


if (window.jasmine || window.mocha) {

  var currentSpec = null,
      annotatedFunctions = [],
      isSpecRunning = function() {
        return !!currentSpec;
      };

  angular.mock.$$annotate = angular.injector.$$annotate;
  angular.injector.$$annotate = function(fn) {
    if (typeof fn === 'function' && !fn.$inject) {
      annotatedFunctions.push(fn);
    }
    return angular.mock.$$annotate.apply(this, arguments);
  };


  (window.beforeEach || window.setup)(function() {
    annotatedFunctions = [];
    currentSpec = this;
  });

  (window.afterEach || window.teardown)(function() {
    var injector = currentSpec.$injector;

    annotatedFunctions.forEach(function(fn) {
      delete fn.$inject;
    });

    angular.forEach(currentSpec.$modules, function(module) {
      if (module && module.$$hashKey) {
        module.$$hashKey = undefined;
      }
    });

    currentSpec.$injector = null;
    currentSpec.$modules = null;
    currentSpec = null;

    if (injector) {
      injector.get('$rootElement').off();
    }

    // clean up jquery's fragment cache
    angular.forEach(angular.element.fragments, function(val, key) {
      delete angular.element.fragments[key];
    });

    MockXhr.$$lastInstance = null;

    angular.forEach(angular.callbacks, function(val, key) {
      delete angular.callbacks[key];
    });
    angular.callbacks.counter = 0;
  });

  /**
   * @ngdoc function
   * @name angular.mock.module
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * This function registers a module configuration code. It collects the configuration information
   * which will be used when the injector is created by {@link angular.mock.inject inject}.
   *
   * See {@link angular.mock.inject inject} for usage example
   *
   * @param {...(string|Function|Object)} fns any number of modules which are represented as string
   *        aliases or as anonymous module initialization functions. The modules are used to
   *        configure the injector. The 'ng' and 'ngMock' modules are automatically loaded. If an
   *        object literal is passed they will be registered as values in the module, the key being
   *        the module name and the value being what is returned.
   */
  window.module = angular.mock.module = function() {
    var moduleFns = Array.prototype.slice.call(arguments, 0);
    return isSpecRunning() ? workFn() : workFn;
    /////////////////////
    function workFn() {
      if (currentSpec.$injector) {
        throw new Error('Injector already created, can not register a module!');
      } else {
        var modules = currentSpec.$modules || (currentSpec.$modules = []);
        angular.forEach(moduleFns, function(module) {
          if (angular.isObject(module) && !angular.isArray(module)) {
            modules.push(function($provide) {
              angular.forEach(module, function(value, key) {
                $provide.value(key, value);
              });
            });
          } else {
            modules.push(module);
          }
        });
      }
    }
  };

  /**
   * @ngdoc function
   * @name angular.mock.inject
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * The inject function wraps a function into an injectable function. The inject() creates new
   * instance of {@link auto.$injector $injector} per test, which is then used for
   * resolving references.
   *
   *
   * ## Resolving References (Underscore Wrapping)
   * Often, we would like to inject a reference once, in a `beforeEach()` block and reuse this
   * in multiple `it()` clauses. To be able to do this we must assign the reference to a variable
   * that is declared in the scope of the `describe()` block. Since we would, most likely, want
   * the variable to have the same name of the reference we have a problem, since the parameter
   * to the `inject()` function would hide the outer variable.
   *
   * To help with this, the injected parameters can, optionally, be enclosed with underscores.
   * These are ignored by the injector when the reference name is resolved.
   *
   * For example, the parameter `_myService_` would be resolved as the reference `myService`.
   * Since it is available in the function body as _myService_, we can then assign it to a variable
   * defined in an outer scope.
   *
   * ```
   * // Defined out reference variable outside
   * var myService;
   *
   * // Wrap the parameter in underscores
   * beforeEach( inject( function(_myService_){
   *   myService = _myService_;
   * }));
   *
   * // Use myService in a series of tests.
   * it('makes use of myService', function() {
   *   myService.doStuff();
   * });
   *
   * ```
   *
   * See also {@link angular.mock.module angular.mock.module}
   *
   * ## Example
   * Example of what a typical jasmine tests looks like with the inject method.
   * ```js
   *
   *   angular.module('myApplicationModule', [])
   *       .value('mode', 'app')
   *       .value('version', 'v1.0.1');
   *
   *
   *   describe('MyApp', function() {
   *
   *     // You need to load modules that you want to test,
   *     // it loads only the "ng" module by default.
   *     beforeEach(module('myApplicationModule'));
   *
   *
   *     // inject() is used to inject arguments of all given functions
   *     it('should provide a version', inject(function(mode, version) {
   *       expect(version).toEqual('v1.0.1');
   *       expect(mode).toEqual('app');
   *     }));
   *
   *
   *     // The inject and module method can also be used inside of the it or beforeEach
   *     it('should override a version and test the new version is injected', function() {
   *       // module() takes functions or strings (module aliases)
   *       module(function($provide) {
   *         $provide.value('version', 'overridden'); // override version here
   *       });
   *
   *       inject(function(version) {
   *         expect(version).toEqual('overridden');
   *       });
   *     });
   *   });
   *
   * ```
   *
   * @param {...Function} fns any number of functions which will be injected using the injector.
   */



  var ErrorAddingDeclarationLocationStack = function(e, errorForStack) {
    this.message = e.message;
    this.name = e.name;
    if (e.line) this.line = e.line;
    if (e.sourceId) this.sourceId = e.sourceId;
    if (e.stack && errorForStack)
      this.stack = e.stack + '\n' + errorForStack.stack;
    if (e.stackArray) this.stackArray = e.stackArray;
  };
  ErrorAddingDeclarationLocationStack.prototype.toString = Error.prototype.toString;

  window.inject = angular.mock.inject = function() {
    var blockFns = Array.prototype.slice.call(arguments, 0);
    var errorForStack = new Error('Declaration Location');
    return isSpecRunning() ? workFn.call(currentSpec) : workFn;
    /////////////////////
    function workFn() {
      var modules = currentSpec.$modules || [];
      var strictDi = !!currentSpec.$injectorStrict;
      modules.unshift('ngMock');
      modules.unshift('ng');
      var injector = currentSpec.$injector;
      if (!injector) {
        if (strictDi) {
          // If strictDi is enabled, annotate the providerInjector blocks
          angular.forEach(modules, function(moduleFn) {
            if (typeof moduleFn === "function") {
              angular.injector.$$annotate(moduleFn);
            }
          });
        }
        injector = currentSpec.$injector = angular.injector(modules, strictDi);
        currentSpec.$injectorStrict = strictDi;
      }
      for (var i = 0, ii = blockFns.length; i < ii; i++) {
        if (currentSpec.$injectorStrict) {
          // If the injector is strict / strictDi, and the spec wants to inject using automatic
          // annotation, then annotate the function here.
          injector.annotate(blockFns[i]);
        }
        try {
          /* jshint -W040 *//* Jasmine explicitly provides a `this` object when calling functions */
          injector.invoke(blockFns[i] || angular.noop, this);
          /* jshint +W040 */
        } catch (e) {
          if (e.stack && errorForStack) {
            throw new ErrorAddingDeclarationLocationStack(e, errorForStack);
          }
          throw e;
        } finally {
          errorForStack = null;
        }
      }
    }
  };


  angular.mock.inject.strictDi = function(value) {
    value = arguments.length ? !!value : true;
    return isSpecRunning() ? workFn() : workFn;

    function workFn() {
      if (value !== currentSpec.$injectorStrict) {
        if (currentSpec.$injector) {
          throw new Error('Injector already created, can not modify strict annotations');
        } else {
          currentSpec.$injectorStrict = value;
        }
      }
    }
  };
}


})(window, window.angular);

(function() {
  angular.module("app").constant("config", {
    title: "foo"
  });

}).call(this);

(function() {
  var slice = [].slice;

  beforeEach(module('app'));

  describe('buildrequest controller', function() {
    var $httpBackend, $rootScope, $scope, $stateParams, $timeout, createController, dataService, goneto, injected;
    dataService = $scope = $httpBackend = $rootScope = null;
    $timeout = createController = $stateParams = null;
    goneto = null;
    beforeEach(module(function($provide) {
      $provide.value("$state", {
        go: function() {
          var args;
          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
          return goneto = args;
        }
      });
      $provide.value("$stateParams", {
        buildrequest: 1
      });
      return null;
    }));
    injected = function($injector) {
      var $controller, $q;
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $timeout = $injector.get('$timeout');
      $stateParams = $injector.get('$stateParams');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      dataService = $injector.get('dataService');
      return createController = function() {
        return $controller('buildrequestController', {
          $scope: $scope
        });
      };
    };
    beforeEach(inject(injected));
    it('should query for buildrequest', function() {
      var controller;
      dataService.when('buildsets/1/properties', [
        {
          a: ['a', 'b']
        }
      ]);
      dataService.when('buildrequests/1', [
        {
          buildrequestid: 1,
          builderid: 1,
          buildsetid: 1
        }
      ]);
      dataService.when('builders/1', [
        {
          builderid: 1
        }
      ]);
      dataService.when('buildsets/1', [
        {
          buildsetid: 1
        }
      ]);
      controller = createController();
      $timeout.flush();
      expect(dataService.get).toHaveBeenCalledWith('buildrequests', 1, jasmine.any(Object));
      dataService.when('builds', {
        buildrequestid: 1
      }, [
        {
          buildid: 1,
          buildrequestid: 1
        }, {
          buildid: 2,
          buildrequestid: 1
        }
      ]);
      $scope.$apply(function() {
        return $scope.buildrequest.claimed = true;
      });
      $timeout.flush();
      return expect($scope.builds[0]).toBeDefined();
    });
    it('should query for builds again if first query returns 0', function() {
      var controller;
      dataService.when('buildsets/1/properties', [
        {
          a: ['a', 'b']
        }
      ]);
      dataService.when('buildrequests/1', [
        {
          buildrequestid: 1,
          builderid: 1,
          buildsetid: 1
        }
      ]);
      dataService.when('builders/1', [
        {
          builderid: 1
        }
      ]);
      dataService.when('buildsets/1', [
        {
          buildsetid: 1
        }
      ]);
      controller = createController();
      dataService.when('builds', {
        buildrequestid: 1
      }, []);
      $timeout.flush();
      $scope.$apply(function() {
        return $scope.buildrequest.claimed = true;
      });
      $timeout.flush();
      expect($scope.builds.length).toBe(0);
      $scope.builds.from([
        {
          buildid: 1,
          buildrequestid: 1
        }, {
          buildid: 2,
          buildrequestid: 1
        }
      ]);
      $timeout.flush();
      return expect($scope.builds.length).toBe(2);
    });
    return it('should go to build page if build started', function() {
      var controller;
      dataService.when('buildsets/1/properties', [
        {
          a: ['a', 'b']
        }
      ]);
      dataService.when('buildrequests/1', [
        {
          buildrequestid: 1,
          builderid: 3,
          buildsetid: 1
        }
      ]);
      dataService.when('builders/3', [
        {
          builderid: 3
        }
      ]);
      dataService.when('buildsets/1', [
        {
          buildsetid: 1
        }
      ]);
      $stateParams.redirect_to_build = 1;
      controller = createController();
      $timeout.flush();
      dataService.when('builds', {
        buildrequestid: 1
      }, [
        {
          buildid: 1,
          builderid: 3,
          number: 1,
          buildrequestid: 1
        }
      ]);
      $scope.$apply(function() {
        return $scope.buildrequest.claimed = true;
      });
      $timeout.flush();
      return expect(goneto).toEqual([
        'build', {
          builder: 3,
          build: 1
        }
      ]);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildrequest controller', function() {
    var $httpBackend, $rootScope, $scope, $stateParams, $timeout, createController, dataService, injected, modal;
    dataService = $scope = $rootScope = null;
    createController = $stateParams = modal = $httpBackend = $timeout = null;
    injected = function($injector) {
      var $controller, $q;
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $timeout = $injector.get('$timeout');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      dataService = $injector.get('dataService');
      $httpBackend = $injector.get('$httpBackend');
      modal = {};
      return createController = function() {
        return $controller('forceDialogController', {
          $scope: $scope,
          builderid: 1,
          schedulerid: 'forcesched',
          modal: modal
        });
      };
    };
    beforeEach(inject(injected));
    it('should query for forcecheduler', function() {
      var controller;
      dataService.when('forceschedulers/forcesched', [
        {
          all_fields: [
            {
              'foo': 'int'
            }
          ]
        }
      ]);
      controller = createController();
      return $rootScope.$apply();
    });
    return it('should call forcecheduler control api when ok', function() {
      var controller;
      dataService.when('forceschedulers/forcesched', [
        {
          name: "forcesched",
          all_fields: [
            {
              'foo': 'int'
            }
          ]
        }
      ]);
      controller = createController();
      $timeout.flush();
      $httpBackend.when('POST', 'api/v2/forceschedulers/forcesched').respond("{}");
      $scope.ok();
      return $rootScope.$apply();
    });
  });

}).call(this);

(function() {
  describe('page with sidebar', function() {
    var assertDOM, elements, elmBody, padding, printDOM, queries, rootScope, scope, scrollTo, timeout;
    beforeEach(module("app"));
    elmBody = scope = rootScope = queries = timeout = null;
    padding = function(pix) {
      return {
        type: "padding",
        height: pix
      };
    };
    elements = function(start, end) {
      return {
        type: "elements",
        start: start,
        end: end
      };
    };
    assertDOM = function(l) {
      var c, childs, i, item, j, len, results;
      childs = [];
      $("div", elmBody).each(function(i, c) {
        return childs.push(c);
      });
      results = [];
      for (j = 0, len = l.length; j < len; j++) {
        item = l[j];
        if (item.type === "padding") {
          c = childs.shift();
          expect($(c).hasClass("padding")).toBe(true, c.outerHTML);
          expect($(c).height()).toEqual(item.height, c.outerHTML);
        }
        if (item.type === "elements") {
          results.push((function() {
            var k, ref, ref1, results1;
            results1 = [];
            for (i = k = ref = item.start, ref1 = item.end; ref <= ref1 ? k <= ref1 : k >= ref1; i = ref <= ref1 ? ++k : --k) {
              c = childs.shift();
              expect($(c).hasClass("padding")).toBe(false, c.outerHTML);
              results1.push(expect(c.innerText).toEqual(i.toString() + "a" + i.toString(), c.outerHTML));
            }
            return results1;
          })());
        } else {
          results.push(void 0);
        }
      }
      return results;
    };
    printDOM = function() {
      return $("div", elmBody).each(function() {
        if ($(this).hasClass("padding")) {
          return console.log("padding", $(this).height());
        } else {
          return console.log("row", this.innerText, $(this).height());
        }
      });
    };
    scrollTo = function(pos, verifyPos) {
      if (verifyPos == null) {
        verifyPos = pos;
      }
      elmBody.scrollTop(pos);
      expect(elmBody.scrollTop()).toBe(verifyPos);
      elmBody.trigger("scroll");
      timeout.flush();
      return expect(elmBody.scrollTop()).toBe(verifyPos);
    };
    beforeEach(inject(function($rootScope, $compile, glMenuService, $timeout, $q, $document) {
      timeout = $timeout;
      queries = [];
      rootScope = $rootScope;
      elmBody = angular.element('<div scroll-viewport style="height:50px">' + '<div style="height:10px" total-size="1000" scroll="item in items">{{::$index}}a{{::item.v}}' + '</div></div>');
      scope = $rootScope.$new();
      scope.items = {
        get: function(index, num) {
          var d;
          queries.push([index, num]);
          d = $q.defer();
          $timeout(function() {
            var i, j, ref, ret;
            ret = [];
            for (i = j = 0, ref = num - 1; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
              ret.push({
                v: index + i
              });
            }
            return d.resolve(ret);
          });
          return d.promise;
        }
      };
      $compile(elmBody)(scope)[0];
      scope.$digest();
      return elmBody.appendTo("body");
    }));
    it('should initially load 2 screens', inject(function($timeout) {
      $timeout.flush();
      expect(queries).toEqual([[0, 10]]);
      assertDOM([elements(0, 9), padding(9900)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    it('if scroll to middle, should load 3 screens', inject(function($timeout) {
      $timeout.flush();
      scrollTo(600);
      expect(queries).toEqual([[0, 10], [55, 15]]);
      assertDOM([elements(0, 9), padding(450), elements(55, 69), padding(10000 - 700)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    it('several scroll loads several screens, and paddings are cleaned out', inject(function($timeout) {
      $timeout.flush();
      scrollTo(600);
      expect(queries).toEqual([[0, 10], [55, 15]]);
      assertDOM([elements(0, 9), padding(450), elements(55, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(400);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15]]);
      assertDOM([elements(0, 9), padding(250), elements(35, 49), padding(50), elements(55, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(500);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5]]);
      assertDOM([elements(0, 9), padding(250), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(100);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10]]);
      assertDOM([elements(0, 19), padding(150), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(200);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10], [20, 10]]);
      assertDOM([elements(0, 29), padding(50), elements(35, 69), padding(10000 - 700)]);
      expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
      scrollTo(300);
      expect(queries).toEqual([[0, 10], [55, 15], [35, 15], [50, 5], [10, 10], [20, 10], [30, 5]]);
      assertDOM([elements(0, 69), padding(10000 - 700)]);
      return expect(elmBody[0].scrollHeight).toEqual(1000 * 10);
    }));
    return it('Scroll to the end', inject(function($timeout) {
      $timeout.flush();
      scrollTo(10000, 9950);
      expect(queries).toEqual([[0, 10], [990, 10]]);
      return assertDOM([elements(0, 9), padding(9800), elements(990, 999)]);
    }));
  });

}).call(this);

(function() {
  var slice = [].slice;

  beforeEach(module('app'));

  describe('buildrequest summary controller', function() {
    var $q, $rootScope, $scope, $timeout, createController, dataService, goneto, injected;
    $scope = $rootScope = $q = $timeout = null;
    goneto = createController = null;
    dataService = null;
    beforeEach(module(function($provide) {
      $provide.value("$state", {
        go: function() {
          var args;
          args = 1 <= arguments.length ? slice.call(arguments, 0) : [];
          return goneto = args;
        }
      });
      return null;
    }));
    injected = function($injector) {
      var $controller;
      $rootScope = $injector.get('$rootScope');
      $scope = $rootScope.$new();
      $scope.buildrequestid = 1;
      $timeout = $injector.get('$timeout');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      dataService = $injector.get('dataService');
      return createController = function() {
        return $controller('_buildrequestsummaryController', {
          $scope: $scope
        });
      };
    };
    beforeEach(inject(injected));
    it('should get the buildrequest', function() {
      var buildrequests, controller;
      buildrequests = [
        {
          buildrequestid: 1
        }
      ];
      dataService.expect('buildrequests/1', buildrequests);
      expect(dataService.get).not.toHaveBeenCalled();
      controller = createController();
      $timeout.flush();
      dataService.verifyNoOutstandingExpectation();
      return expect($scope.buildrequest.buildrequestid).toBe(1);
    });
    return it('should query for builds again if first query returns 0', function() {
      var buildrequests, builds, controller;
      buildrequests = [
        {
          buildrequestid: 1
        }
      ];
      dataService.expect('buildrequests/1', buildrequests);
      builds = [];
      controller = createController();
      $timeout.flush();
      dataService.verifyNoOutstandingExpectation();
      dataService.expect('builds', {
        buildrequestid: 1
      }, builds);
      $scope.$apply(function() {
        return $scope.buildrequest.claimed = true;
      });
      $timeout.flush();
      dataService.verifyNoOutstandingExpectation();
      expect($scope.builds.length).toBe(builds.length);
      builds = [
        {
          buildid: 1,
          buildrequestid: 1
        }, {
          buildid: 2,
          buildrequestid: 1
        }
      ];
      $scope.builds.from(builds);
      $timeout.flush();
      dataService.verifyNoOutstandingExpectation();
      return expect($scope.builds.length).toBe(builds.length);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildsticker controller', function() {
    var $compile, $timeout, dataService, injected, results, scope;
    dataService = scope = $compile = results = $timeout = null;
    injected = function($injector) {
      var $controller, $q, $rootScope;
      $compile = $injector.get('$compile');
      $rootScope = $injector.get('$rootScope');
      scope = $rootScope.$new();
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      $timeout = $injector.get('$timeout');
      results = $injector.get('RESULTS');
      return dataService = $injector.get('dataService');
    };
    beforeEach(inject(injected));
    return it('directive should generate correct html', function() {
      var build, buildLink, durationSpan, element, resultSpan, row0, row1, startedSpan, stateSpan, sticker;
      build = {
        buildid: 3,
        builderid: 2,
        number: 1
      };
      dataService.when('builds/3', [build]);
      dataService.when('builders/2', [
        {
          builderid: 2
        }
      ]);
      dataService.getBuilds(build.buildid).then(function(builds) {
        return scope.build = builds[0];
      });
      element = $compile("<buildsticker build='build'></buildsticker>")(scope);
      $timeout.flush();
      sticker = element.children().eq(0);
      row0 = sticker.children().eq(0);
      row1 = sticker.children().eq(1);
      resultSpan = row0.children().eq(0);
      buildLink = row0.children().eq(1);
      durationSpan = row1.children().eq(0);
      startedSpan = row1.children().eq(1);
      stateSpan = row1.children().eq(2);
      expect(buildLink.attr('href')).toBe('#/builders/2/builds/1');
      scope.build.complete = false;
      scope.build.started_at = Date.now();
      scope.build.results = -1;
      scope.build.state_string = 'pending';
      scope.$apply();
      expect(resultSpan.hasClass('results_PENDING')).toBe(true);
      expect(resultSpan.text()).toBe('...');
      expect(durationSpan.hasClass('ng-hide')).toBe(true);
      expect(startedSpan.hasClass('ng-hide')).toBe(false);
      expect(stateSpan.text()).toBe('pending');
      scope.build.complete = true;
      scope.build.complete_at = scope.build.started_at + 1;
      scope.build.results = results.SUCCESS;
      scope.build.state_string = 'finished';
      scope.$apply();
      expect(resultSpan.hasClass('results_SUCCESS')).toBe(true);
      expect(resultSpan.text()).toBe('SUCCESS');
      expect(durationSpan.hasClass('ng-hide')).toBe(false);
      expect(startedSpan.hasClass('ng-hide')).toBe(true);
      expect(durationSpan.text()).toBe('1 s');
      expect(stateSpan.text()).toBe('finished');
      scope.build.complete = true;
      scope.build.complete_at = scope.build.started_at + 1;
      scope.build.results = results.FAILURE;
      scope.build.state_string = 'failed';
      scope.$apply();
      expect(resultSpan.hasClass('results_FAILURE')).toBe(true);
      expect(resultSpan.text()).toBe('FAILURE');
      expect(durationSpan.hasClass('ng-hide')).toBe(false);
      expect(startedSpan.hasClass('ng-hide')).toBe(true);
      expect(durationSpan.text()).toBe('1 s');
      return expect(stateSpan.text()).toBe('failed');
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('buildsummary controller', function() {
    var $compile, $rootScope, $stateParams, $timeout, baseurl, createController, dataService, goneto, injected, results, scope;
    dataService = scope = $rootScope = $compile = null;
    $timeout = createController = $stateParams = results = baseurl = null;
    goneto = null;
    injected = function($injector) {
      var $controller, $location, $q;
      results = $injector.get('RESULTS');
      $rootScope = $injector.get('$rootScope');
      scope = $rootScope.$new();
      scope.buildid = 1;
      scope.condensed = 0;
      $timeout = $injector.get('$timeout');
      $stateParams = $injector.get('$stateParams');
      $controller = $injector.get('$controller');
      $q = $injector.get('$q');
      $compile = $injector.get('$compile');
      $location = $injector.get('$location');
      baseurl = $location.absUrl().split("#")[0];
      dataService = $injector.get('dataService');
      dataService.when('builds/1', [
        {
          buildid: 1,
          builderid: 1
        }
      ]);
      dataService.when('builders/1', [
        {
          builderid: 1
        }
      ]);
      dataService.when('builds/1/steps', [
        {
          builderid: 1,
          stepid: 1,
          number: 1
        }
      ]);
      return dataService.when('steps/1/logs', [
        {
          stepid: 1,
          logid: 1
        }, {
          stepid: 1,
          logid: 2
        }
      ]);
    };
    beforeEach(inject(injected));
    it('should provide correct isStepDisplayed when condensed', function() {
      var buildsummary, element;
      scope.condensed = true;
      element = $compile("<buildsummary buildid='buildid' condensed='condensed'></buildsummary>")(scope);
      scope.$apply();
      buildsummary = element.isolateScope().buildsummary;
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
      buildsummary.toggleDetails();
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      buildsummary.toggleDetails();
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      buildsummary.toggleDetails();
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      return expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
    });
    it('should provide correct isStepDisplayed when not condensed', function() {
      var buildsummary, element;
      scope.condensed = 0;
      element = $compile("<buildsummary buildid='buildid' condensed='condensed'></buildsummary>")(scope);
      scope.$apply();
      buildsummary = element.isolateScope().buildsummary;
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      buildsummary.toggleDetails();
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(false);
      buildsummary.toggleDetails();
      expect(buildsummary.isStepDisplayed({
        results: results.SUCCESS
      })).toBe(false);
      expect(buildsummary.isStepDisplayed({
        results: results.WARNING
      })).toBe(true);
      expect(buildsummary.isStepDisplayed({
        results: results.FAILURE
      })).toBe(true);
      return buildsummary.toggleDetails();
    });
    it('should provide correct getBuildRequestIDFromURL', function() {
      var buildsummary, element;
      element = $compile("<buildsummary buildid='buildid'></buildsummary>")(scope);
      scope.$apply();
      buildsummary = element.isolateScope().buildsummary;
      return expect(buildsummary.getBuildRequestIDFromURL(baseurl + "#buildrequests/123")).toBe(123);
    });
    it('should provide correct isBuildRequestURL', function() {
      var buildsummary, element;
      element = $compile("<buildsummary buildid='buildid'></buildsummary>")(scope);
      scope.$apply();
      buildsummary = element.isolateScope().buildsummary;
      expect(buildsummary.isBuildRequestURL(baseurl + "#buildrequests/123")).toBe(true);
      expect(buildsummary.isBuildRequestURL("http://otherdomain:5000/#buildrequests/123")).toBe(false);
      expect(buildsummary.isBuildRequestURL(baseurl + "#builds/123")).toBe(false);
      return expect(buildsummary.isBuildRequestURL(baseurl + "#buildrequests/bla")).toBe(false);
    });
    return it('should provide correct isBuildURL', function() {
      var buildsummary, element;
      element = $compile("<buildsummary buildid='buildid'></buildsummary>")(scope);
      scope.$apply();
      buildsummary = element.isolateScope().buildsummary;
      expect(buildsummary.isBuildURL(baseurl + "#builders/123/builds/123")).toBe(true);
      return expect(buildsummary.isBuildURL(baseurl + "#builders/sdf/builds/123")).toBe(false);
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('recent storage service', function() {
    var $q, $rootScope, $window, injected, recentStorage;
    recentStorage = $q = $window = $rootScope = null;
    injected = function($injector) {
      $q = $injector.get('$q');
      $window = $injector.get('$window');
      $rootScope = $injector.get('$rootScope');
      return recentStorage = $injector.get('recentStorage');
    };
    beforeEach(inject(injected));
    it('should store recent builds', function(done) {
      var testBuild1, testBuild2, testBuild3;
      testBuild1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuild2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuild3 = {
        link: '/test3',
        caption: 'test3'
      };
      recentStorage.clearAll().then(function(e) {
        return $q.all([recentStorage.addBuild(testBuild1), recentStorage.addBuild(testBuild3)]).then(function() {
          return recentStorage.getBuilds().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).not.toBeNull();
            expect(resolved).toContain(testBuild1);
            expect(resolved).toContain(testBuild3);
            expect(resolved).not.toContain(testBuild2);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
    it('should store recent builders', function(done) {
      var testBuilder1, testBuilder2, testBuilder3;
      testBuilder1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuilder2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuilder3 = {
        link: '/test3',
        caption: 'test3'
      };
      recentStorage.clearAll().then(function(e) {
        return $q.all([recentStorage.addBuilder(testBuilder1), recentStorage.addBuilder(testBuilder3)]).then(function() {
          return recentStorage.getBuilders().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).not.toBeNull();
            expect(resolved).toContain(testBuilder1);
            expect(resolved).toContain(testBuilder3);
            expect(resolved).not.toContain(testBuilder2);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
    return it('should clear all recent builds and builders', function(done) {
      var testBuild1, testBuild2, testBuilder1, testBuilder2;
      testBuild1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuild2 = {
        link: '/test2',
        caption: 'test2'
      };
      testBuilder1 = {
        link: '/test1',
        caption: 'test1'
      };
      testBuilder2 = {
        link: '/test2',
        caption: 'test2'
      };
      $q.all([recentStorage.addBuild(testBuild1), recentStorage.addBuild(testBuild2), recentStorage.addBuilder(testBuilder1), recentStorage.addBuilder(testBuilder2)]).then(function() {
        return recentStorage.clearAll().then(function(e) {
          return recentStorage.getAll().then(function(e) {
            var resolved;
            resolved = e;
            expect(resolved).toBeDefined();
            expect(resolved.recent_builds.length).toBe(0);
            expect(resolved.recent_builders.length).toBe(0);
            return done();
          });
        });
      }, function() {
        expect($window.indexedDB).toBeUndefined();
        return done();
      });
      return $rootScope.$digest();
    });
  });

}).call(this);

(function() {
  beforeEach(module('app'));

  describe('results service', function() {
    var injected, resultsService;
    resultsService = null;
    injected = function($injector) {
      return resultsService = $injector.get('resultsService');
    };
    beforeEach(inject(injected));
    it('should provide correct results2class', function() {
      var results, results2class;
      results = resultsService.results;
      results2class = function(r) {
        return resultsService.results2class({
          results: r
        });
      };
      expect(results2class(results.SUCCESS)).toBe("results_SUCCESS");
      expect(results2class(results.RETRY)).toBe("results_RETRY");
      expect(results2class(1234)).toBe("results_UNKNOWN");
      expect(resultsService.results2class(void 0)).toBe("results_UNKNOWN");
      expect(resultsService.results2class({
        results: void 0
      })).toBe("results_UNKNOWN");
      expect(resultsService.results2class({
        results: void 0,
        complete: false,
        started_at: void 0
      })).toBe("results_UNKNOWN");
      return expect(resultsService.results2class({
        results: void 0,
        complete: false,
        started_at: 10
      }, "pulse")).toBe("results_PENDING pulse");
    });
    return it('should provide correct results2Text', function() {
      var results, results2text;
      results = resultsService.results;
      results2text = function(r) {
        return resultsService.results2text({
          results: r
        });
      };
      expect(results2text(results.SUCCESS)).toBe("SUCCESS");
      expect(results2text(results.RETRY)).toBe("RETRY");
      expect(results2text(1234)).toBe("...");
      expect(resultsService.results2text(void 0)).toBe("...");
      expect(resultsService.results2text({
        results: void 0
      })).toBe("...");
      expect(resultsService.results2text({
        results: void 0,
        complete: false,
        started_at: void 0
      })).toBe("...");
      return expect(resultsService.results2text({
        results: void 0,
        complete: false,
        started_at: 10
      })).toBe("...");
    });
  });

}).call(this);

(function() {
  describe('settingsService', function() {
    var bbSettingsServiceProviderRef;
    bbSettingsServiceProviderRef = "";
    beforeEach(module('common', function(bbSettingsServiceProvider) {
      bbSettingsServiceProviderRef = bbSettingsServiceProvider;
      localStorage.clear();
      bbSettingsServiceProvider.addSettingsGroup({
        name: 'User',
        caption: 'User related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox1',
            default_value: false
          }, {
            type: 'choices',
            name: 'radio',
            default_value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
      bbSettingsServiceProvider.addSettingsGroup({
        name: 'Release',
        caption: 'Release related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_release',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release2',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release3',
            default_value: false
          }, {
            type: 'choices',
            name: name,
            default_value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
      return null;
    }));
    it('should merge groups when old group has values already set', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }
        ]
      };
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should merge groups when new group is defined with no items', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: true,
            default_value: false
          }
        ]
      };
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: []
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: []
      });
    }));
    it('should merge groups when old group is defined with no items', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: []
      };
      new_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should merge groups when new group is undefined', inject(function(bbSettingsService) {
      var group_result, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, void 0);
      return expect(group_result).toBeUndefined();
    }));
    it('should merge groups when old group is undefined', inject(function(bbSettingsService) {
      var group_result, new_group;
      localStorage.clear();
      new_group = {
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(void 0, new_group);
      return expect(group_result).toEqual({
        name: 'Auth',
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            value: false,
            default_value: false
          }
        ]
      });
    }));
    it('should not add a group without name', inject(function(bbSettingsService) {
      var exceptionRun, group;
      localStorage.clear();
      group = {
        caption: 'Auth related settings',
        items: [
          {
            type: 'bool',
            name: 'radio1',
            default_value: false
          }, {
            type: 'bool',
            name: 'radio2',
            default_value: false
          }
        ]
      };
      exceptionRun = function() {
        var group_result;
        return group_result = bbSettingsServiceProviderRef.addSettingsGroup(group);
      };
      return expect(exceptionRun).toThrow();
    }));
    it('should merge groups when new group has item with no default value', inject(function(bbSettingsService) {
      var group_result, new_group, old_group;
      localStorage.clear();
      old_group = {
        name: 'System',
        caption: 'System related settings',
        items: []
      };
      new_group = {
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2'
          }
        ]
      };
      group_result = bbSettingsServiceProviderRef._mergeNewGroup(old_group, new_group);
      return expect(group_result).toEqual({
        name: 'System',
        caption: 'System related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_system',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_system2',
            value: void 0
          }
        ]
      });
    }));
    it('should generate correct settings', inject(function(bbSettingsService) {
      var groups;
      groups = bbSettingsService.getSettingsGroups();
      return expect(groups['Release']).toEqual({
        name: 'Release',
        caption: 'Release related settings',
        items: [
          {
            type: 'bool',
            name: 'checkbox_release',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release2',
            value: false,
            default_value: false
          }, {
            type: 'bool',
            name: 'checkbox_release3',
            value: false,
            default_value: false
          }, {
            type: 'choices',
            name: name,
            default_value: 'radio1',
            value: 'radio1',
            answers: [
              {
                name: 'radio1'
              }, {
                name: 'radio2'
              }
            ]
          }
        ]
      });
    }));
    it('should return correct setting', inject(function(bbSettingsService) {
      var userSetting1, userSetting2, userSetting3;
      userSetting1 = bbSettingsService.getSetting('User.checkbox1');
      userSetting2 = bbSettingsService.getSetting('User.whatever');
      userSetting3 = bbSettingsService.getSetting('UserAA.User_checkbox1');
      expect(userSetting1).toBeDefined();
      expect(userSetting2).toBeUndefined();
      return expect(userSetting3).toBeUndefined();
    }));
    return it('should save correct settings', inject(function(bbSettingsService) {
      var checkbox, storageCheckbox, storageGroups;
      checkbox = bbSettingsService.getSetting('User.checkbox1');
      expect(checkbox.value).toBe(false);
      checkbox.value = true;
      bbSettingsService.save();
      storageGroups = angular.fromJson(localStorage.getItem('settings'));
      storageCheckbox = storageGroups['User'].items[0].value;
      return expect(storageCheckbox).toBeTruthy();
    }));
  });

}).call(this);
