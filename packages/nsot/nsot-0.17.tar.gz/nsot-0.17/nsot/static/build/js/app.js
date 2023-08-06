(function() {
    "use strict";

    var templateCache = angular.module("nsotTemplates", []);
    var app = angular.module(
        "nsotApp",
        ["nsotTemplates", "ngRoute", "ngResource", "ngTagsInput", "chart.js"]
    );

    app.config(["$interpolateProvider", function($interpolateProvider){
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }])
    .config(["$logProvider", function($logProvider){
        $logProvider.debugEnabled(true);
    }])
    .config(["$locationProvider", function($locationProvider) {
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });
    }])
    .config(["$httpProvider", function($httpProvider) {
        _.assign($httpProvider.defaults, {
            "xsrfCookieName": "_xsrf",
            // Django expects a different CSRF header name than the default.
            // This will become configurable in Django 1.9.
            "xsrfHeaderName": "X-CSRFToken"
        });
    }])
    // Intercept HTTP calls to detect 401s and redirect to the login page.
    // Adapted from: https://gist.github.com/gnomeontherun/5678505
    .config(["$provide", "$httpProvider", function($provide, $httpProvider) {
      // Intercept http calls.
      $provide.factory('AuthInterceptor', ["$q", function ($q) {
        return {
          // On request success
          request: function (config) {
            // Contains the data about the request before it is sent.
            // console.log(config);

            // Return the config or wrap it in a promise if blank.
            return config || $q.when(config);
          },

          // On request failure
          requestError: function (rejection) {
            // Contains the data about the error on the request.
            // console.log(rejection);

            // Return the promise rejection.
            return $q.reject(rejection);
          },

          // On response success
          response: function (response) {
            // Contains the data from the response.
            // console.log(response);

            // Return the response or promise.
            return response || $q.when(response);
          },

          // On response failture
          responseError: function (rejection) {
            // Contains the data about the error.
            // console.log(rejection);
            if (rejection.status === 401) {
                console.log('Response error 401', rejection);
                window.location.replace('/api/auth/login/?next=/');
            }

            // Return the promise rejection.
            return $q.reject(rejection);
          }
        };
      }]);
      // Add the interceptor to the $httpProvider.
      $httpProvider.interceptors.push('AuthInterceptor');
    }])
    // Tell Angular not to strip trailing slashes from URLs.
    .config(["$resourceProvider", function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    // Configure Chart.js global settings
    .config(["ChartJsProvider", function(ChartJsProvider) {
        // Override default colors for Pie charts.
        ChartJsProvider.setOptions('Pie', {
            colours: [
                "#dff0d8", // bg-success (green)
                "#d9edf7", // bg-info (blue)
                "#fcf8e3", // bg-warning (yellow)
                "#f2dede"  // bg-danger (red)
            ]
        });
    }])
    // NSoT app routes.
    .config(["$routeProvider", function($routeProvider) {
        $routeProvider
        .when("/", {
            templateUrl: "index.html",
            controller: "IndexController"
        })
        .when("/users", {
            templateUrl: "users.html",
            controller: "UsersController"
        })
        .when("/users/:userId", {
            templateUrl: "user.html",
            controller: "UserController"
        })
        .when("/profile", {
            template: "",
            controller: "ProfileController"
        })
        .when("/sites", {
            templateUrl: "sites.html",
            controller: "SitesController"
        })
        .when("/sites/:siteId", {
            templateUrl: "site.html",
            controller: "SiteController"
        })
        .when("/sites/:siteId/networks", {
            templateUrl: "networks.html",
            controller: "NetworksController"
        })
        .when("/sites/:siteId/networks/:networkId", {
            templateUrl: "network.html",
            controller: "NetworkController"
        })
        .when("/sites/:siteId/interfaces", {
            templateUrl: "interfaces.html",
            controller: "InterfacesController"
        })
        .when("/sites/:siteId/interfaces/:ifaceId", {
            templateUrl: "interface.html",
            controller: "InterfaceController"
        })
        .when("/sites/:siteId/devices", {
            templateUrl: "devices.html",
            controller: "DevicesController"
        })
        .when("/sites/:siteId/devices/:deviceId", {
            templateUrl: "device.html",
            controller: "DeviceController"
        })
        .when("/sites/:siteId/attributes", {
            templateUrl: "attributes.html",
            controller: "AttributesController"
        })
        .when("/sites/:siteId/attributes/:attributeId", {
            templateUrl: "attribute.html",
            controller: "AttributeController"
        })
        .when("/sites/:siteId/changes", {
            templateUrl: "changes.html",
            controller: "ChangesController"
        })
        .when("/sites/:siteId/changes/:changeId", {
            templateUrl: "change.html",
            controller: "ChangeController"
        })
        .otherwise({redirectTo: "/"});
    }]);

    app.run(["$rootScope", function($rootScope){
        $rootScope.NSOT_VERSION = window.NSOT_VERSION;
    }]);


})();

