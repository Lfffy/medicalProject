/**
 * 浏览器兼容性Polyfill解决方案
 * 支持IE11+和现代浏览器
 */

// 1. Fetch API Polyfill (IE11)
if (!window.fetch) {
    console.log('Loading Fetch API polyfill...');
    // 使用XMLHttpRequest实现fetch
    window.fetch = function(url, options) {
        options = options || {};
        return new Promise(function(resolve, reject) {
            var request = new XMLHttpRequest();
            request.onload = function() {
                var response = {
                    ok: request.status >= 200 && request.status < 300,
                    status: request.status,
                    statusText: request.statusText,
                    url: request.responseURL,
                    json: function() {
                        return Promise.resolve(JSON.parse(request.responseText));
                    },
                    text: function() {
                        return Promise.resolve(request.responseText);
                    }
                };
                resolve(response);
            };
            request.onerror = function() {
                reject(new Error('Network request failed'));
            };
            request.open(options.method || 'GET', url, true);
            
            // 设置请求头
            if (options.headers) {
                for (var header in options.headers) {
                    request.setRequestHeader(header, options.headers[header]);
                }
            }
            
            request.send(options.body);
        });
    };
}

// 2. Promise Polyfill (IE11)
if (!window.Promise) {
    console.log('Loading Promise polyfill...');
    (function() {
        var Promise = function(executor) {
            this.state = 'pending';
            this.value = undefined;
            this.reason = undefined;
            this.onFulfilledCallbacks = [];
            this.onRejectedCallbacks = [];
            
            var self = this;
            
            function resolve(value) {
                if (self.state === 'pending') {
                    self.state = 'fulfilled';
                    self.value = value;
                    self.onFulfilledCallbacks.forEach(function(callback) {
                        callback(value);
                    });
                }
            }
            
            function reject(reason) {
                if (self.state === 'pending') {
                    self.state = 'rejected';
                    self.reason = reason;
                    self.onRejectedCallbacks.forEach(function(callback) {
                        callback(reason);
                    });
                }
            }
            
            try {
                executor(resolve, reject);
            } catch (e) {
                reject(e);
            }
        };
        
        Promise.prototype.then = function(onFulfilled, onRejected) {
            var self = this;
            return new Promise(function(resolve, reject) {
                function handle(callback) {
                    try {
                        var result = callback(self.state === 'fulfilled' ? self.value : self.reason);
                        resolve(result);
                    } catch (e) {
                        reject(e);
                    }
                }
                
                if (self.state === 'fulfilled') {
                    handle(onFulfilled);
                } else if (self.state === 'rejected') {
                    handle(onRejected);
                } else {
                    self.onFulfilledCallbacks.push(function() {
                        handle(onFulfilled);
                    });
                    self.onRejectedCallbacks.push(function() {
                        handle(onRejected);
                    });
                }
            });
        };
        
        Promise.prototype.catch = function(onRejected) {
            return this.then(null, onRejected);
        };
        
        window.Promise = Promise;
    })();
}

// 3. String.prototype.includes Polyfill (IE11)
if (!String.prototype.includes) {
    String.prototype.includes = function(search, start) {
        if (typeof start !== 'number') {
            start = 0;
        }
        if (start + search.length > this.length) {
            return false;
        } else {
            return this.indexOf(search, start) !== -1;
        }
    };
}

// 4. Array.prototype.includes Polyfill (IE11)
if (!Array.prototype.includes) {
    Array.prototype.includes = function(searchElement, fromIndex) {
        if (this == null) {
            throw new TypeError('"this" is null or not defined');
        }
        var O = Object(this);
        var len = O.length >>> 0;
        if (len === 0) {
            return false;
        }
        var n = fromIndex | 0;
        var k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);
        function sameValueZero(x, y) {
            return x === y || (typeof x === 'number' && typeof y === 'number' && isNaN(x) && isNaN(y));
        }
        while (k < len) {
            if (sameValueZero(O[k], searchElement)) {
                return true;
            }
            k++;
        }
        return false;
    };
}

// 5. Object.assign Polyfill (IE11)
if (typeof Object.assign !== 'function') {
    Object.assign = function(target, varArgs) {
        if (target == null) {
            throw new TypeError('Cannot convert undefined or null to object');
        }
        var to = Object(target);
        for (var index = 1; index < arguments.length; index++) {
            var nextSource = arguments[index];
            if (nextSource != null) {
                for (var nextKey in nextSource) {
                    if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
                        to[nextKey] = nextSource[nextKey];
                    }
                }
            }
        }
        return to;
    };
}

// 6. CustomEvent Polyfill (IE11)
if (typeof window.CustomEvent !== 'function') {
    function CustomEvent(event, params) {
        params = params || { bubbles: false, cancelable: false, detail: undefined };
        var evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
        return evt;
    }
    CustomEvent.prototype = window.Event.prototype;
    window.CustomEvent = CustomEvent;
}

// 7. requestAnimationFrame Polyfill (IE9+)
if (!window.requestAnimationFrame) {
    window.requestAnimationFrame = function(callback) {
        return window.setTimeout(function() {
            callback(Date.now());
        }, 1000 / 60);
    };
    
    window.cancelAnimationFrame = function(id) {
        clearTimeout(id);
    };
}

