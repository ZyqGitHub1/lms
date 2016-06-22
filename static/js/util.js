function Request(baseUrl, query) {
    this.baseUrl = baseUrl;
    this.query = null;

    if ( query ) {
        this.query = query;
    }
}

Object.defineProperty(Request.prototype, 'url', {
        get: function() {
            return Request.makeUrl(this.baseUrl, this.query);
        }
});

Request.makeUrl = function(baseUrl, query) {
    if ( !query ) {
        return baseUrl;
    }

    var queryString = Request.makeQueryString(parameters);
    if ( queryString.length == 0 ) {
        return baseUrl;
    }

    return baseUrl + '?' + queryString;
}

Request.extractBaseUrl = function(href) {
    var queryPos = href.indexOf('?');
    if ( queryPos == -1 ) {
        return href;
    }

    return href.slice(0, queryPos);
}

Request.makeQueryString = function(parameters) {
    parameterList = [];
    for ( var key in parameters ) {
        var value = parameters[key];
        
        parameterList.push(key + '=' + value);
    }

    return parameterList.join('&');
}

Request.parseQueryString = function(queryString) {
    queryString = queryString.substring(1);
    if ( queryString == null || queryString == '' ) {
        return {};
    }

    var parameterList = queryString.split('&');
    var parameters = {};
    for ( parameterIndex in parameterList ) {
        var parameter = parameterList[parameterIndex];

        var keyValue = parameter.split('=');
        var key = keyValue[0];
        var value = keyValue[1];

        parameters[key] = value;
    }

    return parameters;
}

function Response() {
}

Response.prototype.redirectTo = function(request) {
    location.href = request.url;
}

var Application = {
    data: Object.create(null),
    showPage: function(page) {
        var queryString = window.location.search;
        var baseUrl = Request.extractBaseUrl(location.href);
        var query = Request.parseQueryString(queryString);
        var request = new Request(baseUrl, query);
        var response = new Response();

        page.request = request;
        page.response = response;

        if ( 'onInitialize' in page ) {
            page.onInitialize();
        }

        $('.app-page').hide();
        page.$page.show();

        if ( 'onShow' in page ) {
            page.onShow();
        }
    }
};

function postJSON(url, data, callback, error) {
    $.ajax({ 
        url: url,
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(data) {
            callback(data);
        },
        error: function(req, message, e) {
            console.log(message);
            console.log(e);

            if ( error ) {
                error(req, message, e);
            }
        }
    });
}

function getJSON(url, callback, error) {
    $.ajax({ 
        url: url,
        type: 'get',
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        },
        error: function(req, message, e) {
            console.log(message);
            console.log(e);

            if ( error ) {
                error(req, message, e);
            }
        }
    });
}

function toJSON(object) {
    return JSON.stringify(object);
}

function fromJSON(data) {
    if ( !data ) {
        return undefined;
    }
    
    return JSON.parse(data);
}

function redirectTo(url) {
    window.location.href = url; 
}

function disableAll(e) {
    e.preventDefault();
    e.stopPropagation();
}

function Template(templateName, $container) {
    var templateClass = '.' + templateName + '.template';
    var instanceClass = '.' + templateName + '.instance';

    if ( $container ) {
        $container.find(instanceClass).remove();
        this.$template = $container.find(templateClass);
    }
}

Template.prototype.getInstance = function($template) {
    return this.$template.clone(true).removeClass('template').addClass('instance');
}

function formatDate(date) {
    return date.getFullYear() + '/' +
        (date.getMonth() + 1) + '/' +
        date.getDate() + ' ' +
        date.getHours() + ':' +
        date.getMinutes() + ':' +
        date.getSeconds();
}