(function() {
    "use strict";

    var app = angular.module("nsotApp");

    app.controller("navigationController", ["$scope", "$location", function($scope, $location) {

        $scope.siteId = null;
        $scope.$on('$routeChangeStart', function(next, current) {
            $scope.siteId = current.params.siteId;
        });

        $scope.isActive = function(str){
            var path = $location.path();
            return path === str;
        };

    }]);

    app.controller("IndexController", ["$location", "Site", function($location, Site) {

        // Hack the planet. Get all sites w/ limit=500 to force pagination.
        Site.query({limit: 500}, function(response){
            var sites = response.data;
            if (!sites.length || sites.length > 1) {
                $location.path("/sites");
            } else {
                // If there's a single site, just go there.
                $location.path("/sites/" + sites[0].id);
            }
            $location.replace();
        });
    }]);

    app.controller("ProfileController", ["User", "$location", "$q", function(User, $location, $q) {
        $q.all([
            User.get({id: 0}).$promise,
        ]).then(function(results){
            $location.path("/users/" + results[0].id);
        });

    }]);

    app.controller("SitesController", ["$scope", "$q", "$location", "Site", "User", function($scope, $q, $location, Site, User) {

        $scope.loading = true;
        $scope.sites = [];
        $scope.user = null;
        $scope.site = new Site();
        $scope.error = null;

        // Again get all sites w/ limit=500 to force pagination. This sucks.
        $q.all([
            User.get({id: 0}).$promise,
            Site.query({limit: 500}).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.sites = results[1].data;

            $scope.loading = false;
        });

        $scope.createSite = function(){
            $scope.site.$save(function(site){
                $location.path("/sites/" + site.id);
            }, function(data){
                $scope.error = data.data.error;
            });
        };
    }]);

    app.controller("SiteController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "Site", "User", "Device", "Network", "Change", "Interface", function($scope, $route, $location, $q, $routeParams, Site, User,
                     Device, Network, Change, Interface) {

        $scope.loading = true;
        $scope.user = null;
        $scope.site = null;
        $scope.total_devices = null;
        $scope.total_interfaces = null;
        $scope.total_networks = null;
        $scope.total_ipv4 = null ;
        $scope.total_ipv6 = null;
        $scope.total_reserved = null;
        $scope.total_allocated = null;
        $scope.total_assigned = null;
        $scope.total_orphaned = null;
        $scope.admin = false;
        $scope.updateError = null;
        $scope.deleteError = null;
        $scope.changes = [];

        var siteId = $routeParams.siteId;

        var netsets = {
            siteId: siteId,
            include_ips: true,
            limit: 1
        }
        var net4 = {
            siteId: siteId,
            include_ips: true,
            ip_version: 4,
            limit: 1
        } 
        var net6 = {
            siteId: siteId,
            include_ips: true,
            ip_version: 6,
            limit: 1
         }
        var ipam_reserved = {
            siteId: siteId,
            include_ips: true,
            state: "reserved",
            limit:1
        }
        var ipam_allocated = {
            siteId: siteId,
            include_ips: true,
            state: "allocated",
            limit: 1
        }
        var ipam_assigned = {
            siteId: siteId,
            include_ips: true,
            state: "assigned",
            limit: 1
        }
        var ipam_orphaned = {
            siteId: siteId,
            include_ips: true,
            state: "orphaned",
            limit: 1
        }
        var change_go = {
            siteId: siteId,
            limit: 10
        }

        $q.all([
            User.get({id: 0}).$promise,
            Site.get({id: siteId}).$promise,
            Device.query({siteId: siteId, limit:1}).$promise,
            Network.query(netsets).$promise,
            Network.query(net4).$promise,
            Network.query(net6).$promise,
            Network.query(ipam_reserved).$promise,
            Network.query(ipam_allocated).$promise,
            Network.query(ipam_assigned).$promise,
            Network.query(ipam_orphaned).$promise,
            Change.query(change_go).$promise,
            Interface.query({siteId: siteId, limit:1}).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.site = results[1];
            $scope.total_devices = results[2].count;
            $scope.total_networks = results[3].count;
            $scope.total_ipv4 = results[4].count;
            $scope.total_ipv6 = results[5].count;
            $scope.total_reserved = results[6].count;
            $scope.total_allocated = results[7].count;
            $scope.total_assigned = results[8].count;
            $scope.total_orphaned = results[9].count;
            $scope.changes = results[10].data;
            $scope.total_interfaces = results[11].count;
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);
            $scope.loading = false;

            // BEG chart
            $scope.labels = [
                "Assigned",
                "Allocated",
                "Reserved",
                "Orphaned"
            ];
            $scope.data = [
                $scope.total_assigned,
                $scope.total_allocated,
                $scope.total_reserved,
                $scope.total_orphaned
            ];
            // END chart
        });

        $scope.updateSite = function(){
            $scope.site.$update(function(){
                $route.reload();
            }, function(data){
                $scope.updateError = data.data.error;
            });
        };

        $scope.deleteSite = function(){
            $scope.site.$delete(function(){
                $location.path("/sites");
            }, function(data){
                $scope.deleteError = data.data.error;
            });
        };
    }]);

    app.controller("UsersController",
            ["$scope", "$route", "$location", "$q", "$routeParams", function($scope, $route, $location, $q, $routeParams) {
        $scope.loading = true;
    }]);

    app.controller("UserController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", function($scope, $route, $location, $q, $routeParams, User) {

        $scope.loading = true;
        $scope.currentUser = null;
        $scope.profileUser = null;
        $scope.secret_key = null;
        var userId = $routeParams.userId;
        $scope.isSelf = false;

        $scope.showKey = function(){
            User.get({id: userId, with_secret_key: true}, function(data){
                $scope.secret_key = data.secret_key;
            });
        };

        $scope.rotateKey = function(){
            $scope.profileUser.rotateSecretKey().success(function(new_key){
                $scope.secret_key = new_key;
            });
        };

        $q.all([
            User.get({id: 0}).$promise,
            User.get({id: userId}).$promise,
        ]).then(function(results){
            $scope.loading = false;
            $scope.currentUser = results[0];
            $scope.profileUser = results[1];
            $scope.isSelf = $scope.currentUser.id === $scope.profileUser.id;
        });
    }]);

    app.controller("NetworksController",
            ["$scope", "$location", "$q", "$routeParams", "User", "Network", "Attribute", "pagerParams", "Paginator", function($scope, $location, $q,  $routeParams,
                     User, Network, Attribute, pagerParams, Paginator) {
        $scope.loading = true;
        $scope.user = null;
        $scope.attributes = {};
        $scope.networks = [];
        $scope.paginator = null;
        $scope.error = null;
        $scope.admin = false;
        var siteId = $scope.siteId = $routeParams.siteId;

        $scope.formMode = "create";
        $scope.formUrl = "includes/networks-form.html";
        $scope.formData = {
            attributes: []
        };
        $scope.ip_versions = ['4', '6'];
        $scope.states = ['allocated', 'assigned', 'reserved', 'orphaned'];

        $scope.filters = {
            include_ips: nsot.qpBool($routeParams, "include_ips", true),
            include_networks: nsot.qpBool($routeParams, "include_networks", true),
            root_only: nsot.qpBool($routeParams, "root_only", false),
            ip_version: $routeParams.ip_version,
            state: $routeParams.state
        };

        var params = _.extend(pagerParams(), {
            siteId: siteId,
        }, $scope.filters);

        $q.all([
            User.get({id: 0}).$promise,
            Network.query(params).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.networks = results[1].data;
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);


            $scope.paginator = new Paginator(results[1]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#createNetworkModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Network"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});

                $scope.formData.attributes = _.chain($scope.attributes)
                    .filter(function(value){
                        return value.display;
                    })
                    .sortBy(function(value){
                        return value.required ? 0 : 1;
                    })
                    .map(function(value){
                        return {
                            name: value.name
                        };
                    }).value();
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#createNetworkModal");
        });


        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.createNetwork = function() {
            var network = Network.fromForm($scope.formData);
            network.$save({siteId: siteId}, function(network){
                $location.path("/sites/" + siteId + "/networks/" + network.id);
            }, function(data){
                $scope.error = data.data.error;
            });
        };

    }]);

    app.controller("NetworkController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", "Network", "Attribute", "Change", function($scope, $route, $location, $q, $routeParams,
                     User, Network, Attribute, Change) {

        $scope.loading = true;
        $scope.user = {};
        $scope.network = {};
        $scope.attributes = {};
        $scope.admin = false;
        $scope.updateError = null;
        $scope.deleteError = null;
        var siteId = $scope.siteId = $routeParams.siteId;
        var networkId = $scope.networkId = $routeParams.networkId;
        $scope.formMode = "update";
        $scope.formUrl = "includes/networks-form.html";
        $scope.formData = {
            attributes: []
        };


        $q.all([
            User.get({id: 0}).$promise,
            Network.get({siteId: siteId, id: networkId}).$promise,
            Change.query({
                siteId: siteId, limit: 10, offset: 0,
                resource_name: "Network", resource_id: networkId
            }).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.network = results[1];
            $scope.changes = results[2].data;
            $scope.formData = $scope.network.toForm();
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);

            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#updateNetworkModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Network"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#updateNetworkModal");
        });

        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.updateNetwork = function(){
            var network = $scope.network;
            network.updateFromForm($scope.formData);
            network.$update({siteId: siteId}, function(data){
                $route.reload();
            }, function(data){
                $scope.updateError = data.data.error;
            });
        };

        $scope.deleteNetwork = function(){
            $scope.network.$delete({siteId: siteId}, function(){
                $location.path("/sites/" + siteId + "/networks");
            }, function(data){
                $scope.deleteError = data.data.error;
            });
        };


    }]);

    app.controller("DevicesController",
            ["$scope", "$location", "$q", "$routeParams", "User", "Device", "Attribute", "pagerParams", "Paginator", function($scope, $location, $q, $routeParams,
                     User, Device, Attribute, pagerParams, Paginator) {

        $scope.loading = true;
        $scope.user = null;
        $scope.attributes = {};
        $scope.devices = [];
        $scope.paginator = null;
        $scope.error = null;
        $scope.admin = false;
        var siteId = $scope.siteId = $routeParams.siteId;

        $scope.formUrl = "includes/devices-form.html";
        $scope.formData = {
            attributes: []
        };

        var params = _.extend(pagerParams(), {
            siteId: siteId,
        });

        $q.all([
            User.get({id: 0}).$promise,
            Device.query(params).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.devices = results[1].data;
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);


            $scope.paginator = new Paginator(results[1]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#createDeviceModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Device"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});

                $scope.formData.attributes = _.chain($scope.attributes)
                    .filter(function(value){
                        return value.display;
                    })
                    .sortBy(function(value){
                        return value.required ? 0 : 1;
                    })
                    .map(function(value){
                        return {
                            name: value.name
                        };
                    }).value();
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#createDeviceModal");
        });


        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.createDevice = function() {
            var device = Device.fromForm($scope.formData);
            device.$save({siteId: siteId}, function(device){
                $location.path("/sites/" + siteId + "/devices/" + device.id);
            }, function(data){
                $scope.error = data.data.error;
            });
        };

    }]);

    app.controller("DeviceController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", "Device", "Attribute", "Change", function($scope, $route, $location, $q, $routeParams,
                     User, Device, Attribute, Change) {

        $scope.loading = true;
        $scope.user = {};
        $scope.device = {};
        $scope.attributes = {};
        $scope.admin = false;
        $scope.updateError = null;
        $scope.deleteError = null;
        var siteId = $scope.siteId = $routeParams.siteId;
        var deviceId = $scope.deviceId = $routeParams.deviceId;
        $scope.formMode = "update";
        $scope.formUrl = "includes/devices-form.html";
        $scope.formData = {
            attributes: []
        };


        $q.all([
            User.get({id: 0}).$promise,
            Device.get({siteId: siteId, id: deviceId}).$promise,
            Change.query({
                siteId: siteId, limit: 10, offset: 0,
                resource_name: "Device", resource_id: deviceId
            }).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.device = results[1];
            $scope.changes = results[2].data;
            $scope.formData = $scope.device.toForm();
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);

            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#updateDeviceModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Device"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#updateDeviceModal");
        });

        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.updateDevice = function(){
            var device = $scope.device;
            device.updateFromForm($scope.formData);
            device.$update({siteId: siteId}, function(data){
                $route.reload();
            }, function(data){
                $scope.updateError = data.data.error;
            });
        };

        $scope.deleteDevice = function(){
            $scope.device.$delete({siteId: siteId}, function(){
                $location.path("/sites/" + siteId + "/devices");
            }, function(data){
                $scope.deleteError = data.data.error;
            });
        };

    }]);

    app.controller("InterfacesController",
            ["$scope", "$location", "$q", "$routeParams", "User", "Interface", "Attribute", "Device", "pagerParams", "Paginator", function($scope, $location, $q, $routeParams,
                     User, Interface, Attribute, Device, pagerParams, Paginator) {

        $scope.loading = true;
        $scope.user = null;
        $scope.attributes = {};
        $scope.interfaces = [];
        $scope.devices = [];
        $scope.paginator = null;
        $scope.error = null;
        $scope.admin = false;
        var siteId = $scope.siteId = $routeParams.siteId;

        $scope.formMode = "create";
        $scope.formUrl = "includes/interfaces-form.html";
        $scope.formData = {
            attributes: [],
            devices: []
        };

        var params = _.extend(pagerParams(), {
            siteId: siteId,
        });

        $q.all([
            User.get({id: 0}).$promise,
            Interface.query(params).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.interfaces = results[1].data;
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);


            $scope.paginator = new Paginator(results[1]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#createInterfaceModal", function(e){
            Device.query({siteId: siteId}, function(response){
                $scope.devices = response.data;
                $scope.formData.devices = _.chain($scope.devices).value();
                /*
                $scope.getDeviceById = _.reduce(
                        $scope.devices, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});

                $scope.formData.devices = _.chain($scope.devices).value();
                    .filter(function(value){
                        return value.display;
                    })
                    .sortBy(function(value){
                        return value.required ? 0 : 1;
                    })
                    .map(function(value){
                        return {
                            name: value.name
                        };
                    }).value();
                */
            });
        });

        $("body").on("show.bs.modal", "#createInterfaceModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Interface"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});

                $scope.formData.attributes = _.chain($scope.attributes)
                    .filter(function(value){
                        return value.display;
                    })
                    .sortBy(function(value){
                        return value.required ? 0 : 1;
                    })
                    .map(function(value){
                        return {
                            name: value.name
                        };
                    }).value();
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#createInterfaceModal");
        });


        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.createInterface = function() {
            var iface = Interface.fromForm($scope.formData);
            iface.$save({siteId: siteId}, function(iface){
                $location.path("/sites/" + siteId + "/interfaces/" + iface.id);
            }, function(data){
                $scope.error = data.data.error;
            });
        };

    }]);

    app.controller("InterfaceController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", "Interface", "Attribute", "Change", function($scope, $route, $location, $q, $routeParams,
                     User, Interface, Attribute, Change) {

        $scope.loading = true;
        $scope.user = {};
        $scope.iface = {};
        $scope.schema = null;
        $scope.attributes = {};
        $scope.admin = false;
        $scope.updateError = null;
        $scope.deleteError = null;
        var siteId = $scope.siteId = $routeParams.siteId;
        var ifaceId = $scope.ifaceId = $routeParams.ifaceId;
        $scope.formMode = "update";
        $scope.formUrl = "includes/interfaces-form.html";
        $scope.formData = {
            attributes: []
        };


        $q.all([
            User.get({id: 0}).$promise,
            Interface.get({siteId: siteId, id: ifaceId}).$promise,
            Interface.schema({siteId: siteId, id: ifaceId}).$promise,
            Change.query({
                siteId: siteId, limit: 10, offset: 0,
                resource_name: "Interface", resource_id: ifaceId
            }).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.iface = results[1];
            $scope.schema = results[2].schema;
            $scope.changes = results[3].data;
            $scope.formData = $scope.iface.toForm();
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);

            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $("body").on("show.bs.modal", "#updateInterfaceModal", function(e){
            Attribute.query({siteId: siteId, limit: 500, resource_name: "Interface"}, function(response){
                $scope.attributes = response.data;
                $scope.attributesByName = _.reduce(
                        $scope.attributes, function(acc, value, key){
                    acc[value.name] = value;
                    return acc;
                }, {});
            });
        });

        $scope.$on('$destroy', function() {
            $("body").off("show.bs.modal", "#updateInterfaceModal");
        });

        $scope.addAttr = function() {
            $scope.formData.attributes.push({});
        };

        $scope.removeAttr = function(idx) {
            $scope.formData.attributes.splice(idx, 1);
        };

        $scope.updateInterface = function(){
            var iface = $scope.iface;
            iface.updateFromForm($scope.formData);
            iface.$update({siteId: siteId}, function(data){
                $route.reload();
            }, function(data){
                $scope.updateError = data.data.error;
            });
        };

        $scope.deleteInterface = function(){
            $scope.iface.$delete({siteId: siteId}, function(){
                $location.path("/sites/" + siteId + "/interfaces");
            }, function(data){
                $scope.deleteError = data.data.error;
            });
        };

    }]);

    app.controller("AttributesController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", "Attribute", function($scope, $route, $location, $q, $routeParams,
                     User, Attribute) {

        $scope.loading = true;
        $scope.user = null;
        $scope.attributes = [];
        $scope.error = null;
        $scope.admin = false;
        $scope.formMode = "create";
        $scope.formUrl = "includes/attributes-form.html";
        $scope.formData = {};

        var siteId = $scope.siteId = $routeParams.siteId;

        $q.all([
            User.get({id: 0}).$promise,
            Attribute.query({siteId: siteId, limit: 1000}).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.attributes = results[1].data;
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $scope.createAttribute = function(){
            var attribute = Attribute.fromForm($scope.formData);
            attribute.$save({siteId: siteId}, function(attr){
                $location.path(
                    "/sites/" + siteId + "/attributes/" + attr.id
                );
            }, function(data){
                $scope.error = data.data.error;
            });
        };

    }]);

    app.controller("AttributeController",
            ["$scope", "$route", "$location", "$q", "$routeParams", "User", "Attribute", function($scope, $route, $location, $q, $routeParams,
                     User, Attribute) {

        $scope.loading = true;
        $scope.user = null;
        $scope.attribute = null;
        $scope.admin = false;
        $scope.updateError = null;
        $scope.deleteError = null;
        $scope.formMode = "update";
        $scope.formUrl = "includes/attributes-form.html";
        $scope.formData = {};

        var siteId = $scope.siteId = $routeParams.siteId;
        var attributeId = $scope.attributeId = $routeParams.attributeId;

        $q.all([
            User.get({id: 0}).$promise,
            Attribute.get({siteId: siteId, id: attributeId}).$promise
        ]).then(function(results){
            $scope.user = results[0];
            $scope.attribute = results[1];
            $scope.formData = $scope.attribute.toForm();
            $scope.admin = $scope.user.isAdmin(siteId, ["admin"]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

        $scope.updateAttribute = function(){
            $scope.attribute.updateFromForm($scope.formData);
            $scope.attribute.$update({siteId: siteId}, function(){
                $route.reload();
            }, function(data){
                $scope.updateError = data.data.error;
            });
        };

        $scope.deleteAttribute = function(){
            $scope.attribute.$delete({siteId: siteId}, function(){
                $location.path("/sites/" + siteId + "/attributes");
            }, function(data){
                $scope.deleteError = data.data.error;
            });
        };

    }]);

    app.controller("ChangesController",
            ["$scope", "$location", "$q", "$routeParams", "Change", "pagerParams", "Paginator", function($scope, $location, $q, $routeParams, Change,
                     pagerParams, Paginator) {

        $scope.loading = true;
        $scope.changes = [];
        $scope.paginator = null;

        var siteId = $scope.siteId = $routeParams.siteId;
        var params = pagerParams();

        $q.all([
            Change.query(_.extend({siteId: siteId}, params)).$promise
        ]).then(function(results){
            $scope.changes = results[0].data;
            $scope.paginator = new Paginator(results[0]);
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

    }]);

    app.controller("ChangeController",
            ["$scope", "$location", "$q", "$routeParams", "Change", function($scope, $location, $q, $routeParams, Change) {

        $scope.loading = true;
        $scope.change = null;

        var siteId = $scope.siteId = $routeParams.siteId;
        var changeId = $scope.changeId = $routeParams.changeId;

        $q.all([
            Change.get({siteId: siteId, id: changeId}).$promise
        ]).then(function(results){
            $scope.change = results[0];
            $scope.loading = false;
        }, function(data){
            if (data.status === 404) {
                $location.path("/");
                $location.replace();
            }
        });

    }]);

})();


(function() {
    "use strict";

    var app = angular.module("nsotApp");

    app.directive("panel", function(){
        return {
            restrict: "E",
            transclude: true,
            template: "<div class='panel panel-default'>" +
                      "  <ng-transclude></ng-transclude>" +
                      "</div>"
        };
    });

    app.directive("panelHeading", function(){
        return {
            restrict: "E",
            transclude: true,
            template: "<div class='panel-heading'><strong>" +
                      "  <ng-transclude></ng-transclude>" +
                      "</strong></div>"
        };
    });

    app.directive("panelBody", function(){
        return {
            restrict: "E",
            transclude: true,
            template: "<div class='panel-body'>" +
                      "  <ng-transclude></ng-transclude>" +
                      "</div>"
        };
    });

    app.directive("panelFooter", function(){
        return {
            restrict: "E",
            transclude: true,
            template: "<div class='panel-footer'>" +
                      "  <ng-transclude></ng-transclude>" +
                      "</div>"
        };
    });

    app.directive("loadingPanel", function(){
        return {
            restrict: "E",
            templateUrl: "directives/loading-panel.html"
        };
    });

    app.directive("headingBar", function(){
        return {
            restrict: "E",
            scope: {
                "heading": "@",
                "subheading": "@"
            },
            transclude: true,
            template: "<div class='row'><div class='col-md-12'>" +
                      "  <div class='header'>" +
                      "    <h2>[[heading]]</h2>" +
                      "    <h3 ng-if='subheading'>[[subheading]]</h3>" +
                      "    <div class='buttons'>" +
                      "      <ng-transclude></ng-transclude>" +
                      "    </div>" +
                      "  </div>" +
                      "</div></div>"
        };
    });

    app.directive("nsotModal", function(){
        return {
            restrict: "E",
            scope: {
                "title": "@",
                "modalId": "@",
                "modalSize": "@"
            },
            transclude: true,
            templateUrl: "directives/nsot-modal.html"
        };
    });

    app.directive("paginator", function(){
        return {
            restrict: "E",
            scope: {
                "pager": "=",
            },
            templateUrl: "directives/paginator.html"
        };
    });

    app.directive("dropdown", function(){
        return {
            restrict: "E",
            scope: {
                "ctxtObj": "=",
            },
            templateUrl: "directives/dropdown.html"
        };
    });

})();

(function() {
    "use strict";

    var app = angular.module("nsotApp");

    app.filter("from_now", function(){
        return function(input){
            return moment.unix(input).fromNow();
        };
    });

    app.filter("ts_fmt", function(){
        return function(input){
            return moment.unix(input).format("YYYY/MM/DD hh:mm:ss a");
        };
    });

})();

(function() {
    "use strict";

    var nsot = window.nsot = nsot || {};
    var TRUTHY = ["true", "yes", "on", "1", ""];

    nsot.qpBool = function(object, path, defaultValue) {
        var val = _.get(object, path, defaultValue).toString().toLowerCase();
        for (var idx = 0; idx < TRUTHY.length; idx++) {
            var elem = TRUTHY[idx];
            if (val === elem) {
                return true;
            }
        }
        return false;
    };

    nsot.Pager = function(previous, next, count, $location) {
        this.previous = previous;
        this.next = next;
        this.count = count;
        this.$location = $location;

        // Use an 'a' element as a URL parser. How novel.
        var parser = document.createElement('a');
        parser.href = (this.next || this.previous);  // This is a hack.

        // Given "search" params; parse them into an object.
        // Ref: https://css-tricks.com/snippets/jquery/get-query-params-object/
        this.parse_query_params = function(str) {
            /// I have no idea WTF this hackery even is. Kill me.
            return str.replace(/(^\?)/, '')
                .split("&")
                .map(function(n) {
                    return n = n.split("="), this[n[0]] = n[1], this
                }.bind({}))[0];
        }

        // Use pager_params to calculate limit/offset/pages, etc.
        var pager_params = this.parse_query_params(parser.search);
        var limit = parseInt(pager_params.limit);
        var offset = parseInt(pager_params.offset);

        this.page = ((offset + limit) / limit) - 1;  // Another hack
        this.numPages = Math.ceil(count / limit);
        this.limit = limit;
        this.offset = offset - limit;

        this.hasFirst = function(){
            return this.offset !== 0;
        };

        this.hasPrevious = function(){
            return this.offset !== 0;
        };

        this.hasNext = function(){
            return this.offset + this.limit < this.count;
        };

        this.hasLast = function(){
            return this.offset + this.limit < this.count;
        };

        this.firstPage = function(){
            return 0;
        };

        this.previousPage = function(){
            return this.offset - this.limit;
        };

        this.nextPage = function(){
            return this.offset + this.limit;
        };

        this.lastPage = function(){
            return (this.numPages - 1) * this.limit;
        };

        this.firstPageUrl = function(){
            return "?" + $.param(_.defaults(
                {"offset": this.firstPage()},
                this.$location.search()
            ));
        };

        this.previousPageUrl = function(){
            return "?" + $.param(_.defaults(
                {"offset": this.previousPage()},
                this.$location.search()
            ));
        };

        this.nextPageUrl = function(){
            return "?" + $.param(_.defaults(
                {"offset": this.nextPage()},
                this.$location.search()
            ));
        };

        this.lastPageUrl = function(){
            return "?" + $.param(_.defaults(
                {"offset": this.lastPage()},
                this.$location.search()
            ));
        };
    };

    nsot.Limiter = function(limit, $location) {

        this.name = "Limit";
        this.current = limit;
        this.values = [10, 25, 50, 100];
        this.$location = $location;

        this.getUrl = function(value){
            return "?" + $.param(_.defaults(
                {"limit": value}, this.$location.search()
            ));
        };
    };

})();

(function() {
    "use strict";

    var app = angular.module("nsotApp");

    function appendTransform(defaults, transform) {
        defaults = angular.isArray(defaults) ? defaults : [defaults];
        return defaults.concat(transform);
    }

    function buildActions($http, resourceName, collectionName) {

        // Return a single object
        var resourceTransform = appendTransform(
            $http.defaults.transformResponse, function(response) {
                return response;
            }
        );

        // Return a collection of objects
        var collectionTransform = appendTransform(
            $http.defaults.transformResponse, function(response) {
                if (response != undefined) {
                    return {
                        previous: response.previous,
                        next: response.next,
                        count: response.count,
                        data: response.results
                    };
                }
                return response;
            }
        );

        // Return the schema actions for a resource endpoint
        var schemaTransform = appendTransform(
            $http.defaults.transformResponse, function(response) {
                return {
                    schema: response.actions
                };
            }
        );

        return {
            query:  {
                method: "GET", isArray: false,
                transformResponse: collectionTransform,
            },
            get: {
                method: "GET", isArray: false,
                transformResponse: resourceTransform,
            },
            update: {
                method: "PUT", isArray: false,
                transformResponse: resourceTransform,
            },
            save: {
                method: "POST", isArray: false,
                transformResponse: resourceTransform,
            },
            schema: {
                method: "OPTIONS", isArray: false,
                transformResponse: schemaTransform,
            }
        };
    }

    app.factory("Site", ["$resource", "$http", function($resource, $http){
        return $resource(
            "/api/sites/:id/",
            { id: "@id" },
            buildActions($http, "site", "sites")
        );
    }]);

    app.factory("User", ["$resource", "$http", function($resource, $http){
        var User = $resource(
            "/api/users/:id/",
            { id: "@id" },
            buildActions($http, "user", "users")
        );

        User.prototype.rotateSecretKey = function(){
            var userId = this.id;
            return $http({
                method: "POST",
                url: "/api/users/" + userId + "/rotate_secret_key/",
                data: {},
                transformResponse: appendTransform(
                    $http.defaults.transformResponse, function(response) {
                        return response.data.secret_key;
                    }
                )
            });
        };

        User.prototype.isAdmin = function(siteId, permissions){
            var user_permissions = this.permissions[siteId] || {};
                user_permissions = user_permissions.permissions || [];

            return _.any(user_permissions, function(value){
                return _.contains(permissions, value);
            });
        };

        return User;
    }]);

    app.factory("Change", ["$resource", "$http", function($resource, $http){
        return $resource(
            "/api/sites/:siteId/changes/:id/",
            { siteId: "@siteId", id: "@id" },
            buildActions($http, "change", "changes")
        );
    }]);

    app.factory("Attribute", ["$resource", "$http", function($resource, $http){
        var Attribute = $resource(
            "/api/sites/:siteId/attributes/:id/",
            { siteId: "@siteId", id: "@id" },
            buildActions($http, "attribute", "attributes")
        );

        Attribute.prototype.updateFromForm = function(formData) {
            return _.extend(this, {
                name: formData.name,
                resource_name: formData.resourceName,
                description: formData.description,
                required: formData.required,
                display: formData.display,
                multi: formData.multi,
                constraints: {
                    pattern: formData.pattern,
                    allow_empty: formData.allowEmpty,
                    valid_values: _.map(formData.validValues, function(value){
                        return value.text;
                    })
                }
            });
        };

        Attribute.fromForm = function(formData) {
            var attr = new Attribute();
            attr.updateFromForm(formData);
            return attr;
        };

        Attribute.prototype.toForm = function() {
            return {
                name: this.name,
                resourceName: this.resource_name,
                description: this.description,
                required: this.required,
                display: this.display,
                multi: this.multi,
                pattern: this.constraints.pattern,
                allowEmpty: this.constraints.allow_empty,
                validValues: _.map(this.constraints.valid_values, function(value) {
                    return { text: value };
                })
            };
        };

        return Attribute;
    }]);

    app.factory("Network", ["$resource", "$http", function($resource, $http){
        var Network = $resource(
            "/api/sites/:siteId/networks/:id/",
            { siteId: "@siteId", id: "@id" },
            buildActions($http, "network", "networks")
        );

        Network.prototype.updateFromForm = function(formData) {
            return _.extend(this, {
                cidr: formData.cidr,
                attributes: _.reduce(formData.attributes, function(acc, attribute){
                    if (!attribute.value) attribute.value = "";
                    if (_.isArray(attribute.value)) {
                        attribute.value = _.map(attribute.value, function(val){
                            return val.text;
                        });
                    }
                    acc[attribute.name] = attribute.value;
                    return acc;
                }, {})
            });
        };

        Network.fromForm = function(formData) {
            var network = new Network();
            network.updateFromForm(formData);
            return network;
        };

        Network.prototype.toForm = function() {
            return {
                cidr: this.network_address + "/" + this.prefix_length,
                attributes: _.map(_.cloneDeep(this.attributes), function(attrVal, attrKey){
                    if (_.isArray(attrVal)) {
                        attrVal = _.map(attrVal, function(val) {
                            return {text: val};
                        });
                    }

                    return {
                        name: attrKey,
                        value: attrVal
                    };

                })
            };
        };

        return Network;
    }]);

    app.factory("Device", ["$resource", "$http", function($resource, $http){
        var Device = $resource(
            "/api/sites/:siteId/devices/:id/",
            { siteId: "@siteId", id: "@id" },
            buildActions($http, "device", "devices")
        );

        Device.prototype.updateFromForm = function(formData) {
            return _.extend(this, {
                hostname: formData.hostname,
                attributes: _.reduce(formData.attributes, function(acc, attribute){
                    if (!attribute.value) attribute.value = "";
                    if (_.isArray(attribute.value)) {
                        attribute.value = _.map(attribute.value, function(val){
                            return val.text;
                        });
                    }
                    acc[attribute.name] = attribute.value;
                    return acc;
                }, {})
            });
        };

        Device.fromForm = function(formData) {
            var device = new Device();
            device.updateFromForm(formData);
            return device;
        };

        Device.prototype.toForm = function() {
            return {
                hostname: this.hostname,
                attributes: _.map(_.cloneDeep(this.attributes), function(attrVal, attrKey){
                    if (_.isArray(attrVal)) {
                        attrVal = _.map(attrVal, function(val) {
                            return {text: val};
                        });
                    }

                    return {
                        name: attrKey,
                        value: attrVal
                    };

                })
            };
        };

        return Device;
    }]);

    app.factory("Interface", ["$resource", "$http", function($resource, $http){
        var Interface = $resource(
            "/api/sites/:siteId/interfaces/:id/",
            { siteId: "@siteId", id: "@id" },
            buildActions($http, "interface", "interfaces")
        );

        Interface.prototype.updateFromForm = function(formData) {
            return _.extend(this, {
                device: formData.device,
                name: formData.name,
                description: formData.description,
                addresses: formData.addresses,
                speed: formData.speed,
                type: formData.type,
                mac_address: formData.mac_address,
                attributes: _.reduce(formData.attributes, function(acc, attribute){
                    if (!attribute.value) attribute.value = "";
                    if (_.isArray(attribute.value)) {
                        attribute.value = _.map(attribute.value, function(val){
                            return val.text;
                        });
                    }
                    acc[attribute.name] = attribute.value;
                    return acc;
                }, {})
            });
        };

        Interface.fromForm = function(formData) {
            var iface = new Interface();
            iface.updateFromForm(formData);
            return iface;
        };

        Interface.prototype.toForm = function() {
            return {
                device: this.device,
                name: this.name,
                description: this.description,
                addresses: this.addresses,
                speed: this.speed,
                type: this.type,
                mac_address: this.mac_address,
                attributes: _.map(_.cloneDeep(this.attributes), function(attrVal, attrKey){
                    if (_.isArray(attrVal)) {
                        attrVal = _.map(attrVal, function(val) {
                            return {text: val};
                        });
                    }

                    return {
                        name: attrKey,
                        value: attrVal
                    };

                })
            };
        };

        return Interface;
    }]);

    app.factory("pagerParams", ["$location", function($location){

        var defaults = {
            limit: 10,
            offset: 0,
        };

        return function() {
            var params = _.clone(defaults);
            return _.extend(params, $location.search());
        };

    }]);

    app.factory("Paginator", ["$location", function($location){
        return function(obj) {
            obj.limit = obj.data.length;  // Item count doubles as limit

            this.pager = new nsot.Pager(
                obj.previous,
                obj.next,
                obj.count,
                $location
            );
            this.limiter = new nsot.Limiter(
                obj.limit, $location
            );
        };
    }]);


})();

angular.module("nsotTemplates").run(["$templateCache", function($templateCache) {$templateCache.put("attribute.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Attributes\" subheading=\"[[attribute.name]]\">\n        <button ng-if=\"admin\"\n            class=\"btn btn-info\"\n            data-toggle=\"modal\"\n            data-target=\"#updateAttrModal\"\n        >Update Attribute</button>\n        <button ng-if=\"admin\"\n            class=\"btn btn-danger\"\n            data-toggle=\"modal\"\n            data-target=\"#deleteAttrModal\"\n        >Delete Attribute</button>\n    </heading-bar>\n\n    <div class=\"row\"><div class=\"col-sm-8 col-sm-offset-2\">\n        <panel>\n            <panel-heading>\n                Attribute\n            </panel-heading>\n            <panel-body>\n                <dl class=\"dl-horizontal\">\n                    <dt>Name</dt>\n                    <dd>[[attribute.name]]</dd>\n\n                    <dt>Resource Type</dt>\n                    <dd>[[attribute.resource_name]]</dd>\n\n                    <dt>Description</dt>\n                    <dd>[[attribute.description]]</dd>\n\n                    <dt>Value Pattern</dt>\n                    <dd>[[attribute.constraints.pattern]]</dd>\n\n                    <dt>Valid Values</dt>\n                    <dd>[[attribute.constraints.valid_values.join(\", \")]]</dd>\n\n                    <dt>Required</dt>\n                    <dd><i ng-if=\"attribute.required\" class=\"fa fa-check\"></i></dd>\n\n                    <dt>Display</dt>\n                    <dd><i ng-if=\"attribute.display\" class=\"fa fa-check\"></i></dd>\n\n                    <dt>Allow Multiple Values</dt>\n                    <dd><i ng-if=\"attribute.multi\" class=\"fa fa-check\"></i></dd>\n\n                    <dt>Allow Empty Values</dt>\n                    <dd>\n                        <i ng-if=\"attribute.constraints.allow_empty\" class=\"fa fa-check\"></i>\n                    </dd>\n\n                </dl>\n\n            </panel-body>\n       </panel>\n    </div></div>\n\n    <nsot-modal title=\"Update Attribute\" modal-id=\"updateAttrModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"updateError\" class=\"alert alert-danger\">\n                [[updateError.code]] - [[updateError.message]]\n            </div>\n            <form novalidate name=\"attrForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"updateAttribute()\"\n                    class=\"btn btn-primary\" ng-disabled=\"attrForm.$invalid\"\n            >\n                Update\n            </button>\n        </div>\n    </nsot-modal>\n\n    <nsot-modal title=\"Delete Attribute\" modal-id=\"deleteAttrModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"deleteError\" class=\"alert alert-danger\">\n                [[deleteError.code]] - [[deleteError.message]]\n            </div>\n            Are you sure you want to delete this attribute?\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\"\n                    ng-click=\"deleteAttribute()\"\n                    class=\"btn btn-primary\"\n            >\n                Delete\n            </button>\n        </div>\n    </nsot-modal>\n\n</div>\n");
$templateCache.put("attributes.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Attributes\">\n        <button\n            ng-if=\"admin\"\n            class=\"btn btn-success\"\n            data-toggle=\"modal\"\n            data-target=\"#createAttributeModal\"\n        >Create Attribute</button>\n    </heading-bar>\n\n    <nsot-modal title=\"Create Attribute\" modal-id=\"createAttributeModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"error\" class=\"alert alert-danger\">\n                [[error.code]] - [[error.message]]\n            </div>\n            <form novalidate name=\"attrForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"createAttribute()\"\n                    class=\"btn btn-primary\" ng-disabled=\"attrForm.$invalid\"\n            >\n                Create\n            </button>\n        </div>\n    </nsot-modal>\n\n    <div class=\"row\" ng-if=\"attributes.length\" class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Attributes</panel-heading>\n            <panel-body ng-if=\"!attributes.length\">\n                No Attributes\n            </panel-body>\n            <panel-body ng-if=\"attributes.length\">\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th class=\"col-sm-1\">Resource Type</th>\n                            <th class=\"col-sm-2\">Name</th>\n                            <th class=\"col-sm-3\">Description</th>\n                            <th class=\"col-sm-1\">Required</th>\n                            <th class=\"col-sm-1\">Display</th>\n                            <th class=\"col-sm-1\">Multi</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"attr in attributes\">\n                            <td>[[attr.resource_name]]</td>\n                            <td>\n                                <a href=\"/sites/[[siteId]]/attributes/[[attr.id]]\"\n                                >[[attr.name]]</a>\n                            </td>\n                            <td>[[attr.description]]</td>\n                            <td>\n                                <i ng-if=\"attr.required\" class=\"fa fa-check\"></i>\n                            </td>\n                            <td>\n                                <i ng-if=\"attr.display\" class=\"fa fa-check\"></i>\n                            </td>\n                            <td>\n                                <i ng-if=\"attr.multi\" class=\"fa fa-check\"></i>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n\n\n</div>\n");
$templateCache.put("change.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n\n    <heading-bar\n        heading=\"Changes\"\n        subheading=\"[[change.resource_name]] [[change.resource_id]]\">\n    </heading-bar>\n    <div class=\"row\"><div class=\"col-sm-8 col-sm-offset-2\">\n        <panel>\n            <panel-heading>\n                Change\n            </panel-heading>\n            <panel-body>\n                <dl class=\"dl-horizontal\">\n                    <dt>Event</dt>\n                    <dd>[[change.event]]</dd>\n\n                    <dt>Resource Type</dt>\n                    <dd>[[change.resource_name]]</dd>\n\n                    <dt>Resource ID</dt>\n                    <dd>[[change.resource_id]]</dd>\n\n                    <dt>User</dt>\n                    <dd>[[change.user.email]]</dd>\n\n                    <dt>Change At</dt>\n                    <dd>[[change.change_at|from_now]]</dd>\n\n                    <dt>Resource</dt>\n                    <dd><pre class=\"resource-block\">[[change.resource|json:4]]</pre></dd>\n                </dl>\n\n            </panel-body>\n       </panel>\n    </div></div>\n\n</div>\n");
$templateCache.put("changes.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Changes\">\n        <dropdown ctxt-obj=\"paginator.limiter\"></dropdown>\n        <paginator pager=\"paginator.pager\"></paginator>\n    </heading-bar>\n\n    <div class=\"row\" class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Changes</panel-heading>\n            <panel-body>\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th class=\"col-sm-1\">ID</th>\n                            <th class=\"col-sm-2\">User</th>\n                            <th class=\"col-sm-1\">Event</th>\n                            <th class=\"col-sm-1\">Resource Type</th>\n                            <th class=\"col-sm-1\">Resource ID</th>\n                            <th class=\"col-sm-2\">Change At</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"change in changes\">\n                            <td>\n                                <a ng-href=\"/sites/[[siteId]]/changes/[[change.id]]\">\n                                    [[change.id]]\n                                </a>\n                            </td>\n                            <td>[[change.user.email]]</td>\n                            <td>[[change.event]]</td>\n                            <td>[[change.resource_name]]</td>\n                            <td>[[change.resource_id]]</td>\n                            <td>[[change.change_at|from_now]]</td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n</div>\n");
$templateCache.put("device.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Device\"\n        subheading=\"[[device.hostname]]\">\n        <button ng-if=\"admin\"\n            class=\"btn btn-info\"\n            data-toggle=\"modal\"\n            data-target=\"#updateDeviceModal\"\n        >Update Device</button>\n        <button ng-if=\"admin\"\n            class=\"btn btn-danger\"\n            data-toggle=\"modal\"\n            data-target=\"#deleteDeviceModal\"\n        >Delete Device</button>\n    </heading-bar>\n\n    <div class=\"row\">\n        <div class=\"col-sm-4\">\n            <panel>\n                <panel-heading>\n                    Attributes\n                </panel-heading>\n                <panel-body>\n                    <dl class=\"dl-horizontal\">\n                        <dt ng-repeat-start=\"(key, value) in device.attributes\">[[key]]</dt>\n                        <dd ng-repeat-end>[[value]]</dd>\n                    </dl>\n                </panel-body>\n            </panel>\n        </div>\n        <div class=\"col-sm-8\">\n            <panel>\n                <panel-heading>\n                    Recent Changes\n                </panel-heading>\n                <panel-body>\n                    <table class=\"table table-condensed table-hover\">\n                        <thead>\n                            <tr>\n                                <th class=\"col-sm-1\">ID</th>\n                                <th class=\"col-sm-2\">User</th>\n                                <th class=\"col-sm-1\">Event</th>\n                                <th class=\"col-sm-2\">Change At</th>\n                            </tr>\n                        </thead>\n                        <tbody>\n                            <tr ng-repeat=\"change in changes\">\n                                <td>\n                                    <a ng-href=\"/sites/[[siteId]]/changes/[[change.id]]\">\n                                        [[change.id]]\n                                    </a>\n                                </td>\n                                <td>[[change.user.email]]</td>\n                                <td>[[change.event]]</td>\n                                <td>[[change.change_at|from_now]]</td>\n                            </tr>\n                            <tr>\n                                <td colspan=\"4\" class=\"text-center\">\n                                    <a ng-href=\"/sites/[[siteId]]/changes?resource_name=Device&resource_id=[[device.id]]\">\n                                        More\n                                    </a>\n                                </td>\n                            </tr>\n                        </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n    </div>\n\n    <nsot-modal title=\"Update Device\" modal-id=\"updateDeviceModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"updateError\" class=\"alert alert-danger\">\n                [[updateError.code]] - [[updateError.message]]\n            </div>\n            <form novalidate name=\"deviceForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"updateDevice()\"\n                    class=\"btn btn-primary\" ng-disabled=\"deviceForm.$invalid\"\n            >\n                Update\n            </button>\n        </div>\n    </nsot-modal>\n\n    <nsot-modal title=\"Delete Device\" modal-id=\"deleteDeviceModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"deleteError\" class=\"alert alert-danger\">\n                [[deleteError.code]] - [[deleteError.message]]\n            </div>\n            Are you sure you want to delete this device?\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\"\n                    ng-click=\"deleteDevice()\"\n                    class=\"btn btn-primary\"\n            >\n                Delete\n            </button>\n        </div>\n    </nsot-modal>\n\n\n\n</div>\n");
$templateCache.put("devices.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Device\">\n        <dropdown ctxt-obj=\"paginator.limiter\"></dropdown>\n        <paginator pager=\"paginator.pager\"></paginator>\n\n        <button\n            class=\"btn btn-success\"\n            data-toggle=\"modal\"\n            data-target=\"#createDeviceModal\"\n            ng-if=\"admin\"\n        >Create Device</button>\n    </heading-bar>\n\n    <nsot-modal title=\"Create Device\" modal-id=\"createDeviceModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"error\" class=\"alert alert-danger\">\n                [[error.code]] - [[error.message]]\n            </div>\n            <form novalidate name=\"deviceForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"createDevice()\"\n                    class=\"btn btn-primary\" ng-disabled=\"deviceForm.$invalid\"\n            >\n                Create\n            </button>\n        </div>\n    </nsot-modal>\n\n    <div class=\"row\" class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Devices</panel-heading>\n            <panel-body ng-if=\"!devices.length\" class=\"text-center\">\n                No Devices\n            </panel-body>\n            <panel-body ng-if=\"devices.length\">\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th class=\"col-sm-3\">Hostname</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"device in devices\">\n                            <td>\n                                <a href=\"/sites/[[siteId]]/devices/[[device.id]]\"\n                                >[[device.hostname]]</a>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n\n\n</div>\n");
$templateCache.put("index.html","<loading-panel></loading-panel>\n");
$templateCache.put("interface.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Interface\"\n        subheading=\"[[iface.name]]\">\n        <button ng-if=\"admin\"\n            class=\"btn btn-info\"\n            data-toggle=\"modal\"\n            data-target=\"#updateInterfaceModal\"\n        >Update Interface</button>\n        <button ng-if=\"admin\"\n            class=\"btn btn-danger\"\n            data-toggle=\"modal\"\n            data-target=\"#deleteInterfaceModal\"\n        >Delete Interface</button>\n    </heading-bar>\n\n    <div class=\"row\">\n        <div class=\"col-sm-4\">\n            <panel>\n                <panel-heading>\n                    Attributes\n                </panel-heading>\n                <panel-body>\n                    <dl class=\"dl-horizontal\">\n                        <dt ng-repeat-start=\"(key, value) in iface.attributes\">[[key]]</dt>\n                        <dd ng-repeat-end>[[value]]</dd>\n                    </dl>\n                </panel-body>\n            </panel>\n        </div>\n\n        <div class=\"col-sm-8\">\n            <panel>\n                <panel-heading>\n                    Fields\n                </panel-heading>\n                <panel-body>\n                    <dl class=\"dl-horizontal\">\n			<dt>Name</dt>\n			<dd>[[iface.name]]</dd>\n\n			<dt>Device</dt>\n			<dd>\n                            <a ng-href=\"/sites/[[siteId]]/devices/[[iface.device]]/\">\n                                [[iface.device]]\n                            </a>\n                        </dd>\n\n			<dt>Description</dt>\n			<dd>[[iface.description]]</dd>\n\n			<dt>Addresses</dt>\n			<dd>[[iface.addresses]]</dd>\n\n			<dt>Speed</dt>\n			<dd>[[iface.speed]]</dd>\n\n			<dt>Type</dt>\n			<dd>[[iface.type]]</dd>\n\n			<dt>MAC Address</dt>\n			<dd>[[iface.mac_address]]</dd>\n\n			<dt>Parent</dt>\n			<dd>[[iface.parent_id]]</dd>\n                    </dl>\n                </panel-body>\n            </panel>\n        </div>\n    </div>\n\n    <div class=\"row\">\n        <div class=\"col-sm-12\">\n            <panel>\n                <panel-heading>\n                    Recent Changes\n                </panel-heading>\n                <panel-body>\n                    <table class=\"table table-condensed table-hover\">\n                        <thead>\n                            <tr>\n                                <th class=\"col-sm-1\">ID</th>\n                                <th class=\"col-sm-2\">User</th>\n                                <th class=\"col-sm-1\">Event</th>\n                                <th class=\"col-sm-2\">Change At</th>\n                            </tr>\n                        </thead>\n                        <tbody>\n                            <tr ng-repeat=\"change in changes\">\n                                <td>\n                                    <a ng-href=\"/sites/[[siteId]]/changes/[[change.id]]\">\n                                        [[change.id]]\n                                    </a>\n                                </td>\n                                <td>[[change.user.email]]</td>\n                                <td>[[change.event]]</td>\n                                <td>[[change.change_at|from_now]]</td>\n                            </tr>\n                            <tr>\n                                <td colspan=\"4\" class=\"text-center\">\n                                    <a\n                                        ng-href=\"/sites/[[siteId]]/changes?resource_name=Interface&resource_id=[[iface.id]]\">\n                                        More\n                                    </a>\n                                </td>\n                            </tr>\n                        </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n    </div>\n\n    <nsot-modal title=\"Update Interface\" modal-id=\"updateInterfaceModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"updateError\" class=\"alert alert-danger\">\n                [[updateError.code]] - [[updateError.message]]\n            </div>\n            <form novalidate name=\"interfaceForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"updateInterface()\"\n                    class=\"btn btn-primary\" ng-disabled=\"interfaceForm.$invalid\"\n            >\n                Update\n            </button>\n        </div>\n    </nsot-modal>\n\n    <nsot-modal title=\"Delete Interface\" modal-id=\"deleteInterfaceModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"deleteError\" class=\"alert alert-danger\">\n                [[deleteError.code]] - [[deleteError.message]]\n            </div>\n            Are you sure you want to delete this interface?\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\"\n                    ng-click=\"deleteInterface()\"\n                    class=\"btn btn-primary\"\n            >\n                Delete\n            </button>\n        </div>\n    </nsot-modal>\n\n\n\n</div>\n");
$templateCache.put("interfaces.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Interface\">\n        <dropdown ctxt-obj=\"paginator.limiter\"></dropdown>\n        <paginator pager=\"paginator.pager\"></paginator>\n\n        <button\n            class=\"btn btn-success\"\n            data-toggle=\"modal\"\n            data-target=\"#createInterfaceModal\"\n            ng-if=\"admin\"\n        >Create Interface</button>\n    </heading-bar>\n\n    <nsot-modal title=\"Create Interface\" modal-id=\"createInterfaceModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"error\" class=\"alert alert-danger\">\n                [[error.code]] - [[error.message]]\n            </div>\n            <form novalidate name=\"interfaceForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"createInterface()\"\n                    class=\"btn btn-primary\" ng-disabled=\"interfaceForm.$invalid\"\n            >\n                Create\n            </button>\n        </div>\n    </nsot-modal>\n\n    <div class=\"row\" class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Interfaces</panel-heading>\n            <panel-body ng-if=\"!interfaces.length\" class=\"text-center\">\n                No Interfaces\n            </panel-body>\n            <panel-body ng-if=\"interfaces.length\">\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th class=\"col-sm-3\">Name</th>\n                            <th class=\"col-sm-1\">Device</th>\n                            <th class=\"col-sm-1\">Speed</th>\n                            <th class=\"col-sm-1\">Type</th>\n                            <th class=\"col-sm-1\">MAC</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"iface in interfaces\">\n                            <td>\n                                <a\n                                    href=\"/sites/[[siteId]]/interfaces/[[iface.id]]\"\n                                >[[iface.name]]</a>\n                            </td>\n                            <td>\n                                <a\n                                    href=\"/sites/[[siteId]]/devices/[[iface.device]]\"\n                                >[[iface.device]]</a>\n                            </td>\n                            <td>\n                                [[iface.speed]]\n                            </td>\n                            <td>\n                                [[iface.type]]\n                            </td>\n                            <td>\n                                [[iface.mac_address]]\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n\n\n</div>\n");
$templateCache.put("network.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Network\"\n        subheading=\"[[network.network_address]]/[[network.prefix_length]]\">\n        <button ng-if=\"admin\"\n            class=\"btn btn-info\"\n            data-toggle=\"modal\"\n            data-target=\"#updateNetworkModal\"\n        >Update Network</button>\n        <button ng-if=\"admin\"\n            class=\"btn btn-danger\"\n            data-toggle=\"modal\"\n            data-target=\"#deleteNetworkModal\"\n        >Delete Network</button>\n    </heading-bar>\n\n    <div class=\"row\"><div class=\"col-sm-12\"><div class=\"adv-buttons\">\n        <button class=\"btn btn-default\"\n                ng-click=\"filters.root_only = !filters.root_only\"\n                ng-class=\"{active: filters.root_only}\"\n        >Root Only</button>\n        <div class=\"btn-group\" role=\"group\">\n            <button class=\"btn btn-default\"\n                    ng-click=\"filters.include_networks = !filters.include_networks\"\n                    ng-class=\"{active: filters.include_networks}\"\n            >Networks</button>\n            <button class=\"btn btn-default\"\n                    ng-click=\"filters.include_ips = !filters.include_ips\"\n                    ng-class=\"{active: filters.include_ips}\"\n            >IPs</button>\n        </div>\n\n        <form style=\"display: inline;\" method=\"get\" action=\"\">\n            <input type=\"hidden\" name=\"root_only\" ng-value=\"filters.root_only\">\n            <input type=\"hidden\" name=\"include_ips\" ng-value=\"filters.include_ips\">\n            <input type=\"hidden\" name=\"include_networks\" ng-value=\"filters.include_networks\">\n            <input type=\"submit\" class=\"btn btn-primary\" value=\"Update Filters\">\n        </form>\n    </div></div></div>\n\n    <div class=\"row\">\n        <div class=\"col-sm-4\">\n            <panel>\n                <panel-heading>\n                    Attributes\n                </panel-heading>\n                <panel-body>\n                    <dl class=\"dl-horizontal\">\n                        <dt ng-repeat-start=\"(key, value) in network.attributes\">[[key]]</dt>\n                        <dd ng-repeat-end>[[value]]</dd>\n                    </dl>\n\n                </panel-body>\n            </panel>\n        </div>\n        <div class=\"col-sm-8\">\n            <panel>\n                <panel-heading>\n                    Subnetworks\n                </panel-heading>\n                <panel-body>\n                    Coming Soon!\n                </panel-body>\n            </panel>\n        </div>\n    </div>\n\n    <hr>\n\n    <div class=\"row\">\n        <div class=\"col-sm-12\">\n            <panel>\n                <panel-heading>\n                    Recent Changes\n                </panel-heading>\n                <panel-body>\n                    <table class=\"table table-condensed table-hover\">\n                        <thead>\n                            <tr>\n                                <th class=\"col-sm-1\">ID</th>\n                                <th class=\"col-sm-2\">User</th>\n                                <th class=\"col-sm-1\">Event</th>\n                                <th class=\"col-sm-2\">Change At</th>\n                            </tr>\n                        </thead>\n                        <tbody>\n                            <tr ng-repeat=\"change in changes\">\n                                <td>\n                                    <a ng-href=\"/sites/[[siteId]]/changes/[[change.id]]\">\n                                        [[change.id]]\n                                    </a>\n                                </td>\n                                <td>[[change.user.email]]</td>\n                                <td>[[change.event]]</td>\n                                <td>[[change.change_at|from_now]]</td>\n                            </tr>\n                            <tr>\n                                <td colspan=\"4\" class=\"text-center\">\n                                    <a ng-href=\"/sites/[[siteId]]/changes?resource_name=Network&resource_id=[[network.id]]\">\n                                        More\n                                    </a>\n                                </td>\n                            </tr>\n                        </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n    </div>\n\n    <nsot-modal title=\"Update Network\" modal-id=\"updateNetworkModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"updateError\" class=\"alert alert-danger\">\n                [[updateError.code]] - [[updateError.message]]\n            </div>\n            <form novalidate name=\"networkForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"updateNetwork()\"\n                    class=\"btn btn-primary\" ng-disabled=\"networkForm.$invalid\"\n            >\n                Update\n            </button>\n        </div>\n    </nsot-modal>\n\n    <nsot-modal title=\"Delete Network\" modal-id=\"deleteNetworkModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"deleteError\" class=\"alert alert-danger\">\n                [[deleteError.code]] - [[deleteError.message]]\n            </div>\n            Are you sure you want to delete this network?\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\"\n                    ng-click=\"deleteNetwork()\"\n                    class=\"btn btn-primary\"\n            >\n                Delete\n            </button>\n        </div>\n    </nsot-modal>\n\n\n\n</div>\n");
$templateCache.put("networks.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Network\">\n        <dropdown ctxt-obj=\"paginator.limiter\"></dropdown>\n        <paginator pager=\"paginator.pager\"></paginator>\n\n        <button\n            class=\"btn btn-success\"\n            data-toggle=\"modal\"\n            data-target=\"#createNetworkModal\"\n            ng-if=\"admin\"\n        >Create Network</button>\n    </heading-bar>\n\n    <nsot-modal title=\"Create Network\" modal-id=\"createNetworkModal\" modal-size=\"large\">\n        <div class=\"modal-body\">\n            <div ng-if=\"error\" class=\"alert alert-danger\">\n                [[error.code]] - [[error.message]]\n            </div>\n            <form novalidate name=\"networkForm\" class=\"nsot-form\">\n                <div ng-include=\"formUrl\"></div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"createNetwork()\"\n                    class=\"btn btn-primary\" ng-disabled=\"networkForm.$invalid\"\n            >\n                Create\n            </button>\n        </div>\n    </nsot-modal>\n\n\n    <div class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n<div class=\"adv-buttons\">\n\n            <button class=\"btn btn-default\"\n                    ng-click=\"filters.root_only = !filters.root_only\"\n                    ng-class=\"{active: filters.root_only}\"\n            >Root Only</button>\n            <div class=\"btn-group\" role=\"group\">\n                <button class=\"btn btn-default\"\n                        ng-click=\"filters.include_networks = !filters.include_networks\"\n                        ng-class=\"{active: filters.include_networks}\"\n                >Networks</button>\n                <button class=\"btn btn-default\"\n                        ng-click=\"filters.include_ips = !filters.include_ips\"\n                        ng-class=\"{active: filters.include_ips}\"\n                >IPs</button>\n            </div>\n            <div class=\"btn-group\">\n                <select name=\"ip_version\"\n                        class=\"form-control\"\n                        ng-model=\"selectedVersion\"\n                        ng-change=\"filters.ip_version = selectedVersion\"\n                        ng-options=\"selectedVersion for selectedVersion in ip_versions\"\n                        ng-init=\'selectedVersion = filters.ip_version\'\n                    >\n                    <option value=\"\" disabled>IP Version</option>\n                    {{selectedVersion}}\n                </select>\n            </div>\n            <div class=\"btn-group\">\n                <select name=\"state\"\n                        class=\"form-control\"\n                        ng-model=\"selectedState\"\n                        ng-change=\"filters.state = selectedState\"\n                        ng-options=\"selectedState for selectedState in states\"\n                        ng-init=\'selectedState = filters.state\'\n                    >\n                    <option value=\"\" disabled>State</option>\n                    {{selectedState}}\n                </select>\n            </div>\n        <form style=\"display: inline;\" method=\"get\" action=\"\">\n            <input type=\"hidden\" name=\"root_only\" ng-value=\"filters.root_only\">\n            <input type=\"hidden\" name=\"include_ips\" ng-value=\"filters.include_ips\">\n            <input type=\"hidden\" name=\"include_networks\" ng-value=\"filters.include_networks\">\n            <input type=\"hidden\" name=\"ip_version\" ng-value=\"filters.ip_version\">\n            <input type=\"hidden\" name=\"state\" ng-value=\"filters.state\">\n            <input type=\"submit\" class=\"btn btn-primary\" value=\"Update Filters\">\n        </form>\n\n    </div></div></div>\n\n    <div class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Networks</panel-heading>\n            <panel-body ng-if=\"!networks.length\" class=\"text-center\">\n                No Networks\n            </panel-body>\n            <panel-body ng-if=\"networks.length\">\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th class=\"col-sm-1\">Network Address</th>\n                            <th class=\"col-sm-1\">Prefix Length</th>\n                            <th class=\"col-sm-1\">IP Version</th>\n                            <th class=\"col-sm-1\">State</th>\n                            <th class=\"col-sm-1\">IP Address</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"network in networks\">\n                            <td>\n                                <a href=\"/sites/[[siteId]]/networks/[[network.id]]\">\n                                    [[network.network_address]]\n                                </a>\n                            </td>\n                            <td>\n                                <a href=\"/sites/[[siteId]]/networks/?prefix_length=[[network.prefix_length]]\">\n                                    [[network.prefix_length]]\n                                </a>\n                            </td>\n                            <td>\n                                <a href=\"/sites/[[siteId]]/networks/?ip_version=[[network.ip_version]]\">\n                                    [[network.ip_version]]\n                                </a>\n                            </td>\n                            <td>\n                                <a href=\"/sites/[[siteId]]/networks/?state=[[network.state]]\">\n                                    [[network.state]]\n                                </a>\n                            </td>\n                            <td>\n                                <i ng-if=\"network.is_ip\" class=\"fa fa-check\"></i>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n\n\n</div>\n");
$templateCache.put("site.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"[[site.name]]\">\n        <button ng-if=\"admin\"\n            class=\"btn btn-info\"\n            data-toggle=\"modal\"\n            data-target=\"#updateSiteModal\"\n        >Update Site</button>\n        <button ng-if=\"admin\"\n            class=\"btn btn-danger\"\n            data-toggle=\"modal\"\n            data-target=\"#deleteSiteModal\"\n        >Delete Site</button>\n    </heading-bar>\n\n    <div class=\"row\">\n        <div class=\"col-md-12\">\n            [[site.description]]<br><br>\n        </div>\n    </div>\n\n    <div class=\"row\">\n\n        <div class=\"col-md-3\">\n            <panel>\n                <panel-heading>\n                    Totals\n                </panel-heading>\n                <panel-body>\n                    <table class=\"table table-striped\">\n                        <tbody>\n                            <tr>\n                                <th>Devices</th>\n                                <td>\n                                    <a href=\"/sites/[[site.id]]/devices/\"\n                                       class=\"btn btn-info\">\n                                        [[total_devices]]\n                                    </a>\n                                </td>\n                            </tr>\n                            <tr>\n                                <th>Interfaces</th>\n                                <td>\n                                    <a href=\"/sites/[[site.id]]/interfaces/\"\n                                       class=\"btn btn-info\">\n                                        [[total_interfaces]]\n                                    </a>\n                                </td>\n                            </tr>\n                            <tr>\n                                <th>Networks</th>\n                                <td>\n                                    <a href=\"/sites/[[site.id]]/networks/\"\n                                       class=\"btn btn-info\">\n                                        [[total_networks]]\n                                    </a>\n                                </td>\n                            </tr>\n                            <tr>\n                               <th>- IPv4</th>\n                               <td>\n                                   <a href=\"/sites/[[site.id]]/networks/?ip_version=4\"\n                                      class=\"btn btn-info\">\n                                       [[total_ipv4]] / [[total_networks]]\n                                   </a>\n                               </td>\n                            </tr>\n                            <tr>\n                                <th>- IPv6</th>\n                                <td>\n                                    <a href=\"/sites/[[site.id]]/networks/?ip_version=6\"\n                                       class=\"btn btn-info\">\n                                       [[total_ipv6]] / [[total_networks]]\n                                   </a>\n                                </td>\n                            </tr>\n                         </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n\n        <div class=\"col-md-3\">\n            <panel>\n                <panel-heading>\n                    Network Usage\n                </panel-heading>\n                <panel-body>\n                    <table class=\"table table-striped\">\n                        <tbody>\n                            <tr>\n                                <th class=\"bg-success\">Assigned</th>\n                                <td class=\"bg-success\">\n                                    <a href=\"/sites/[[site.id]]/networks/?state=assigned\"\n                                       class=\"btn btn-success\">\n                                        [[total_assigned]] / [[total_networks]]\n                                    </a>\n                              </td>\n                            </tr>\n                            <tr>\n                                <th class=\"bg-info\">Allocated</th>\n                                <td class=\"bg-info\">\n                                    <a href=\"/sites/[[site.id]]/networks/?state=allocated\"\n                                       class=\"btn btn-info\">\n                                        [[total_allocated]] / [[total_networks]]\n                                    </a>\n                              </td>\n                           </tr>\n                           <tr>\n                                <th class=\"bg-warning\">Reserved</th>\n                                <td class=\"bg-warning\">\n                                    <a href=\"/sites/[[site.id]]/networks/?state=reserved\"\n                                       class=\"btn btn-warning\">\n                                      [[total_reserved]] / [[total_networks]]\n                                    </a>\n                               </td>\n                          </tr>\n                          <tr>\n                                <th class=\"bg-danger\">Orphaned</th>\n                                <td class=\"bg-danger\">\n                                    <a href=\"/sites/[[site.id]]/networks/?state=orphaned\"\n                                       class=\"btn btn-danger\">\n                                      [[total_orphaned]] / [[total_networks]]\n                                    </a>\n                              </td>\n                          </tr>\n                        </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n\n        <div class=\"col-md-6\">\n            <panel>\n                <panel-body>\n                    <canvas\n                        id=\"pie\" class=\"chart chart-pie\"\n                        chart-data=\"data\" chart-labels=\"labels\"\n                    >\n                    </canvas> \n                </panel-body>\n            </panel>\n        </div>                \n\n    </div>\n\n    <div class=\"row\">\n\n        <div class=\"col-sm-12\">\n            <panel>\n                <panel-heading>Recent Changes</panel-heading>\n                <panel-body>\n                    <table class=\"table table-condensed table-hover\">\n                        <thead>\n                            <tr>\n                                <th class=\"col-sm-1\">ID</th>\n                                <th class=\"col-sm-2\">User</th>\n                                <th class=\"col-sm-1\">Event</th>\n                                <th class=\"col-sm-1\">Resource Type</th>\n                                <th class=\"col-sm-1\">Resource ID</th>\n                                <th class=\"col-sm-2\">Change At</th>\n                            </tr>\n                        </thead>\n                        <tbody>\n                            <tr ng-repeat=\"change in changes\">\n                                <td>\n                                    <a ng-href=\"/sites/[[site.id]]/changes/[[change.id]]\">\n                                        [[change.id]]\n                                    </a>\n                                </td>\n                                <td>[[change.user.email]]</td>\n                                <td>[[change.event]]</td>\n                                <td>[[change.resource_name]]</td>\n                                <td>[[change.resource_id]]</td>\n                                <td>[[change.change_at|from_now]]</td>\n                            </tr>\n                        </tbody>\n                    </table>\n                </panel-body>\n            </panel>\n        </div>\n\n    </div>\n\n    <nsot-modal title=\"Update Site\" modal-id=\"updateSiteModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"updateError\" class=\"alert alert-danger\">\n                [[updateError.code]] - [[updateError.message]]\n            </div>\n            <form novalidate name=\"siteForm\" class=\"nsot-form\">\n                <div class=\"form-group\" ng-class=\"{\n                    \'has-error\' : siteForm.name.$invalid,\n                    \'has-success\' : siteForm.name.$valid,\n                }\">\n                    <input type=\"text\"\n                           class=\"form-control\"\n                           name=\"name\"\n                           placeholder=\"Name (required)\"\n                           ng-model=\"site.name\"\n                           ng-minlength=\"1\"\n                           required\n                    >\n                </div>\n                <div class=\"form-group\">\n                    <textarea style=\"resize: vertical;\"\n                              class=\"form-control\"\n                              rows=\"5\"\n                              name=\"description\"\n                              placeholder=\"Description\"\n                              ng-model=\"site.description\"\n                    >\n                    </textarea>\n                </div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"updateSite()\"\n                    class=\"btn btn-primary\" ng-disabled=\"siteForm.$invalid\"\n            >\n                Update\n            </button>\n        </div>\n    </nsot-modal>\n\n    <nsot-modal title=\"Delete Site\" modal-id=\"deleteSiteModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"deleteError\" class=\"alert alert-danger\">\n                [[deleteError.code]] - [[deleteError.message]]\n            </div>\n            Are you sure you want to delete this site?\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"deleteSite()\" class=\"btn btn-primary\">\n                Delete\n            </button>\n        </div>\n \n   </nsot-modal>\n\n</div>\n");
$templateCache.put("sites.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar heading=\"Sites\">\n        <button\n            class=\"btn btn-success\"\n            data-toggle=\"modal\"\n            data-target=\"#createSiteModal\"\n        >Create Site</button>\n    </heading-bar>\n\n    <nsot-modal title=\"Create Site\" modal-id=\"createSiteModal\">\n        <div class=\"modal-body\">\n            <div ng-if=\"error\" class=\"alert alert-danger\">\n                [[error.code]] - [[error.message]]\n            </div>\n            <form novalidate name=\"siteForm\" class=\"nsot-form\">\n                <div class=\"form-group\" ng-class=\"{\n                    \'has-error\' : siteForm.name.$invalid,\n                    \'has-success\' : siteForm.name.$valid,\n                }\">\n                    <input type=\"text\"\n                           class=\"form-control\"\n                           name=\"name\"\n                           placeholder=\"Name (required)\"\n                           ng-model=\"site.name\"\n                           ng-minlength=\"1\"\n                           required\n                    >\n                </div>\n                <div class=\"form-group\">\n                    <textarea style=\"resize: vertical;\"\n                              class=\"form-control\"\n                              rows=\"5\"\n                              name=\"description\"\n                              placeholder=\"Description\"\n                              ng-model=\"site.description\"\n                    >\n                    </textarea>\n                </div>\n            </form>\n        </div>\n        <div class=\"modal-footer\">\n            <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">\n                Close\n            </button>\n            <button type=\"submit\" ng-click=\"createSite()\"\n                    class=\"btn btn-primary\" ng-disabled=\"siteForm.$invalid\"\n            >\n                Create\n            </button>\n        </div>\n    </nsot-modal>\n\n    <div ng-if=\"!sites.length\" class=\"row\"><div class=\"col-sm-6 col-sm-offset-3\">\n        <panel>\n            <panel-heading>Welcome</panel-heading>\n            <panel-body>\n                Welcome to the Network Source of Truth. It looks like you\'re new\n                here. Lets start by creating a <em>site</em> with the button above.\n                This will be a namespace for all of your data.\n            </panel-body>\n        </panel>\n    </div></div>\n    <div class=\"row\" ng-if=\"sites.length\" class=\"row\"><div class=\"col-sm-10 col-sm-offset-1\">\n        <panel>\n            <panel-heading>Sites</panel-heading>\n            <panel-body>\n                <table class=\"table table-condensed table-hover\">\n                    <thead>\n                        <tr>\n                            <th>Name</th>\n                            <th>Description</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n                        <tr ng-repeat=\"site in sites\">\n                            <td class=\"col-sm-3\">\n                                <a ng-href=\"/sites/[[site.id]]\">[[site.name]]</a>\n                            </td>\n                            <td class=\"col-sm-8\">[[site.description]]</td>\n                        </tr>\n                    </tbody>\n                </table>\n            </panel-body>\n        </panel>\n\n    </div></div>\n</div>\n");
$templateCache.put("user.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n    <heading-bar\n        heading=\"Users\"\n        subheading=\"[[profileUser.email]]\">\n    </heading-bar>\n\n    <div class=\"row\"><div class=\"col-sm-6\">\n        <panel>\n            <panel-heading>\n                User\n            </panel-heading>\n            <panel-body>\n                <dl class=\"dl-horizontal\">\n                    <dt>Email</dt>\n                    <dd>[[profileUser.email]]</dd>\n\n                    <span ng-if=\"isSelf\">\n                        <dt>Secret Key</dt>\n                        <dd ng-if=\"!secret_key\">\n                            <a class=\"clicky\" ng-click=\"showKey()\">Click to show key!</a>\n                        </dd>\n                        <dd ng-if=\"secret_key\">\n                            [[secret_key]]\n                            (<a class=\"clicky\" ng-click=\"rotateKey()\">Rotate Key</a>)\n                        </dd>\n                    </span>\n                </dl>\n            </panel-body>\n       </panel>\n    </div></div>\n\n\n</div>\n");
$templateCache.put("users.html","<loading-panel ng-if=\"loading\"></loading-panel>\n<div ng-if=\"!loading\">\n</div>\n");
$templateCache.put("directives/dropdown.html","<div class=\"btn-group\">\n    <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\">\n        <span ng-if=\"ctxtObj.current\">[[ctxtObj.name]]: [[ctxtObj.current]]</span>\n        <span ng-if=\"!ctxtObj.current\">[[ctxtObj.name]]</span>\n        <span class=\"caret\"></span>\n    </button>\n    <ul class=\"dropdown-menu\" role=\"menu\">\n        <li ng-repeat=\"value in ctxtObj.values\">\n            <a ng-href=\"[[ctxtObj.getUrl(value)]]\">[[value]]</a>\n        </li>\n    </ul>\n</div>\n");
$templateCache.put("directives/loading-panel.html","<div class=\"row\"><div class=\"col-sm-6 col-sm-offset-3\">\n    <panel class=\"notification-box\">\n        <panel-heading>Loading...</panel-heading>\n        <panel-body class=\"text-center\">\n            <i class=\"fa fa-spinner fa-spin fa-2x\"></i>\n        </panel-body>\n    </panel>\n</div></div>\n");
$templateCache.put("directives/nsot-modal.html","<div class=\"modal fade\" id=\"[[modalId]]\" tabindex=\"-1\" role=\"dialog\">\n    <div class=\"modal-dialog\" ng-class=\"{\n        \'modal-lg\': modalSize == \'large\',\n        \'modal-sm\': modalSize == \'small\'\n    }\">\n        <div class=\"modal-content\">\n            <div class=\"modal-header\">\n                <button type=\"button\" class=\"close close-light\" data-dismiss=\"modal\">\n                    <span class=\"fa fa-close\"</span>\n                </button>\n                <h4 class=\"modal-title\">[[title]]</h4>\n            </div>\n            <ng-transclude></ng-transclude>\n        </div>\n    </div>\n</div>\n\n");
$templateCache.put("directives/paginator.html","<div ng-if=\"pager.limit\" class=\"btn-group\" style=\"padding-right: 10px;\">\n\n\n    <a ng-disabled=\"!pager.hasFirst()\" class=\"btn btn-default\" ng-href=\"[[pager.firstPageUrl()]]\">\n        <i class=\"fa fa-angle-double-left\"></i>\n    </a>\n\n    <a ng-disabled=\"!pager.hasPrevious()\" class=\"btn btn-default\" ng-href=\"[[pager.previousPageUrl()]]\">\n        <i class=\"fa fa-angle-left\"></i>\n    </a>\n\n    <a class=\"btn btn-default disabled\">Page [[pager.page]] of [[pager.numPages]]</a>\n\n    <a ng-disabled=\"!pager.hasNext()\" class=\"btn btn-default\" ng-href=\"[[pager.nextPageUrl()]]\">\n        <i class=\"fa fa-angle-right\"></i>\n    </a>\n\n    <a ng-disabled=\"!pager.hasLast()\" class=\"btn btn-default\" ng-href=\"[[pager.lastPageUrl()]]\">\n        <i class=\"fa fa-angle-double-right\"></i>\n    </a>\n</div>\n");
$templateCache.put("includes/attributes-form.html","<div class=\"row\">\n    <div class=\"col-md-6\">\n        <div class=\"form-group\" ng-if=\"formMode == \'create\'\" ng-class=\"{\n            \'has-error\' : attrForm.name.$invalid,\n            \'has-success\' : attrForm.name.$valid\n        }\">\n            <label>Name *</label>\n            <input type=\"text\"\n                   class=\"form-control\"\n                   name=\"name\"\n                   ng-model=\"formData.name\"\n                   ng-minlength=\"1\"\n                   required\n            >\n        </div>\n        <span ng-if=\"formMode === \'update\'\">\n            <label>Name</label> [[attribute.name]]\n        <span>\n    </div>\n\n    <div class=\"col-md-6\">\n        <div class=\"form-group\" ng-if=\"formMode == \'create\'\" ng-class=\"{\n            \'has-error\' : attrForm.resourcType.$invalid,\n            \'has-success\' : attrForm.resourceType.$valid\n        }\">\n            <label>Resource Type</label>\n            <select\n                name=\"resourceType\"\n                class=\"form-control\"\n                ng-required\n                ng-init=\"formData.resourceName = \'Network\'\"\n                ng-model=\"formData.resourceName\">\n                <option value=\"Network\">Network</option>\n                <option value=\"Device\">Device</option>\n                <option value=\"Interface\">Interface</option>\n            </select>\n        </div>\n        <span ng-if=\"formMode === \'update\'\">\n            <label>Resource Type</label> [[attribute.resource_name]]\n        <span>\n    </div>\n</div>\n<div class=\"form-group\">\n    <label>Description</label>\n    <textarea style=\"resize: vertical;\"\n              class=\"form-control\"\n              rows=\"5\"\n              ng-model=\"formData.description\"\n    >\n    </textarea>\n</div>\n<h4 class=\"form-subheading\">Constraints</h4>\n<div class=\"form-group\">\n    <label>Valid Values</label>\n    <tags-input\n        placeholder=\"Add Value\"\n        name=\"validValues\"\n        min-length=\"1\"\n        ng-model=\"formData.validValues\"\n    ></tags-input>\n</div>\n<div class=\"form-group\">\n    <label>Value Pattern</label>\n    <input type=\"text\"\n           class=\"form-control\"\n           name=\"pattern\"\n           ng-model=\"formData.pattern\"\n    >\n</div>\n<label class=\"checkbox-inline\">\n    <input type=\"checkbox\" name=\"required\"\n            ng-model=\"formData.required\"> Required\n</label>\n<label class=\"checkbox-inline\">\n    <input type=\"checkbox\" name=\"display\"\n            ng-model=\"formData.display\"> Display\n</label>\n<label class=\"checkbox-inline\">\n    <input type=\"checkbox\" name=\"multi\"\n            ng-model=\"formData.multi\"> Allow Multi Values\n</label>\n<label class=\"checkbox-inline\">\n    <input type=\"checkbox\" name=\"allowEmpty\"\n            ng-model=\"formData.allowEmpty\"> Allow Empty Values\n</label>\n");
$templateCache.put("includes/devices-form.html","<div class=\"form-group\" ng-class=\"{\n    \'has-error\' : deviceForm.hostname.$invalid,\n    \'has-success\' : deviceForm.hostname.$valid,\n}\">\n    <input type=\"text\"\n           class=\"form-control\"\n           name=\"hostname\"\n           placeholder=\"Hostname (required)\"\n           ng-model=\"formData.hostname\"\n           ng-minlength=\"1\"\n           required\n    >\n</div>\n\n<h4 class=\"form-subheading\">Attributes</h4>\n\n<div class=\"row\" ng-repeat=\"attr in formData.attributes\">\n\n    <div ng-if=\"attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select name=\"attribute\" class=\"form-control\" disabled>\n            <option>[[attr.name]]</option>\n        </select>\n    </div>\n    <div ng-if=\"!attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select\n            name=\"attribute\"\n            class=\"form-control\"\n            required\n            ng-change=\"formData.attributes[$index].value = undefined\"\n            ng-model=\"formData.attributes[$index].name\">\n            <option value=\"\" disabled selected></option>\n            <option value=\"[[val.name]]\"\n                    ng-selected=\"[[\n                        formData.attributes[$parent.$index].name == val.name\n                    ]]\"\n                    ng-repeat=\"(idx, val) in attributes\n                               |filter:{required:false}\">\n                [[val.name]]\n            </option>\n        </select>\n    </div>\n\n    <div class=\"col-sm-7\" style=\"padding-left: 0px;\">\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : deviceForm[\'value_\' + $index].$invalid,\n            \'has-success\' : deviceForm[\'value_\' + $index].$valid,\n        }\">\n            <input ng-if=\"!attributesByName[attr.name].multi\"\n                   type=\"text\"\n                   class=\"form-control\"\n                   name=\"value_[[$index]]\"\n                   placeholder=\"Value\"\n                   ng-model=\"formData.attributes[$index].value\"\n                   ng-required=\"!attributesByName[attr.name].constraints.allow_empty\"\n            >\n            <tags-input ng-if=\"attributesByName[attr.name].multi\"\n                        name=\"value_[[$index]]\"\n                        ng-model=\"formData.attributes[$index].value\"\n                        placeholder=\"Add multiple values\"\n                        min-length=\"1\"\n            ></tags-input>\n        </div>\n    </div>\n\n    <div class=\"col-sm-1 text-center\">\n        <span ng-if=\"!attributesByName[attr.name].required\" class=\"attr-buttons\">\n            <span class=\"fa fa-lg fa-minus-circle rm-attr-btn\"\n                  ng-click=\"removeAttr($index);\"\n            ></span>\n        </span>\n    </div>\n</div>\n\n<div class=\"row\">\n    <div class=\"col-sm-12 text-right\">\n        <a ng-click=\"addAttr()\" class=\"add-attr-btn\">\n            Add an attribute\n            <i class=\"fa fa-lg fa-plus-circle add-attr-btn\"></i>\n        </a>\n    </div>\n</div>\n\n");
$templateCache.put("includes/interfaces-form.html","<div class=\"row\">\n    <div class=\"col-md-6\">\n        <div class=\"form-group\" ng-if=\"formMode === \'create\'\" ng-class=\"{\n            \'has-error\' : interfaceForm.device.$invalid,\n            \'has-success\' : interfaceForm.device.$valid,\n        }\">\n            <label>Device *</label>\n            <select\n                class=\"form-control\"\n                name=\"device\"\n                ng-required\n                ng-model=\"formData.device\"\n            >\n                <option value=\"\" selected disabled>\n                    Select a device (required)\n                </option>\n                <option\n                    ng-repeat=\"dev in formData.devices\"\n                    value=\"[[dev.id]]\">\n                    [[dev.hostname]]\n                </option>\n            </select>\n        </div>\n        <div class=\"form-group\" ng-if=\"formMode === \'update\'\">\n            <label>Device</label>\n            <input type=\"text\" \n                   class=\"form-control\"\n                   readonly\n                   value=\"[[iface.device]]\"\n            >\n        </div>\n    </div>\n\n    <div class=\"col-md-6\">\n\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : interfaceForm.name.$invalid,\n            \'has-success\' : interfaceForm.name.$valid,\n        }\">\n            <label>Name *</label>\n            <input type=\"text\"\n                   class=\"form-control\"\n                   name=\"name\"\n                   placeholder=\"Name (required)\"\n                   ng-model=\"formData.name\"\n                   ng-minlength=\"1\"\n                   required\n            >\n        </div>\n    </div>\n</div>\n\n<div class=\"row\">\n    <div class=\"col-md-6\">\n\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : interfaceForm.mac_address.$invalid,\n            \'has-success\' : interfaceForm.mac_address.$valid,\n        }\">\n            <label>MAC Address</label>\n            <input type=\"text\"\n                   class=\"form-control\"\n                   name=\"mac_address\"\n                   placeholder=\"(Default: 00:00:00:00:00:00)\"\n                   ng-model=\"formData.mac_address\"\n            >\n        </div>\n    </div>\n\n    <div class=\"col-md-6\">\n\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : interfaceForm.speed.$invalid,\n            \'has-success\' : interfaceForm.speed.$valid,\n        }\">\n            <label>Speed</label>\n            <input type=\"text\"\n                   class=\"form-control\"\n                   name=\"speed\"\n                   placeholder=\"Speed in Mbps (Default: 1000)\"\n                   ng-model=\"formData.speed\"\n                   ng-minlength=\"1\"\n            >\n        </div>\n    </div>\n</div>\n\n<div class=\"row\">\n    <div class=\"col-md-12\">\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : interfaceForm.description.$invalid,\n            \'has-success\' : interfaceForm.description.$valid,\n        }\">\n            <label>Description</label>\n            <input type=\"text\"\n                   class=\"form-control\"\n                   name=\"description\"\n                   placeholder=\"Something short and sweet (optional)\"\n                   ng-model=\"formData.description\"\n            >\n        </div>\n    </div>\n</div>\n\n<h4 class=\"form-subheading\">Attributes</h4>\n\n<div class=\"row\" ng-repeat=\"attr in formData.attributes\">\n\n    <div ng-if=\"attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select name=\"attribute\" class=\"form-control\" disabled>\n            <option>[[attr.name]]</option>\n        </select>\n    </div>\n    <div ng-if=\"!attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select\n            name=\"attribute\"\n            class=\"form-control\"\n            required\n            ng-change=\"formData.attributes[$index].value = undefined\"\n            ng-model=\"formData.attributes[$index].name\">\n            <option value=\"\" disabled selected></option>\n            <option value=\"[[val.name]]\"\n                    ng-selected=\"[[\n                        formData.attributes[$parent.$index].name == val.name\n                    ]]\"\n                    ng-repeat=\"(idx, val) in attributes\n                               |filter:{required:false}\">\n                [[val.name]]\n            </option>\n        </select>\n    </div>\n\n    <div class=\"col-sm-7\" style=\"padding-left: 0px;\">\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : interfaceForm[\'value_\' + $index].$invalid,\n            \'has-success\' : interfaceForm[\'value_\' + $index].$valid,\n        }\">\n            <input ng-if=\"!attributesByName[attr.name].multi\"\n                   type=\"text\"\n                   class=\"form-control\"\n                   name=\"value_[[$index]]\"\n                   placeholder=\"Value\"\n                   ng-model=\"formData.attributes[$index].value\"\n                   ng-required=\"!attributesByName[attr.name].constraints.allow_empty\"\n            >\n            <tags-input ng-if=\"attributesByName[attr.name].multi\"\n                        name=\"value_[[$index]]\"\n                        ng-model=\"formData.attributes[$index].value\"\n                        placeholder=\"Add multiple values\"\n                        min-length=\"1\"\n            ></tags-input>\n        </div>\n    </div>\n\n    <div class=\"col-sm-1 text-center\">\n        <span ng-if=\"!attributesByName[attr.name].required\" class=\"attr-buttons\">\n            <span class=\"fa fa-lg fa-minus-circle rm-attr-btn\"\n                  ng-click=\"removeAttr($index);\"\n            ></span>\n        </span>\n    </div>\n</div>\n\n<div class=\"row\">\n    <div class=\"col-sm-12 text-right\">\n        <a ng-click=\"addAttr()\" class=\"add-attr-btn\">\n            Add an attribute\n            <i class=\"fa fa-lg fa-plus-circle add-attr-btn\"></i>\n        </a>\n    </div>\n</div>\n\n");
$templateCache.put("includes/networks-form.html","<div class=\"form-group\" ng-class=\"{\n    \'has-error\' : networkForm.cidr.$invalid,\n    \'has-success\' : networkForm.cidr.$valid,\n}\">\n    <input type=\"text\"\n           class=\"form-control\"\n           name=\"cidr\"\n           placeholder=\"Network (required)\"\n           ng-if=\"formMode === \'create\'\"\n           ng-model=\"formData.cidr\"\n           ng-minlength=\"1\"\n           required\n    >\n    <span ng-if=\"formMode === \'update\'\">\n        <label>cidr</label> [[network.network_address]]/[[network.prefix_length]]\n    <span>\n</div>\n\n<h4 class=\"form-subheading\">Attributes</h4>\n\n<div class=\"row\" ng-repeat=\"attr in formData.attributes\">\n\n    <div ng-if=\"attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select name=\"attribute\" class=\"form-control\" disabled>\n            <option>[[attr.name]]</option>\n        </select>\n    </div>\n    <div ng-if=\"!attributesByName[attr.name].required\" class=\"col-sm-4\">\n        <select\n            name=\"attribute\"\n            class=\"form-control\"\n            required\n            ng-change=\"formData.attributes[$index].value = undefined\"\n            ng-model=\"formData.attributes[$index].name\">\n            <option value=\"\" disabled selected></option>\n            <option value=\"[[val.name]]\"\n                    ng-selected=\"[[\n                        formData.attributes[$parent.$index].name == val.name\n                    ]]\"\n                    ng-repeat=\"(idx, val) in attributes\n                               |filter:{required:false}\">\n                [[val.name]]\n            </option>\n        </select>\n    </div>\n\n    <div class=\"col-sm-7\" style=\"padding-left: 0px;\">\n        <div class=\"form-group\" ng-class=\"{\n            \'has-error\' : networkForm[\'value_\' + $index].$invalid,\n            \'has-success\' : networkForm[\'value_\' + $index].$valid,\n        }\">\n            <input ng-if=\"!attributesByName[attr.name].multi\"\n                   type=\"text\"\n                   class=\"form-control\"\n                   name=\"value_[[$index]]\"\n                   placeholder=\"Value\"\n                   ng-model=\"formData.attributes[$index].value\"\n                   ng-required=\"!attributesByName[attr.name].constraints.allow_empty\"\n            >\n            <tags-input ng-if=\"attributesByName[attr.name].multi\"\n                        name=\"value_[[$index]]\"\n                        ng-model=\"formData.attributes[$index].value\"\n                        placeholder=\"Add multiple values\"\n                        min-length=\"1\"\n            ></tags-input>\n        </div>\n    </div>\n\n    <div class=\"col-sm-1 text-center\">\n        <span ng-if=\"!attributesByName[attr.name].required\" class=\"attr-buttons\">\n            <span class=\"fa fa-lg fa-minus-circle rm-attr-btn\"\n                  ng-click=\"removeAttr($index);\"\n            ></span>\n        </span>\n    </div>\n</div>\n\n<div class=\"row\">\n    <div class=\"col-sm-12 text-right\">\n        <a ng-click=\"addAttr()\" class=\"add-attr-btn\">\n            Add an attribute\n            <i class=\"fa fa-lg fa-plus-circle add-attr-btn\"></i>\n        </a>\n    </div>\n</div>\n\n");}]);