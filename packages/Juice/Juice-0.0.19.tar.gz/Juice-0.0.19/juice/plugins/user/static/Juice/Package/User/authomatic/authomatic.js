// Generated by CoffeeScript 1.6.2
/*
# CoffeeDoc example documentation #

This is a module-level docstring, and will be displayed at the top of the module documentation.
Documentation generated by [CoffeeDoc](http://github.com/omarkhan/coffeedoc)

npm install -g coffeedoc
*/


(function() {
    var $, Authomatic, BaseProvider, Flickr, Foursquare, Google, LinkedIn, Oauth1Provider, Oauth2Provider, WindowsLive, deserializeCredentials, format, getProviderClass, globalOptions, jsonPCallbackCounter, log, openWindow, parseQueryString, parseUrl, _ref, _ref1, _ref2, _ref3, _ref4, _ref5,
        __slice = [].slice,
        __bind = function(fn, me) {
            return function() {
                return fn.apply(me, arguments);
            };
        },
        __hasProp = {}.hasOwnProperty,
        __extends = function(child, parent) {
            for (var key in parent) {
                if (__hasProp.call(parent, key)) child[key] = parent[key];
            }

            function ctor() {
                this.constructor = child;
            }
            ctor.prototype = parent.prototype;
            child.prototype = new ctor();
            child.__super__ = parent.prototype;
            return child;
        };

    $ = jQuery;

    jsonPCallbackCounter = 0;

    globalOptions = {
        logging: true,
        popupWidth: 800,
        popupHeight: 600,
        popupLinkSelector: 'a.authomatic',
        popupFormSelector: 'form.authomatic',
        popupFormValidator: function($form) {
            return true;
        },
        backend: null,
        forceBackend: false,
        substitute: {},
        params: {},
        headers: {},
        body: '',
        jsonpCallbackPrefix: 'authomaticJsonpCallback',
        onPopupInvalid: null,
        onPopupOpen: null,
        onLoginComplete: null,
        onBackendStart: null,
        onBackendComplete: null,
        onAccessSuccess: null,
        onAccessComplete: null
    };

    log = function() {
        var args, _ref;

        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        if (globalOptions.logging && ((typeof console !== "undefined" && console !== null ? (_ref = console.log) != null ? _ref.apply : void 0 : void 0) != null)) {
            return typeof console !== "undefined" && console !== null ? console.log.apply(console, ['Authomatic:'].concat(__slice.call(args))) : void 0;
        }
    };

    openWindow = function(url) {
        var height, left, settings, top, width;

        width = globalOptions.popupWidth;
        height = globalOptions.popupHeight;
        top = (screen.height / 2) - (height / 2);
        left = (screen.width / 2) - (width / 2);
        settings = "width=" + width + ",height=" + height + ",top=" + top + ",left=" + left;
        log('Opening popup:', url);
        if (typeof globalOptions.onPopupOpen === "function") {
            globalOptions.onPopupOpen(url);
        }
        return window.open(url, '', settings);
    };

    parseQueryString = function(queryString) {
        var item, k, result, v, _i, _len, _ref, _ref1;

        result = {};
        _ref = queryString.split('&');
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            item = _ref[_i];
            _ref1 = item.split('='), k = _ref1[0], v = _ref1[1];
            v = decodeURIComponent(v);
            if (result.hasOwnProperty(k)) {
                if (Array.isArray(result[k])) {
                    result[k].push(v);
                } else {
                    result[k] = [result[k], v];
                }
            } else {
                result[k] = v;
            }
        }
        return result;
    };

    parseUrl = function(url) {
        var qs, questionmarkIndex, u;

        log('parseUrl', url);
        questionmarkIndex = url.indexOf('?');
        if (questionmarkIndex >= 0) {
            u = url.substring(0, questionmarkIndex);
            qs = url.substring(questionmarkIndex + 1);
        } else {
            u = url;
        }
        return {
            url: u,
            query: qs,
            params: qs ? parseQueryString(qs) : void 0
        };
    };

    deserializeCredentials = function(credentials) {
        var sc, subtype, type, typeId, _ref;

        sc = decodeURIComponent(credentials).split('\n');
        typeId = sc[1];
        _ref = typeId.split('-'), type = _ref[0], subtype = _ref[1];
        return {
            id: parseInt(sc[0]),
            typeId: typeId,
            type: parseInt(type),
            subtype: parseInt(subtype),
            rest: sc.slice(2)
        };
    };

    getProviderClass = function(credentials) {
        var subtype, type, _ref;

        _ref = deserializeCredentials(credentials), type = _ref.type, subtype = _ref.subtype;
        if (type === 1) {
            if (subtype === 2) {
                return Flickr;
            } else {
                return Oauth1Provider;
            }
        } else if (type === 2) {
            if (subtype === 6) {
                return Foursquare;
            } else if (subtype === 9) {
                return LinkedIn;
            } else if (subtype === 14) {
                return WindowsLive;
            } else if (subtype === 12 || subtype === 15) {
                return BaseProvider;
            } else {
                return Oauth2Provider;
            }
        } else {
            return BaseProvider;
        }
    };

    format = function(template, substitute) {
        return template.replace(/{([^}]*)}/g, function(match, tag) {
            var level, target, _i, _len, _ref;

            target = substitute;
            _ref = tag.split('.');
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                level = _ref[_i];
                target = target[level];
            }
            return target;
        });
    };

    window.authomatic = new(Authomatic = (function() {
        function Authomatic() {}

        Authomatic.prototype.setup = function(options) {
            $.extend(globalOptions, options);
            return log('Setting up authomatic to:', globalOptions);
        };

        Authomatic.prototype.popupInit = function() {
            $(globalOptions.popupLinkSelector).click(function(e) {
                e.preventDefault();
                return openWindow($(this).attr('href'));
            });
            return $(globalOptions.popupFormSelector).submit(function(e) {
                var $form, url;

                e.preventDefault();
                $form = $(this);
                url = $form.attr('action') + '?' + $form.serialize();
                if (globalOptions.popupFormValidator($form)) {
                    return openWindow(url);
                } else {
                    return typeof globalOptions.onPopupInvalid === "function" ? globalOptions.onPopupInvalid($form) : void 0;
                }
            });
        };

        Authomatic.prototype.loginComplete = function(result, closer) {
            var result_copy;

            result_copy = $.extend(true, {}, result);
            log('Login procedure complete', result_copy);
            closer();
            return globalOptions.onLoginComplete(result_copy);
        };

        Authomatic.prototype.access = function(credentials, url, options) {
            var Provider, localEvents, provider, updatedOptions;

            if (options == null) {
                options = {};
            }
            localEvents = {
                onBackendStart: null,
                onBackendComplete: null,
                onAccessSuccess: null,
                onAccessComplete: null
            };
            updatedOptions = {};
            $.extend(updatedOptions, globalOptions, localEvents, options);
            url = format(url, updatedOptions.substitute);
            log('access options', updatedOptions, globalOptions);
            if (updatedOptions.forceBackend) {
                Provider = BaseProvider;
            } else {
                Provider = getProviderClass(credentials);
            }
            provider = new Provider(options.backend, credentials, url, updatedOptions);
            log('Instantiating provider:', provider);
            return provider.access();
        };

        return Authomatic;

    })());

    BaseProvider = (function() {
        BaseProvider.prototype._x_jsonpCallbackParamName = 'callback';

        function BaseProvider(backend, credentials, url, options) {
            var parsedUrl;

            this.backend = backend;
            this.credentials = credentials;
            this.options = options;
            this.access = __bind(this.access, this);
            this.contactProvider = __bind(this.contactProvider, this);
            this.contactBackend = __bind(this.contactBackend, this);
            this.backendRequestType = 'auto';
            this.jsonpRequest = false;
            this.jsonpCallbackName = "" + globalOptions.jsonpCallbackPrefix + jsonPCallbackCounter;
            this.deserializedCredentials = deserializeCredentials(this.credentials);
            this.providerID = this.deserializedCredentials.id;
            this.providerType = this.deserializedCredentials.type;
            this.credentialsRest = this.deserializedCredentials.rest;
            parsedUrl = parseUrl(url);
            this.url = parsedUrl.url;
            this.params = {};
            $.extend(this.params, parsedUrl.params, this.options.params);
        }

        BaseProvider.prototype.contactBackend = function(callback) {
            var data, _base;

            if (this.jsonpRequest && this.options.method === !'GET') {
                this.backendRequestType = 'fetch';
            }
            data = {
                type: this.backendRequestType,
                credentials: this.credentials,
                url: this.url,
                method: this.options.method,
                body: this.options.body,
                params: JSON.stringify(this.params),
                headers: JSON.stringify(this.options.headers)
            };
            if (typeof globalOptions.onBackendStart === "function") {
                globalOptions.onBackendStart(data);
            }
            if (typeof(_base = this.options).onBackendStart === "function") {
                _base.onBackendStart(data);
            }
            log("Contacting backend at " + this.options.backend + ".", data);
            return $.get(this.options.backend, data, callback);
        };

        BaseProvider.prototype.contactProvider = function(requestElements) {
            var body, headers, jsonpOptions, method, options, params, url,
                _this = this;

            url = requestElements.url, method = requestElements.method, params = requestElements.params, headers = requestElements.headers, body = requestElements.body;
            options = {
                type: method,
                data: params,
                headers: headers,
                complete: [
                    (function(jqXHR, textStatus) {
                        return log('Request complete.', textStatus, jqXHR);
                    }), globalOptions.onAccessComplete, this.options.onAccessComplete
                ],
                success: [
                    (function(data) {
                        return log('Request successful.', data);
                    }), globalOptions.onAccessSuccess, this.options.onAccessSuccess
                ],
                error: function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.state() === 'rejected') {
                        if (_this.options.method === 'GET') {
                            log('Cross domain request failed! trying JSONP request.');
                            _this.jsonpRequest = true;
                        } else {
                            _this.backendRequestType = 'fetch';
                        }
                        return _this.access();
                    }
                }
            };
            if (this.jsonpRequest) {
                jsonpOptions = {
                    jsonpCallback: this.jsonpCallbackName,
                    jsonp: this._x_jsonpCallbackParamName,
                    cache: true,
                    dataType: 'jsonp',
                    error: function(jqXHR, textStatus, errorThrown) {
                        return log('JSONP failed! State:', jqXHR.state());
                    }
                };
                $.extend(options, jsonpOptions);
                log("Contacting provider with JSONP request.", url, options);
            } else {
                log("Contacting provider with cross domain request", url, options);
            }
            return $.ajax(url, options);
        };

        BaseProvider.prototype.access = function() {
            var callback,
                _this = this;

            callback = function(data, textStatus, jqXHR) {
                var responseTo, _base, _base1, _base2;

                if (typeof globalOptions.onBackendComplete === "function") {
                    globalOptions.onBackendComplete(data, textStatus, jqXHR);
                }
                if (typeof(_base = _this.options).onBackendComplete === "function") {
                    _base.onBackendComplete(data, textStatus, jqXHR);
                }
                responseTo = jqXHR != null ? jqXHR.getResponseHeader('Authomatic-Response-To') : void 0;
                if (responseTo === 'fetch') {
                    log("Fetch data returned from backend.", jqXHR.getResponseHeader('content-type'), data);
                    if (typeof globalOptions.onAccessSuccess === "function") {
                        globalOptions.onAccessSuccess(data);
                    }
                    if (typeof(_base1 = _this.options).onAccessSuccess === "function") {
                        _base1.onAccessSuccess(data);
                    }
                    if (typeof globalOptions.onAccessComplete === "function") {
                        globalOptions.onAccessComplete(jqXHR, textStatus);
                    }
                    return typeof(_base2 = _this.options).onAccessComplete === "function" ? _base2.onAccessComplete(jqXHR, textStatus) : void 0;
                } else if (responseTo === 'elements') {
                    log("Request elements data returned from backend.", data);
                    return _this.contactProvider(data);
                }
            };
            if (this.jsonpRequest) {
                jsonPCallbackCounter += 1;
            }
            return this.contactBackend(callback);
        };

        return BaseProvider;

    })();

    Oauth1Provider = (function(_super) {
        __extends(Oauth1Provider, _super);

        function Oauth1Provider() {
            this.contactProvider = __bind(this.contactProvider, this);
            this.access = __bind(this.access, this);
            _ref = Oauth1Provider.__super__.constructor.apply(this, arguments);
            return _ref;
        }

        Oauth1Provider.prototype.access = function() {
            this.jsonpRequest = true;
            this.params[this._x_jsonpCallbackParamName] = this.jsonpCallbackName;
            return Oauth1Provider.__super__.access.call(this);
        };

        Oauth1Provider.prototype.contactProvider = function(requestElements) {
            delete requestElements.params.callback;
            return Oauth1Provider.__super__.contactProvider.call(this, requestElements);
        };

        return Oauth1Provider;

    })(BaseProvider);

    Flickr = (function(_super) {
        __extends(Flickr, _super);

        function Flickr() {
            _ref1 = Flickr.__super__.constructor.apply(this, arguments);
            return _ref1;
        }

        Flickr.prototype._x_jsonpCallbackParamName = 'jsoncallback';

        return Flickr;

    })(Oauth1Provider);

    Oauth2Provider = (function(_super) {
        __extends(Oauth2Provider, _super);

        Oauth2Provider.prototype._x_accessToken = 'access_token';

        Oauth2Provider.prototype._x_bearer = 'Bearer';

        function Oauth2Provider() {
            var args, _ref2;

            args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
            this.access = __bind(this.access, this);
            this.handleTokenType = __bind(this.handleTokenType, this);
            Oauth2Provider.__super__.constructor.apply(this, args);
            _ref2 = this.credentialsRest, this.accessToken = _ref2[0], this.refreshToken = _ref2[1], this.expirationTime = _ref2[2], this.tokenType = _ref2[3];
            this.handleTokenType();
        }

        Oauth2Provider.prototype.handleTokenType = function() {
            if (this.tokenType === '1') {
                return this.options.headers['Authorization'] = "" + this._x_bearer + " " + this.accessToken;
            } else {
                return this.params[this._x_accessToken] = this.accessToken;
            }
        };

        Oauth2Provider.prototype.access = function() {
            var requestElements;

            if (this.backendRequestType === 'fetch') {
                return Oauth2Provider.__super__.access.call(this);
            } else {
                requestElements = {
                    url: this.url,
                    method: this.options.method,
                    params: this.params,
                    headers: this.options.headers,
                    body: this.options.body
                };
                return this.contactProvider(requestElements);
            }
        };

        return Oauth2Provider;

    })(BaseProvider);

    Foursquare = (function(_super) {
        __extends(Foursquare, _super);

        function Foursquare() {
            _ref2 = Foursquare.__super__.constructor.apply(this, arguments);
            return _ref2;
        }

        Foursquare.prototype._x_accessToken = 'oauth_token';

        return Foursquare;

    })(Oauth2Provider);

    Google = (function(_super) {
        __extends(Google, _super);

        function Google() {
            _ref3 = Google.__super__.constructor.apply(this, arguments);
            return _ref3;
        }

        Google.prototype._x_bearer = 'OAuth';

        return Google;

    })(Oauth2Provider);

    LinkedIn = (function(_super) {
        __extends(LinkedIn, _super);

        function LinkedIn() {
            _ref4 = LinkedIn.__super__.constructor.apply(this, arguments);
            return _ref4;
        }

        LinkedIn.prototype._x_accessToken = 'oauth2_access_token';

        return LinkedIn;

    })(Oauth2Provider);

    WindowsLive = (function(_super) {
        __extends(WindowsLive, _super);

        function WindowsLive() {
            this.handleTokenType = __bind(this.handleTokenType, this);
            _ref5 = WindowsLive.__super__.constructor.apply(this, arguments);
            return _ref5;
        }

        WindowsLive.prototype.handleTokenType = function() {
            if (this.tokenType === '1') {
                this.options.headers['Authorization'] = "" + this._x_bearer + " " + this.accessToken;
            }
            return this.params[this._x_accessToken] = this.accessToken;
        };

        return WindowsLive;

    })(Oauth2Provider);

}).call(this);


