'use strict';   // See note about 'use strict'; below

var myApp = angular.module('myApp', [
 'ngRoute',
]);

myApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: '/static/frontend/partials/index.html',
             }).
             when('/about', {
                 templateUrl: '../static/frontend/partials/about.html',
             }).
             otherwise({
                 redirectTo: '/'
             });
    }]);