// 8. console Polyfill (IE8/9)
if (!window.console) {
    window.console = {};
    var methods = ["log", "debug", "info", "warn", "error", "assert", "dir", "clear", "profile", "profileEnd"];
    methods.forEach(function(method) {
        console[method] = function() {};
    });
}

// 9. classList Polyfill (IE9)
if (!('classList' in document.createElement('_'))) {
    (function(view) {
        if (!('Element' in view)) return;
        
        var classListProp = 'classList',
            protoProp = 'prototype',
            elemCtrProto = view.Element[protoProp],
            objCtr = Object,
            strTrim = String[protoProp].trim || function() {
                return this.replace(/^\s+|\s+$/g, '');
            },
            arrIndexOf = Array[protoProp].indexOf || function(item) {
                var i = 0,
                    len = this.length;
                for (; i < len; i++) {
                    if (i in this && this[i] === item) {
                        return i;
                    }
                }
                return -1;
            };
        
        var DOMTokenList = function(elem) {
            this._element = elem;
            this._classList = elem.className.split(/\s+/);
            for (var i = 0, len = this._classList.length; i < len; i++) {
                if (this._classList[i] === '') {
                    this._classList.splice(i, 1);
                    len--;
                    i--;
                }
            }
        };
        
        DOMTokenList[protoProp] = {
            add: function(token) {
                if (this.contains(token)) return;
                this._classList.push(token);
                this._element.className = this._classList.join(' ');
            },
            contains: function(token) {
                return arrIndexOf.call(this._classList, token) !== -1;
            },
            remove: function(token) {
                var index = arrIndexOf.call(this._classList, token);
                if (index === -1) return;
                this._classList.splice(index, 1);
                this._element.className = this._classList.join(' ');
            },
            toggle: function(token) {
                if (this.contains(token)) {
                    this.remove(token);
                } else {
                    this.add(token);
                }
            },
            toString: function() {
                return this._element.className;
            }
        };
        
        Object.defineProperty(elemCtrProto, classListProp, {
            get: function() {
                return new DOMTokenList(this);
            },
            enumerable: true,
            configurable: true
        });
    }(window));
}

// 10. 事件监听器兼容性处理
function addEventListenerCompat(element, event, handler, options) {
    if (element.addEventListener) {
        element.addEventListener(event, handler, options);
    } else if (element.attachEvent) {
        element.attachEvent('on' + event, handler);
    }
}

// 11. JSON Polyfill (IE7)
if (!window.JSON) {
    window.JSON = {
        parse: function(sJSON) {
            return eval('(' + sJSON + ')');
        },
        stringify: function(vContent) {
            if (vContent instanceof Object) {
                var sOutput = "";
                if (vContent.constructor === Array) {
                    for (var nId = 0; nId < vContent.length; sOutput += this.stringify(vContent[nId]) + ",", nId++);
                    return "[" + sOutput.substr(0, sOutput.length - 1) + "]";
                }
                for (var sProp in vContent) {
                    sOutput += '"' + sProp + '":' + this.stringify(vContent[sProp]) + ",";
                }
                return "{" + sOutput.substr(0, sOutput.length - 1) + "}";
            }
            return typeof vContent === "string" ? '"' + vContent.replace(/"/g, '\\"') + '"' : String(vContent);
        }
    };
}

// 12. 检测浏览器版本并加载相应的polyfill
function loadPolyfills() {
    var userAgent = navigator.userAgent;
    var isIE = userAgent.indexOf('MSIE') !== -1 || userAgent.indexOf('Trident/') !== -1;
    var isIE11 = userAgent.indexOf('Trident/7.0') !== -1;
    
    if (isIE) {
        console.log('检测到IE浏览器，正在加载兼容性polyfills...');
        
        // 加载CSS Grid polyfill
        if (!CSS.supports || !CSS.supports('display', 'grid')) {
            console.log('加载CSS Grid polyfill...');
            // 这里可以动态加载CSS Grid polyfill库
        }
        
        // 加载Flexbox polyfill
        if (!CSS.supports || !CSS.supports('display', 'flexbox')) {
            console.log('加载Flexbox polyfill...');
            // 这里可以动态加载Flexbox polyfill库
        }
    }
    
    // 检查是否支持现代JavaScript特性
    var needsModernPolyfills = false;
    
    try {
        // 测试箭头函数
        eval('() => {}');
    } catch (e) {
        needsModernPolyfills = true;
    }
    
    try {
        // 测试const/let
        eval('const test = 1');
    } catch (e) {
        needsModernPolyfills = true;
    }
    
    try {
        // 测试模板字符串
        eval('`test`');
    } catch (e) {
        needsModernPolyfills = true;
    }
    
    if (needsModernPolyfills) {
        console.log('检测到需要现代JavaScript特性polyfill...');
        // 这里可以加载Babel standalone等转换器
    }
}

// 页面加载完成后自动加载polyfills
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadPolyfills);
} else {
    loadPolyfills();
}

// 导出兼容性工具函数
window.CompatibilityUtils = {
    addEventListener: addEventListenerCompat,
    loadPolyfills: loadPolyfills
};