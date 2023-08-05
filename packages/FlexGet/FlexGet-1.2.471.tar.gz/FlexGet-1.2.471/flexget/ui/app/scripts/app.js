'use strict';

String.prototype.startsWith = function (prefix) {
    return this.indexOf(prefix) === 0;
};

function registerPlugin(plugin) {
    angular.module('flexget').requires.push(plugin.name);
}
(function () {
    'use strict';

    angular
        .module('flexget', [
            'ui.router',
            'ngMaterial',
            'ngCookies',
            'angular-loading-bar',
            'flexget.components',
            'flexget.directives',
            'flexget.services'
        ]);

    function bootstrapApplication() {
        /* Bootstrap app after page has loaded which allows plugins to register */
        angular.element(document).ready(function () {
            angular.bootstrap(document, ['flexget']);
        });
        window.loading_screen.finish();
    }

    bootstrapApplication();
})();
(function () {
    'use strict';

    angular
        .module('flexget.components', []);

})();

(function () {
  'use strict';

  angular
    .module('flexget.components')
    .component('seenFields',{
      templateUrl: 'components/seen/seen-fields/seen-fields.tmpl.html',
      controllerAs: 'vm',
      controller: seenFieldsController,
      bindings: {
        fields: '<',
      },
    });

  function seenFieldsController() {
  }
})();

(function () {
  'use strict';

  angular
    .module('flexget.components')
    .component('seenEntry',{
      templateUrl: 'components/seen/seen-entry/seen-entry.tmpl.html',
      controllerAs: 'vm',
      controller: seenEntryController,
      bindings: {
        entry: '<',
      },
    });

  function seenEntryController() {
  }
})();

(function () {
    'use strict';

    tasksService.$inject = ["$rootScope", "$http", "$q"];
    angular.module('flexget.components')
        .service('tasks', tasksService);

    function tasksService($rootScope, $http, $q) {
        // List tasks
        this.list = function () {
            return $http.get('/api/tasks/')
                .then(
                    function (response) {
                        var tasks = [];
                        angular.forEach(response.data.tasks, function (task) {
                            this.push(task.name);
                        }, tasks);
                        return tasks
                    },
                    function (httpError) {
                        throw httpError.status + " : " + httpError.data;
                    });
        };

        // Execute task(s), return stream log etc
        this.execute = function (task_name, options) {
            var deferred = $q.defer();

            var params = '';

            angular.forEach(options, function (value, key) {
                var option = key + '=' + value;
                if (params) {
                    params = params + '&' + option
                } else {
                    params = '?' + option
                }
            });

            var on = function (event, pattern, callback) {
                var wrappedCallback = function () {
                    var args = arguments;

                    return $rootScope.$evalAsync(function () {
                        return callback.apply(stream, args);
                    });
                };

                if (pattern) {
                    stream.on(event, pattern, wrappedCallback);
                } else {
                    stream.on(event, wrappedCallback)
                }
            };

            var stream = oboe({
                url: '/api/tasks/' + task_name + '/execute/' + params,
                method: 'GET'
            }).done(function () {
                deferred.resolve("finished stream");
            }).fail(function (error) {
                deferred.reject(error)
            });

            deferred.promise.log = function (callback) {
                on('node', 'log', callback);
                return deferred.promise;
            };

            deferred.promise.progress = function (callback) {
                on('node', 'progress', callback);
                return deferred.promise;
            };

            deferred.promise.summary = function (callback) {
                on('node', 'summary', callback);
                return deferred.promise;
            };

            deferred.promise.entry_dump = function (callback) {
                on('node', 'entry_dump', callback);
                return deferred.promise;
            };

            deferred.promise.abort = function () {
                return stream.abort();
            };

            return deferred.promise;
        };

        this.queue = function () {
            var defer = $q.defer();

            $http.get('/api/tasks/queue/', {ignoreLoadingBar: true}).then(function (response) {
                defer.resolve(response.data.tasks);
            }, function (response) {
                defer.reject(response);
            });

            return defer.promise;
        };

        // Update task config
        this.update = function () {

        };

        // add task
        this.add = function () {

        };

        // Delete task
        this.delete = function () {

        }
    }
})();
(function() {
    'use strict';

    angular
        .module('flexget.services', [
        ]);
})();
(function () {
    'use strict';

    serverService.$inject = ["$http"];
    angular.module('flexget.services')
        .service('server', serverService);

    function serverService($http) {
        this.reload = function () {
            return $http.get('/api/server/reload/');
        };

        this.shutdown = function () {
            return $http.get('/api/server/shutdown/')
        };
    }

})();



(function () {
    'use strict';

    serverConfig.$inject = ["toolBar", "server", "$mdDialog"];
    angular.module('flexget.services')
        .run(serverConfig);

    function serverConfig(toolBar, server, $mdDialog) {

        var reload = function () {
            var reloadController = function ($mdDialog) {
                var vm = this;

                vm.title = 'Reload Config';
                vm.showCircular = true;
                vm.content = null;
                vm.buttons = [];
                vm.ok = null;

                vm.hide = function () {
                    $mdDialog.hide();
                };

                var done = function (text) {
                    vm.showCircular = false;
                    vm.content = text;
                    vm.ok = 'Close';
                };

                server.reload()
                    .success(function () {
                        done('Reload Success');
                    })
                    . error(function (data, status, headers, config) {
                        done('Reload failed: ' + data.error);
                    });
            };
            reloadController.$inject = ["$mdDialog"];

            $mdDialog.show({
                templateUrl: 'services/modal/modal.dialog.circular.tmpl.html',
                parent: angular.element(document.body),
                controllerAs: 'vm',
                controller: reloadController
            });
        };

        var doShutdown = function () {
            window.stop(); // Kill any http connection

            var shutdownController = function ($mdDialog) {
                var vm = this;

                vm.title = 'Shutting Down';
                vm.showCircular = true;
                vm.content = null;
                vm.buttons = [];
                vm.ok = null;

                vm.hide = function () {
                    $mdDialog.hide();
                };

                var done = function (text) {
                    vm.title = 'Shutdown';
                    vm.showCircular = false;
                    vm.content = text;
                    vm.ok = 'Close';
                };

                server.shutdown().
                success(function () {
                    done('Flexget has been shutdown');
                }).
                error(function (error) {
                    done('Flexget failed to shutdown failed: ' + error.message);
                });
            };
            shutdownController.$inject = ["$mdDialog"];
            $mdDialog.show({
                templateUrl: 'services/modal/modal.dialog.circular.tmpl.html',
                parent: angular.element(document.body),
                controllerAs: 'vm',
                controller: shutdownController
            });

        };

        var shutdown = function () {
            $mdDialog.show(
                $mdDialog.confirm()
                    .parent(angular.element(document.body))
                    .title('Shutdown')
                    .content('Are you sure you want to shutdown Flexget?')
                    .ok('Shutdown')
                    .cancel('Cancel')
            ).then(function () {
                doShutdown();
            });

        };

        toolBar.registerMenuItem('Manage', 'Reload', 'fa fa-refresh', reload);
        toolBar.registerMenuItem('Manage', 'Shutdown', 'fa fa-power-off', shutdown);

    }

})();

(function () {
    'use strict';

    modalService.$inject = ["$modal"];
    angular.module('flexget.services')
        .service('modal', modalService);

    function modalService($modal) {

        var defaultOptions = {
            backdrop: true,
            keyboard: true,
            modalFade: true,
            size: 'md',
            templateUrl: 'services/modal/modal.tmpl.html',
            headerText: 'Proceed?',
            bodyText: 'Perform this action?',
            okText: 'Ok',
            okType: 'primary',
            closeText: 'Cancel',
            closeType: 'default'
        };

        this.showModal = function (options) {
            //Create temp objects to work with since we're in a singleton service
            var tempOptions = {};
            angular.extend(tempOptions, defaultOptions, options);

            if (!tempOptions.controller) {
                tempOptions.controller = function ($modalInstance) {
                    vm = this;

                    vm.modalOptions = tempOptions;

                    vm.ok = function (result) {
                        $modalInstance.close(result);
                    };
                    vm.close = function (result) {
                        $modalInstance.dismiss('cancel');
                    };
                }
            }

            tempOptions.controllerAs = 'vm';

            return $modal.open(tempOptions).result;
        };

    }

})();
(function () {
    'use strict';

    var seriesModule = angular.module('flexget.plugins.series', []);
    registerPlugin(seriesModule);

    seriesModule.run(["$state", "route", "sideNav", "toolBar", function ($state, route, sideNav, toolBar) {
        route.register('series', '/series', 'seriesController', 'plugins/series/series.tmpl.html');
        route.register('episodes', '/series/:id/episodes', 'episodesController', 'plugins/series/series.episodes.tmpl.html');

        sideNav.register('/series', 'Series', 'fa fa-tv', 128);
    }]);

})();
(function () {
    'use strict';

    episodesController.$inject = ["$http", "$stateParams", "$mdDialog"];
    angular.module('flexget.plugins.series')
        .controller('episodesController', episodesController);

    function episodesController($http, $stateParams, $mdDialog) {
        var vm = this;

        var show = "";

        $http.get('/api/series/' + $stateParams.id + '/episodes')
            .success(function(data) {
                vm.episodes = data.episodes;

                show = data.show;
                loadReleases();
            })
            .error(function(error) {
                console.log(error);
            });

        vm.forgetEpisode = function(episode) {
            var confirm = $mdDialog.confirm()
                .title('Confirm forgetting episode.')
                .htmlContent("Are you sure you want to forget episode <b>" + episode.episode_identifier + "</b> from show " + show + "?")
                .ok("Forget")
                .cancel("No");

            $mdDialog.show(confirm).then(function() {
                $http.delete('/api/series/' + $stateParams.id + '/episodes/' + episode.episode_id)
                    .success(function(data) {
                        var index = vm.episodes.indexOf(episode);
                        vm.episodes.splice(index, 1);
                    })
                    .error(function(error) {
                        var errorDialog = $mdDialog.alert()
                            .title("Something went wrong")
                            .htmlContent("Oops, something went wrong when trying to forget <b>" + episode.episode_identifier + "</b> from show " + show + ":\n" + error.message)
                            .ok("Ok");

                        $mdDialog.show(errorDialog);
                    })
            });
        }

        function loadReleases() {
            var params = {
                downloaded: 'downloaded'
            }
            vm.episodes.map(function(episode) {
                $http.get('/api/series/' + $stateParams.id + '/episodes/' + episode.episode_id + '/releases', { params: params })
                    .success(function(data) {
                        episode.releases = data.releases;
                    })
                    .error(function(error) {
                        console.log(error);
                    })
            })
        }
    }

})();
(function () {
    'use strict';

    seriesController.$inject = ["$http", "$state", "$mdDialog"];
    angular.module('flexget.plugins.series')
        .controller('seriesController', seriesController);

    function seriesController($http, $state, $mdDialog) {
        var vm = this;

        var options = {
            page: 1,
            page_size: 10,
            in_config: 'all'
        }

        vm.searchTerm = "";

        function getSeriesList() {
            $http.get('/api/series/', { params: options, cache: true })
                .success(function(data) {
                    vm.series = data.shows;

                    //Set vars for pagination
                    vm.currentPage = data.page;
                    vm.totalShows = data.total_number_of_shows;
                    vm.pageSize = data.number_of_shows;

                    //Get metadata for first show
                    // TODO: Update this to load for all
                    // We will have to use caching in the server, maybe even browser as well?
                    getMetadata();
                });
        }

        function getMetadata() {
            vm.series.map(function(show) {
                $http.get('/api/tvmaze/series/' + show.show_name, { cache: true })
                    .success(function(data) {
                        show.metadata = data;
                    })
                    .error(function(error) {
                        console.log(error);
                    });
                return show;
            })
        }

        //Call from the pagination to update the page to the selected page
        vm.updateListPage = function(index) {
            options.page = index;

            getSeriesList();
        }

        vm.search = function() {
            $http.get('/api/series/search/' + vm.searchTerm, { params: options })
                .success(function(data) {
                    vm.series = data.shows;
                });
        }

        vm.gotoEpisodes = function(id) {
            $state.go('flexget.episodes', { id: id });
        };

        vm.forgetSeries = function(show) {
            var confirm = $mdDialog.confirm()
                .title('Confirm forgetting show.')
                .htmlContent("Are you sure you want to completely forget <b>" + show.show_name + "</b>?")
                .ok("Forget")
                .cancel("No");

            $mdDialog.show(confirm).then(function() {
                $http.delete('/api/series/' + show.show_id)
                    .success(function(data) {
                        var index = vm.series.indexOf(show);
                        vm.series.splice(index, 1);
                    })
                    .error(function(error) {
                        var errorDialog = $mdDialog.alert()
                            .title("Something went wrong")
                            .htmlContent("Oops, something went wrong when trying to forget <b>" + show.show_name + "</b>:\n" + error.message)
                            .ok("Ok");

                        $mdDialog.show(errorDialog);
                    })
            });
        }

        //Load initial list of series
        getSeriesList();
    }

})();
(function () {
  'use strict';

  var seenModule = angular.module(
    'flexget.plugins.seen',
    ['schemaForm']
  );

  registerPlugin(seenModule);

  seenModule.run(["route", "sideNav", function run(route, sideNav) {
    route.register('seen', '/seen', 'seenController', 'plugins/seen/seen.tmpl.html');
    sideNav.register('/seen', 'Seen', 'fa fa-eye', 228);
  }]);
})();

(function () {
  'use strict';

  seenController.$inject = ["$http"];
  angular
    .module('flexget.plugins.seen')
    .controller('seenController', seenController);

  function seenController($http) {
    var vm = this;

    vm.title = 'Seen';

    $http.get('/api/seen', {params: {max: 20}})
      .success(function handleSeen(data) {
        vm.entries = data.seen_entries;
      })
      .error(function handlerSeenError(data) {
        // log error
      });
  }
})();

(function () {
    'use strict';

    var scheduleModule = angular.module('flexget.plugins.schedule', ['schemaForm']);
    registerPlugin(scheduleModule);

    scheduleModule.run(["route", "sideNav", function (route, sideNav) {
        route.register('schedule', '/schedule', 'scheduleController', 'plugins/schedule/schedule.tmpl.html');
        sideNav.register('/schedule', 'Schedule', 'fa fa-calendar', 128);
    }]);

})();
(function () {
    'use strict';

    scheduleController.$inject = ["$http"];
    angular.module('flexget.plugins.schedule')
        .controller('scheduleController', scheduleController);

    function scheduleController($http) {
        var vm = this;

        vm.title = 'Schedules';
        vm.description = 'Task execution';

        vm.form = [
            '*',
            {
                type: 'submit',
                title: 'Save'
            }
        ];

        vm.onSubmit = function (form) {
            // First we broadcast an event so all fields validate themselves
            vm.$broadcast('schemaFormValidate');

            // Then we check if the form is valid
            if (form.$valid) {
                alert('test');
                // ... do whatever you need to do with your data.
            }
        };

        $http.get('/api/schema/config/schedules').
        success(function (data, status, headers, config) {
            // schema-form doesn't allow forms with an array at root level
            vm.schema = {type: 'object', 'properties': {'schedules': data}, required: ['schedules']};
        }).
        error(function (data, status, headers, config) {
            // log error
        });
        $http.get('/api/schedules').
        success(function (data, status, headers, config) {
            vm.models = [data];
        }).
        error(function (data, status, headers, config) {
            // log error
        });
    }

})();
(function () {
    'use strict';

    var logModule = angular.module('flexget.plugins.log', ['ui.grid', 'ui.grid.autoResize', 'ui.grid.autoScroll']);
    registerPlugin(logModule);

    logModule.run(["$state", "route", "sideNav", "toolBar", function ($state, route, sideNav, toolBar) {
        route.register('log', '/log', 'logController', 'plugins/log/log.tmpl.html');
        sideNav.register('/log', 'Log', 'fa fa-file-text-o', 128);
        toolBar.registerButton('Log', 'fa fa-file-text-o', function () {
            $state.go('flexget.log')
        });
    }]);

})();
(function () {
    'use strict';

    logController.$inject = ["$scope"];
    angular.module('flexget.plugins.log')
        .controller('logController', logController);

    function logController($scope) {
        var vm = this;

        vm.logStream = false;

        vm.status = 'Connecting';

        vm.filter = {
            lines: 400,
            search: ''
        };

        vm.refreshOpts = {
            debounce: 1000
        };

        vm.toggle = function () {
            if (vm.status == 'Disconnected') {
                vm.refresh();
            } else {
                vm.stop();
            }
        };

        vm.stop = function () {
            if (typeof vm.logStream !== 'undefined' && vm.logStream) {
                vm.logStream.abort();
                vm.logStream = false;
                vm.status = "Disconnected";
            }

        };

        vm.refresh = function () {
            // Disconnect existing log streams
            vm.stop();

            vm.status = "Connecting";
            vm.gridOptions.data = [];

            var queryParams = '?lines=' + vm.filter.lines;
            if (vm.filter.search) {
                queryParams = queryParams + '&search=' + vm.filter.search;
            }

            vm.logStream = oboe({url: '/api/server/log/' + queryParams})
                .start(function () {
                    $scope.$applyAsync(function () {
                        vm.status = "Streaming";
                    });
                })
                .node('{message}', function (node) {
                    $scope.$applyAsync(function () {
                        vm.gridOptions.data.push(node);
                    });
                })
                .fail(function (test) {
                    $scope.$applyAsync(function () {
                        vm.status = "Disconnected";
                    });
                })
        };

        var rowTemplate = '<div class="{{ row.entity.log_level | lowercase }}"' +
            'ng-class="{summary: row.entity.message.startsWith(\'Summary\'), accepted: row.entity.message.startsWith(\'ACCEPTED\')}"><div ' +
            'ng-repeat="(colRenderIndex, col) in colContainer.renderedColumns track by col.uid" ' +
            'class="ui-grid-cell" ' +
            'ng-class="{ \'ui-grid-row-header-cell\': col.isRowHeader }"  ui-grid-cell>' +
            '</div></div>';

        vm.gridOptions = {
            data: [],
            enableSorting: true,
            rowHeight: 20,
            columnDefs: [
                {field: 'timestamp', name: 'Time', cellFilter: 'date', enableSorting: true, width: 120},
                {field: 'log_level', name: 'Level', enableSorting: false, width: 65},
                {field: 'plugin', name: 'Plugin', enableSorting: false, width: 80, cellTooltip: true},
                {field: 'task', name: 'Task', enableSorting: false, width: 65, cellTooltip: true},
                {field: 'message', name: 'Message', enableSorting: false, minWidth: 400, cellTooltip: true}
            ],
            rowTemplate: rowTemplate,
            onRegisterApi: function (gridApi) {
                vm.gridApi = gridApi;
                vm.refresh();
            }
        };

        // Cancel timer and stop the stream when navigating away
        $scope.$on("$destroy", function () {
            vm.stop();
        });
    }

})
();
(function () {
    'use strict';

    var historyModule = angular.module("flexget.plugins.history", ['angular.filter']);

    registerPlugin(historyModule);

    historyModule.run(["route", "sideNav", function (route, sideNav) {
        route.register('history', '/history', 'historyController', 'plugins/history/history.tmpl.html');
        sideNav.register('/history', 'History', 'fa fa-history', 128);
    }]);

})();
(function () {
    'use strict';
    historyController.$inject = ["$http"];
    angular.module("flexget.plugins.history")
        .controller('historyController', historyController);

    function historyController($http) {
        var vm = this;

        vm.title = 'History';
        $http.get('/api/history').
        success(function (data) {
            vm.entries = data['entries'];
        }).
        error(function (data, status, headers, config) {
            // log error
        });
    }

})();

(function () {
    'use strict';

    var executeModule = angular.module("flexget.plugins.execute", ['ui.grid', 'ui.grid.autoResize', 'angular-spinkit']);

    registerPlugin(executeModule);

    executeModule.run(["route", "sideNav", function (route, sideNav) {
        route.register('execute', '/execute', 'executeController', 'plugins/execute/execute.tmpl.html');
        sideNav.register('/execute', 'Execute', 'fa fa-cog', 128);
    }]);

})();
(function () {
    'use strict';

    angular.module('flexget.plugins.execute')
        .filter('executePhaseFilter', executePhaseFilter);

    function executePhaseFilter() {
        var phaseDescriptions = {
            input: "Gathering Entries",
            metainfo: "Figuring out meta data",
            filter: "Filtering Entries",
            download: "Downloading Accepted Entries",
            modify: "Modifying Entries",
            output: "Executing Outputs",
            exit: "Finished"
        };

        return function (phase) {
            if (phase in phaseDescriptions) {
                return phaseDescriptions[phase]
            } else {
                return "Processing"
            }
        };
    }

})();
(function () {
    'use strict';

    executeController.$inject = ["$scope", "$interval", "$q", "tasks"];
    angular.module('flexget.plugins.execute')
        .controller('executeController', executeController);

    function executeController($scope, $interval, $q, tasks) {
        var vm = this,
            allTasks = [];

        vm.stream = {running: false, tasks: []};
        vm.options = {
            isOpen: false,
            settings: {
                log: true,
                entry_dump: true,
                progress: true,
                summary: true,
                now: true
            },
            optional: [
                {name: 'test', value: false, help: '......', display: 'Test Mode'},
                {name: 'no-cache', value: false, help: 'disable caches. works only in plugins that have explicit support', display: 'Caching'},
                {name: 'stop-waiting', value: null, help: 'matches are not downloaded but will be skipped in the future', display: 'Waiting'},
                {name: 'learn', value: null, help: 'matches are not downloaded but will be skipped in the future', display: 'Learn'},
                {name: 'disable-tracking', value: null, help: 'disable episode advancement for this run', display: 'Tracking'},
                {name: 'discover-now', value: null, help: 'immediately try to discover everything', display: 'Discover'}
            ],
            toggle: function(option) {
                option.value = !option.value;
            }
        };

        // Get a list of tasks for auto complete
        tasks.list()
            .then(function (tasks) {
                allTasks = tasks;
            });

        vm.addTask = function (chip) {
            var chipLower = chip.toLowerCase();

            function alreadyAdded(newChip) {
                for (var i = 0; i < vm.tasksInput.tasks.length; i++) {
                    if (newChip.toLowerCase() == vm.tasksInput.tasks[i].toLowerCase()) {
                        return true
                    }
                }
                return false;
            }

            if (chip.indexOf('*') > -1) {
                for (var i = 0; i < allTasks.length; i++) {
                    var match = new RegExp("^" + chip.replace("*", ".*") + "$", 'i').test(allTasks[i]);
                    if (match && !alreadyAdded(allTasks[i])) {
                        vm.tasksInput.tasks.push(allTasks[i]);
                    }
                }
                return null;
            }

            for (var i = 0; i < allTasks.length; i++) {
                if (chipLower == allTasks[i].toLowerCase() && !alreadyAdded(allTasks[i])) {
                    return chip;
                }
            }
            return null;
        };
        // Used for input form to select tasks to execute
        vm.tasksInput = {
            tasks: [],
            search: [],
            query: function (query) {
                var filter = function () {
                    var lowercaseQuery = angular.lowercase(query);
                    return function filterFn(task) {
                        return (angular.lowercase(task).indexOf(lowercaseQuery) > -1);
                    };
                };
                return query ? allTasks.filter(filter()) : [];
            }
        };

        vm.clear = function () {
            vm.stream.tasks = [];
            vm.stream.running = false;
            vm.options.tasks = [];
        };

        vm.execute = function () {
            vm.stream.running = true;
            vm.stream.tasks = [];

            angular.forEach(vm.tasksInput.tasks, function (task) {
                vm.stream.tasks.push({
                    status: 'pending',
                    name: task,
                    entries: [],
                    percent: 0
                });
            });

            var updateProgress = function () {
                var totalPercent = 0;
                for (var i = 0; i < vm.stream.tasks.length; i++) {
                    totalPercent = totalPercent + vm.stream.tasks[i].percent;
                }
                vm.stream.percent = totalPercent / vm.stream.tasks.length;
            };

            var getTask = function (name) {
                for (var i = 0; i < vm.stream.tasks.length; i++) {
                    var task = vm.stream.tasks[i];
                    if (task.name == name) {
                        return task
                    }
                }
            };

            var streamTask = function (name) {
                var task = getTask(name);

                var options = {};
                angular.copy(vm.options.settings, options);
                angular.forEach(vm.options.optional, function (setting) {
                    //options[setting.name] = setting.value;
                });

                return tasks.execute(name, options)
                    .log(function (log) {
                        task.log.push(log);
                    })
                    .progress(function (update) {
                        angular.extend(task, update);
                        updateProgress();
                    })
                    .summary(function (update) {
                        angular.extend(task, update);
                        updateProgress();
                    })
                    .entry_dump(function (entries) {
                        task.entries = entries;
                    });
            };

            var done = vm.tasksInput.tasks.reduce(function (previous, taskName) {
                return previous.then(function () {
                    if (vm.stream.running) {
                        return streamTask(taskName);
                    }
                });
            }, $q.when());

            done.then(function () {
                vm.stream.running = false;
                vm.stream.percent = 100;
            });


        };

        var getRunning = function () {
            tasks.queue().then(function (tasks) {
                vm.running = tasks
            })
        };
        getRunning();
        var taskInterval = $interval(getRunning, 3000);

        // Cancel timer and stop the stream when navigating away
        $scope.$on("$destroy", function () {
            $interval.cancel(taskInterval);
            if (angular.isDefined(stream)) {
                stream.abort();
            }
        });
    }

})();
(function() {
    'use strict';

    angular
        .module('flexget.directives', [
        ]);
})();
(function () {
    'use strict';

    paletteBackground.$inject = ["flexTheme"];
    angular
        .module('flexget.directives')
        .directive('paletteBackground', paletteBackground);

    /* @ngInject */
    function paletteBackground(flexTheme) {
        var directive = {
            bindToController: true,
            link: link,
            restrict: 'A'
        };
        return directive;

        function link(scope, $element, attrs) {
            var splitColor = attrs.paletteBackground.split(':');
            var color = flexTheme.getPaletteColor(splitColor[0], splitColor[1]);

            if (angular.isDefined(color)) {
                $element.css({
                    'background-color': flexTheme.rgba(color.value),
                    'border-color': flexTheme.rgba(color.value),
                    'color': flexTheme.rgba(color.contrast)
                });
            }
        }
    }
})();
(function() {
  'use strict';

  angular
    .module('flexget.directives')
    .directive('fgMaterialPagination', fgMaterialPagination);

  /* @ngInject */
  function fgMaterialPagination() {
    var directive = {
      restrict: 'E',
      scope: {
        page: '=',
        pageSize: '=',
        total: '=',
        activeClass: '@',
        pagingAction: '&',
      },
      link: pagingLink,
      templateUrl: 'directives/material-pagination/material-pagination.tmpl.html'
    }
    return directive;
  }

  function pagingLink(scope, element, attributes) {
    scope.$watch('page', function(newValue, oldValue) {
      if(newValue && newValue != oldValue) {
        updateButtons(scope, attributes);
      }
    })
  }

  function addRange(start, end, scope) {
    var i = 0;
    for(i = start; i <= end; i++) {
      scope.stepList.push({
        value: i,
        activeClass: scope.page == i ? scope.activeClass : '',
        action: function() {
          internalAction(scope, this.value);
        }
      })
    }
  }

  function internalAction(scope, page) {
    if(scope.page == page) {
      return;
    }

    scope.pagingAction({
      index: page
    });
  }

  function setPrevNext(scope, pageCount, mode) {
    var disabled, item;
    switch(mode) {
      case 'prev':
        disabled = scope.page - 1 <= 0;
        var prevPage = scope.page - 1 <= 0 ? 1 : scope.page - 1;

        item = {
          value: '<',
          disabled: disabled,
          action: function() {
            if(!disabled) {
              internalAction(scope, prevPage);
            }
          }
        }
        break;

      case 'next':
        disabled = scope.page >= pageCount;
        var nextPage = scope.page + 1 >= pageCount ? pageCount : scope.page + 1;

        item = {
          value: '>',
          disabled: disabled,
          action: function() {
            if(!disabled) {
              internalAction(scope, nextPage);
            }
          }
        }
        break;
    }

    if(item) {
      scope.stepList.push(item);
    }
  }

  function updateButtons(scope) {
    var pageCount = Math.ceil(scope.total / scope.pageSize);

    scope.stepList = [];

    var cutOff = 5;

    // Set left navigator
    setPrevNext(scope, pageCount, 'prev');

    if(pageCount <= cutOff) {
      addRange(1, pageCount, scope);
    } else {
      // Check if page is in the first 3
      // Then we don't have to shift the numbers left, otherwise we get 0 and -1 values
      if(scope.page - 2 < 2) {
        addRange(1, 5, scope);

      // Check if page is in the last 3
      // Then we don't have to shift the numbers right, otherwise we get higher values without any results
      } else if(scope.page + 2 > pageCount) {
        addRange(pageCount - 4, pageCount, scope);

      // If page is not in the start of end
      // Then we add 2 numbers to each side of the current page
      } else {
        addRange(scope.page - 2, scope.page + 2, scope);
      }
    }

    // Set right navigator
    setPrevNext(scope, pageCount, 'next');
  }

})();
(function () {
    'use strict';

    userConfig.$inject = ["toolBar"];
    angular.module('flexget.components')
        .run(userConfig);

    function userConfig(toolBar) {
        toolBar.registerMenuItem('Manage', 'Profile', 'fa fa-user', function () {
            alert('not implemented yet')
        }, 100);
    }

})();



(function () {
    'use strict';

    angular.module('flexget.components')
        .factory('toolBar', toolbarService);

    function toolbarService() {
        // Add default Manage (cog) menu
        var items = [
            {type: 'menu', label: 'Manage', cssClass: 'fa fa-cog', items: [], width: 2, order: 255}
        ];

        var defaultOrder = 128;

        var getMenu = function (menu) {
            for (var i = 0, len = items.length; i < len; i++) {
                var item = items[i];
                if (item.type == 'menu' && item.label == menu) {
                    return item;
                }
            }
        };

        return {
            items: items,
            registerButton: function (label, cssClass, action, order) {
                if (!order) {
                    order = defaultOrder;
                }
                items.push({type: 'button', label: label, cssClass: cssClass, action: action, order: order});
            },
            registerMenu: function (label, cssClass, width, order) {
                // Ignore if menu already registered
                var existingMenu = getMenu(label);
                if (!existingMenu) {
                    if (!order) {
                        order = defaultOrder;
                    }
                    if (!width) {
                        width = 2;
                    }
                    items.push({type: 'menu', label: label, cssClass: cssClass, items: [], width: 2, order: order});
                }
            },
            registerMenuItem: function (menu, label, cssClass, action, order) {
                if (!order) {
                    order = defaultOrder;
                }

                menu = getMenu(menu);
                if (menu) {
                    menu.items.push({label: label, cssClass: cssClass, action: action, order: order});
                } else {
                    throw 'Unable to register menu item ' + label + ' as Menu ' + menu + ' was not found';
                }
            }
        }
    }

})();



(function () {
    'use strict';

    toolbarDirective.$inject = ["toolBar"];
    angular.module('flexget.components')
        .directive('toolBar', toolbarDirective);

    function toolbarDirective(toolBar) {
        return {
            restrict: 'E',
            scope: {},
            templateUrl: 'components/toolbar/toolbar.tmpl.html',
            controllerAs: 'vm',
            controller: ["sideNav", function (sideNav) {
                var vm = this;
                vm.toggle = sideNav.toggle;
                vm.toolBarItems = toolBar.items;
            }]
        };
    }

})();
(function () {
    'use strict';

    sideNavService.$inject = ["$rootScope", "$mdSidenav", "$mdMedia"];
    angular.module('flexget.components')
        .factory('sideNav', sideNavService);

    function sideNavService($rootScope, $mdSidenav, $mdMedia) {
        var items = [];

        var toggle = function () {
            if ($mdSidenav('left').isLockedOpen()) {
                $rootScope.menuMini = !$rootScope.menuMini;
            } else {
                $rootScope.menuMini = false;
                $mdSidenav('left').toggle();
            }
        };

        var close = function () {
            if (!$mdMedia('gt-lg')) {
                $mdSidenav('left').close();
            }
        };

        return {
            toggle: toggle,
            close: close,
            register: function (href, caption, icon, order) {
                href = '#' + href;
                items.push({href: href, caption: caption, icon: icon, order: order})
            },
            items: items
        }
    }

})();



(function () {
    'use strict';

    angular.module('flexget.components')
        .directive('sideNav', sideNavDirective);

    function sideNavDirective() {
        return {
            restrict: 'E',
            replace: 'true',
            templateUrl: 'components/sidenav/sidenav.tmpl.html',
            controllerAs: 'vm',
            controller: ["$mdMedia", "sideNav", function ($mdMedia, sideNav) {
                var vm = this;
                vm.toggle = sideNav.toggle;
                vm.navItems = sideNav.items;
            }]
        }
    }

})
();
(function () {
    'use strict';

    var home = angular.module("home", ['angular.filter']);
    registerPlugin(home);

    home.run(["route", function (route) {
        route.register('home', '/home', null, 'components/home/home.tmpl.html');
    }]);
})();
(function () {
    'use strict';

    authService.$inject = ["$state", "$http", "$q"];
    angular.module('flexget.components')
        .factory('authService', authService);

    function authService($state, $http, $q) {
        var loggedIn, prevState, prevParams;

        loggedIn = false;

        return {
            loggedIn: function () {
                var def = $q.defer();

                if (loggedIn) {
                    def.resolve(loggedIn);
                } else {
                    $http.get("/api/server/version/")
                        .success(function () {
                            def.resolve();
                        })
                        .error(function (data) {
                            def.reject()
                        })
                }

                return def.promise;
            },
            login: function (username, password, remember) {
                if (!remember) {
                    remember = false;
                }

                return $http.post('/api/auth/login/?remember=' + remember, {username: username, password: password})
                    .success(function () {
                        loggedIn = true;

                        if (prevState) {
                            $state.go(prevState, prevParams);
                        } else {
                            $state.go('home');
                        }

                    })
            },
            state: function (state, params) {
                if (state.name != 'login') {
                    prevState = state;
                    prevParams = params;
                }
            }
        }
    }

})();
(function () {
    'use strict';

    loginController.$inject = ["$stateParams", "authService"];
    angular.module('flexget.components')
        .controller('LoginController', loginController);

    function loginController($stateParams, authService) {
        var vm = this;

        vm.timeout = $stateParams.timeout;
        vm.remember = false;
        vm.error = '';
        vm.credentials = {
            username: '',
            password: ''
        };

        vm.login = function () {
            authService.login(vm.credentials.username, vm.credentials.password, vm.remember)
                .error(function (data) {
                    vm.credentials.password = '';
                    if ('message' in data) {
                        vm.error = data.message;
                    } else {
                        vm.error = 'Error during authentication';
                    }
                });
        };
    }

})();
(function () {
    'use strict';

    authenticationSetup.$inject = ["$rootScope", "$state", "$http", "toolBar", "authService"];
    authenticationConfig.$inject = ["$httpProvider", "$stateProvider"];
    angular.module('flexget.components')
        .run(authenticationSetup)
        .config(authenticationConfig);

    function authenticationSetup($rootScope, $state, $http, toolBar, authService) {
        $rootScope.$on('event:auth-loginRequired', function (event, timeout) {
            $state.go('login', {'timeout': timeout});
        });

        var logout = function () {
            $http.get('/api/auth/logout/')
                .success(function () {
                    $state.go('login');
                });
        };

        /* Ensure user is authenticated when changing states (pages) unless we are on the login page */
        $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
            if (toState.name == "login") {
                return
            }

            authService.loggedIn()
                .then(function (loggedIn) {
                    // already logged in
                }, function () {
                    // Not logged in
                    event.preventDefault();
                    authService.state(toState, toParams);
                    $rootScope.$broadcast('event:auth-loginRequired', false);
                });
        });

        toolBar.registerMenuItem('Manage', 'Logout', 'fa fa-sign-out', logout, 255);
    }

    function authenticationConfig($httpProvider, $stateProvider) {
        /* Register login page and redirect to page when login is required */
        $stateProvider.state('login', {
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: 'components/authentication/login.tmpl.html'
        });


        /* Intercept 401/403 http return codes and redirect to login page */

        $httpProvider.interceptors.push(['$rootScope', '$q', '$injector', function ($rootScope, $q, $injector) {
            var loginRequired = function () {
                var stateService = $injector.get('$state');
                var authService = $injector.get('authService');
                authService.state(stateService.current, stateService.params);
                $rootScope.$broadcast('event:auth-loginRequired', true);
            };

            return {
                responseError: function (rejection) {
                    if (!rejection.config.ignoreAuthModule) {
                        switch (rejection.status) {
                            case 401:
                                loginRequired();
                                break;
                            case 403:
                                loginRequired();
                                break;
                        }
                    }
                    // otherwise, default behaviour
                    return $q.reject(rejection);
                }
            };
        }]);
    }

})();
(function () {
    'use strict';

    angular
        .module('flexget.plugins', []);

})();
(function () {
    'use strict';

    themesConfig.$inject = ["$mdThemingProvider"];
    flexTheme.$inject = ["$mdThemingProvider"];
    angular
        .module('flexget')
        .config(themesConfig)
        .provider('flexTheme', flexTheme);

    function themesConfig($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('orange', {
                'default': '800'
            })
            .accentPalette('lime')
            .warnPalette('amber');
    }

    function flexTheme($mdThemingProvider) {
        return {
            $get: function() {
                return {
                    getPaletteColor: function(paletteName, hue) {
                        if(angular.isDefined($mdThemingProvider._PALETTES[paletteName]) && angular.isDefined($mdThemingProvider._PALETTES[paletteName][hue])) {
                            return $mdThemingProvider._PALETTES[paletteName][hue];
                        }
                    },
                    rgba: $mdThemingProvider._rgba,
                    palettes: $mdThemingProvider._PALETTES,
                    themes: $mdThemingProvider._THEMES,
                    parseRules: $mdThemingProvider._parseRules
                };
            }
        };
    }

})();
(function () {
    'use strict';

    routeService.$inject = ["$stateProvider", "$urlRouterProvider"];
    routeConfig.$inject = ["$stateProvider"];
    angular.module('flexget')
        .provider('route', routeService)
        .config(routeConfig);

    function routeService($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise(function ($injector) {
            var $state = $injector.get("$state");
            $state.go("flexget.home");
        });

        this.$get = function () {
            return {
                register: function (name, url, controller, template) {
                    $stateProvider.state('flexget.' + name, {
                        url: url,
                        templateUrl: template,
                        controller: controller,
                        controllerAs: 'vm'
                    });
                }
            }
        }
    }

    function routeConfig($stateProvider) {
        $stateProvider
            .state('flexget', {
                abstract: true,
                templateUrl: 'layout.tmpl.html',
            });
    }

})();
angular.module("flexget").run(["$templateCache", function($templateCache) {$templateCache.put("layout.tmpl.html","<div class=\"header md-whiteframe-4dp\" ng-class=\"menuMini ? \'header-mini\': \'header-full\'\"><div class=\"logo\"><a href=\"#/home\"></a></div><tool-bar></tool-bar></div><div layout=\"row\" flex=\"\" ng-class=\"menuMini ? \'nav-menu-mini\': \'nav-menu-full\'\"><side-nav></side-nav><div ui-view=\"\" layout-padding=\"\" flex=\"\" id=\"content\" layout=\"row\"></div></div>");
$templateCache.put("components/authentication/login.tmpl.html","<div class=\"login\" layout=\"column\" layout-padding=\"\"><div class=\"header\"></div><div><form><div layout=\"column\" flex-gt-sm=\"40\" flex-offset-gt-sm=\"30\" flex-gt-md=\"30\" flex-offset-gt-md=\"35\"><p style=\"color: orange\" class=\"text-success text-center\" ng-if=\"vm.timeout == \'true\'\">Your session timed out</p><p style=\"color: red\">{{ vm.error }}</p><md-input-container flex=\"\"><label>Username</label> <input id=\"username\" ng-model=\"vm.credentials.username\"></md-input-container><md-input-container><label>Password</label> <input ng-model=\"vm.credentials.password\" type=\"password\"></md-input-container><div layout=\"column\" layout-align=\"center center\"><md-checkbox md-no-ink=\"\" aria-label=\"Remember Me\" ng-model=\"vm.remember\" class=\"md-primary\">Remember Me</md-checkbox></div><md-button type=\"submit\" class=\"md-raised md-primary\" data-ng-click=\"vm.login()\">Login</md-button></div></form></div></div>");
$templateCache.put("components/home/home.tmpl.html","<md-content layout-xs=\"column\" layout=\"row\" flex=\"\"><div layout=\"column\" flex=\"\" flex-gt-sm=\"50\" flex-offset-gt-sm=\"25\"><md-card><md-card-header palette-background=\"orange:600\"><md-card-header-text><span class=\"md-title\">Flexget Web Interface</span> <span class=\"md-subhead\">Under Development</span></md-card-header-text></md-card-header><md-card-content><p>The interface is not yet ready for end users. Consider this preview only state.</p><p>If you still use it anyways, please do report back to us how well it works, issues, ideas etc..</p><p>We also do really require more man-power to develop webui further. Please join the effort if you know AngularJs or Python!</p><p>There is a functional API with documentation available at <a href=\"/api\">/api</a></p><p><a href=\"http://flexget.com/wiki/Web-UI\">http://flexget.com/wiki/Web-UI</a></p></md-card-content><md-card-actions layout=\"row\" layout-align=\"center center\"><md-button class=\"md-icon-button\" aria-label=\"GitHub\" href=\"http://github.com/Flexget/Flexget\" target=\"_blank\"><md-icon class=\"md-icon fa fa-github\"></md-icon></md-button><md-button class=\"md-icon-button\" aria-label=\"Flexget.com\" href=\"http://flexget.com\" target=\"_blank\"><md-icon class=\"md-icon fa fa-home\"></md-icon></md-button><md-button class=\"md-icon-button\" aria-label=\"Forum\" href=\"http://discuss.flexget.com/\" target=\"_blank\"><md-icon class=\"md-icon fa fa-forumbee\"></md-icon></md-button></md-card-actions></md-card></div></md-content>");
$templateCache.put("components/sidenav/sidenav.tmpl.html","<md-sidenav layout=\"column\" class=\"nav-menu md-sidenav-left md-sidenav-left md-whiteframe-z2\" md-component-id=\"left\" md-is-locked-open=\"$mdMedia(\'gt-sm\')\"><md-content layout=\"column\" flex=\"\"><md-list><md-list-item ng-repeat=\"item in ::vm.navItems\"><md-button href=\"{{ ::item.href }}\" ng-click=\"closeNav()\" flex=\"\"><md-icon class=\"{{ ::item.icon }}\"></md-icon>{{ ::item.caption }}</md-button></md-list-item></md-list></md-content></md-sidenav>");
$templateCache.put("components/toolbar/toolbar.tmpl.html","<div class=\"admin-toolbar\"><md-toolbar class=\"admin-toolbar\"><div class=\"md-toolbar-tools\"><md-button class=\"md-icon-button\" ng-click=\"vm.toggle()\" style=\"width: 40px\"><md-icon class=\"fa fa-bars\" aria-label=\"Menu\"></md-icon></md-button><span flex=\"\"></span><div ng-repeat=\"item in ::vm.toolBarItems | orderBy:\'order\'\"><md-button aria-label=\"{{ item.label }}\" class=\"md-icon-button\" ng-click=\"item.action()\" ng-if=\"::item.type == \'button\'\"><md-tooltip>{{ ::item.label }}</md-tooltip><md-icon md-menu-origin=\"\" class=\"{{ ::item.cssClass }}\"></md-icon></md-button><md-menu ng-if=\"::item.type == \'menu\'\"><md-button aria-label=\"{{ ::item.label }}\" class=\"md-icon-button\" ng-click=\"$mdOpenMenu($event)\"><md-tooltip>{{ ::item.label }}</md-tooltip><md-icon md-menu-origin=\"\" class=\"{{ ::item.cssClass }}\"></md-icon></md-button><md-menu-content width=\"{{ ::item.width }}\"><md-menu-item ng-repeat=\"menuItem in ::item.items | orderBy:\'order\'\"><md-button ng-click=\"menuItem.action()\"><md-icon md-menu-origin=\"\" class=\"{{ ::menuItem.cssClass }}\"></md-icon>{{ ::menuItem.label }}</md-button></md-menu-item></md-menu-content></md-menu></div></div></md-toolbar></div>");
$templateCache.put("directives/material-pagination/material-pagination.tmpl.html","<div layout=\"row\" class=\"fg-material-paging\" layout-align=\"center center\"><md-button class=\"md-raised fg-pagination-button\" ng-repeat=\"step in stepList\" ng-click=\"step.action()\" ng-class=\"step.activeClass\" ng-disabled=\"step.disabled\">{{ step.value }}</md-button></div>");
$templateCache.put("plugins/execute/execute.tmpl.html","<md-content layout=\"column\" layout-padding=\"\" flex=\"\" class=\"execute\" ng-hide=\"vm.stream.tasks.length\"><div layout=\"row\" layout-align=\"center center\"><md-card flex=\"\" flex-gt-sm=\"50\" flex-gt-md=\"40\" class=\"task-search\"><md-card-header><md-card-header-text flex=\"\"><span class=\"md-title\">{{ vm.running.length }} Tasks in Queue</span> <span class=\"md-subhead\" ng-if=\"vm.running[0]\">{{ vm.running[0].name }} ({{ vm.running[0].current_phase }})</span></md-card-header-text><md-menu><md-button class=\"widget-button md-icon-button\" ng-click=\"$mdOpenMenu()\" aria-label=\"open menu\"><md-icon md-font-icon=\"fa fa-ellipsis-v\"></md-icon></md-button><md-menu-content width=\"3\"><md-menu-item ng-repeat=\"option in vm.options.optional\"><md-button ng-click=\"vm.options.toggle(option)\"><md-tooltip>{{ option.help }}</md-tooltip><md-icon ng-class=\"option.value ? \'fa fa-ban\' : \'fa fa-check\'\"></md-icon>{{ option.display }}</md-button></md-menu-item></md-menu-content></md-menu></md-card-header><md-card-content><md-chips ng-model=\"vm.tasksInput.tasks\" md-autocomplete-snap=\"\" md-require-match=\"false\" md-transform-chip=\"vm.addTask($chip)\"><md-autocomplete md-items=\"task in vm.tasksInput.query(vm.tasksInput.search)\" md-item-text=\"task\" placeholder=\"Enter task(s) to execute\" md-selected-item=\"selectedItem\" md-search-text=\"vm.tasksInput.search\"><span md-highlight-text=\"vm.tasksInput.search\">{{ task }}</span></md-autocomplete></md-chips><div flex=\"\"></div><div layout=\"row\" layout-align=\"center center\"><div flex=\"100\" flex-gt-md=\"50\" layout=\"column\"><md-button class=\"md-raised md-primary\" ng-click=\"vm.execute()\">Execute</md-button></div></div></md-card-content></md-card></div></md-content><md-content layout=\"column\" layout-fill=\"\" flex=\"\" ng-show=\"vm.stream.tasks.length\"><div><md-progress-linear md-mode=\"determinate\" value=\"{{ vm.stream.percent }}\"></md-progress-linear></div><span class=\"md-subhead\" ng-if=\"vm.running[0]\">{{ vm.running[0].name }} ({{ vm.running[0].current_phase }})</span><md-tabs md-selected=\"selectedIndex\" md-border-bottom=\"\" md-dynamic-height=\"\" flex=\"\"><md-tab ng-repeat=\"task in vm.stream.tasks\" flex=\"\"><md-tab-label><h3>{{ task.name }}</h3></md-tab-label><md-tab-body><div layout=\"row\" layout-align=\"space-around center\"><div ng-hide=\"task.status == \'complete\'\" class=\"text-center\"><div ng-if=\"task.status == \'pending\'\" class=\"md-display-2\">Pending</div><div ng-if=\"task.status == \'running\'\"><div class=\"md-display-2\">{{ task.phase | executePhaseFilter }}</div><div><small>({{ task.plugin }})</small></div></div></div><div ng-if=\"task.status == \'complete\'\"><md-list><md-subheader class=\"md-no-sticky text-center\"><span>Accepted {{ task.accepted }}</span> <span>Rejected {{ task.rejected }}</span> <span>Accepted {{ task.failed }}</span> <span>Undecided {{ task.undecided }}</span></md-subheader><md-list-item class=\"md-2-line\" ng-repeat=\"entry in task.entries\"><md-icon class=\"fa fa-check-circle\"></md-icon><h4>{{ entry.title }}</h4><p><small>{{ entry.accepted_by }}{{ entry.rejected_by }}{{ entry.failed_by }}</small></p><md-icon class=\"md-secondary\" ng-click=\"doSecondaryAction($event)\" aria-label=\"Chat\" md-svg-icon=\"communication:message\"></md-icon></md-list-item></md-list><div flex=\"\">{{ entry.title }}</div></div></div></md-tab-body></md-tab></md-tabs><div layout=\"row\" layout-align=\"space-around center\"><div></div><md-button class=\"md-raised md-primary\" ng-click=\"vm.clear()\">Clear</md-button><div></div></div></md-content>");
$templateCache.put("plugins/history/history.tmpl.html","<md-content flex=\"\" layout-margin=\"\"><div><section ng-repeat=\"(key, value) in vm.entries | groupBy: \'time | limitTo : 10\'\"><md-subheader class=\"md-primary\">{{ key }}</md-subheader><md-list layout-padding=\"\"><md-list-item class=\"md-2-line\" ng-repeat=\"entry in value\"><div class=\"md-list-item-text\"><h3>{{ entry.title }}</h3><p>{{ entry.task }}</p></div></md-list-item></md-list></section></div></md-content>");
$templateCache.put("plugins/log/log.tmpl.html","<md-content layout=\"column\" flex=\"\"><md-card class=\"log\" flex=\"\"><md-card-header><md-card-header-text><span class=\"md-title\">Server log</span> <span class=\"md-subhead\">{{ vm.status }}</span></md-card-header-text><md-icon class=\"fa fa-filter\"></md-icon><md-input-container class=\"md-block\" style=\"margin: 0px\" flex=\"60\" flex-gt-md=\"70\"><label>Filter</label> <input type=\"text\" aria-label=\"message\" ng-model=\"vm.filter.search\" ng-change=\"vm.refresh()\" ng-model-options=\"vm.refreshOpts\"><div class=\"hint\">Supports operators and, or, (), and \"str\"</div></md-input-container><md-menu><md-button class=\"widget-button md-icon-button\" ng-click=\"$mdOpenMenu()\" aria-label=\"open menu\"><md-icon md-font-icon=\"fa fa-ellipsis-v\"></md-icon></md-button><md-menu-content><md-menu-item layout-margin=\"\"><md-input-container><label>Max Lines</label> <input type=\"number\" aria-label=\"lines\" ng-model=\"vm.filter.lines\" ng-change=\"vm.refresh()\" ng-model-options=\"vm.refreshOpts\"></md-input-container></md-menu-item><md-menu-item><md-button ng-click=\"vm.toggle()\"><md-icon class=\"fa\" ng-class=\"vm.logStream ? \'fa fa-stop\' : \'fa fa-play\'\"></md-icon>{{ vm.logStream ? \'Stop\' : \'Start\' }}</md-button></md-menu-item></md-menu-content></md-menu></md-card-header><md-card-content layout=\"column\" flex=\"\" style=\"padding-top: 0px\"><div id=\"log-grid\" ui-grid=\"vm.gridOptions\" ui-grid-auto-resize=\"\" flex=\"\" ui-grid-auto-scroll=\"\"></div></md-card-content></md-card></md-content>");
$templateCache.put("plugins/schedule/schedule.tmpl.html","<div class=\"row\"><div ng-repeat=\"model in vm.models\"><div class=\"col-xs-3\"><form name=\"myForm\" sf-schema=\"schema\" sf-form=\"form\" sf-model=\"model\" ng-submit=\"onSubmit(myForm)\"></form></div></div></div>");
$templateCache.put("plugins/seen/seen.tmpl.html","<md-content layout=\"column\" flex=\"\"><seen-entry ng-repeat=\"entry in ::vm.entries\" entry=\"entry\"></seen-entry></md-content>");
$templateCache.put("plugins/series/series.episodes.tmpl.html","<md-content flex=\"\" layout-margin=\"\"><md-list><md-list-item class=\"md-3-line\" ng-repeat=\"episode in vm.episodes\"><md-card flex=\"\"><md-card-title><md-card-title-text>{{ episode.episode_identifier }}</md-card-title-text></md-card-title><md-card-content layout=\"row\" layout-align=\"space-between\"><md-list><md-list-item ng-repeat=\"release in episode.releases | orderBy : \'release_downloaded\' : true\"><md-list-item-text><h5><i ng-if=\"release.release_downloaded\" class=\"fa fa-download\"></i> {{ release.release_title }}</h5><h6 class=\"md-subheader\">{{ release.release_quality }}</h6></md-list-item-text></md-list-item></md-list></md-card-content><md-card-actions layout=\"row\" layout-align=\"end center\"><md-button class=\"md-warn md-raised\" ng-click=\"vm.forgetEpisode(episode)\">Forget Episode</md-button></md-card-actions></md-card></md-list-item></md-list></md-content>");
$templateCache.put("plugins/series/series.tmpl.html","<md-content flex=\"\" layout-margin=\"\"><md-tabs md-dynamic-height=\"\" md-border-bottom=\"\"><md-tab label=\"All series\"><div layout-gt-sm=\"row\"><md-input-container flex=\"\" layout-align=\"end center\"><label>Search</label> <input ng-model=\"vm.searchTerm\" ng-change=\"vm.search()\" ng-model-options=\"{ debounce: 1000 }\"></md-input-container></div><md-list><md-list-item class=\"md-3-line\" ng-repeat=\"show in vm.series\"><md-card flex=\"\"><md-card-title><md-card-title-text><span class=\"md-headline\">{{ show.show_name }}</span> <span class=\"md-subhead\">Latest: {{ show.latest_downloaded_episode.episode_identifier ? show.latest_downloaded_episode.episode_identifier : \'No yet\' }}</span></md-card-title-text></md-card-title><md-card-content layout=\"row\" class=\"custom-card\"><div class=\"md-media-lg series-image\"><img ng-src=\"{{ show.metadata.medium_image }}\"></div><p>{{ show.metadata.summary }}</p></md-card-content><md-card-actions layout=\"row\" layout-align=\"end center\"><md-button class=\"md-primary md-raised\" ng-click=\"vm.gotoEpisodes(show.show_id)\">Episodes</md-button><md-button class=\"md-warn md-raised\" ng-click=\"vm.forgetSeries(show)\">Forget</md-button></md-card-actions></md-card></md-list-item><fg-material-pagination page=\"vm.currentPage\" page-size=\"vm.pageSize\" total=\"vm.totalShows\" active-class=\"md-primary\" paging-action=\"vm.updateListPage(index)\"></fg-material-pagination></md-list></md-tab></md-tabs></md-content>");
$templateCache.put("services/modal/modal.dialog.circular.tmpl.html","<md-dialog><md-dialog-content><h2>{{ vm.title }}</h2><div layout=\"row\" layout-align=\"center center\"><p ng-if=\"content\">{{ vm.content }}</p><md-progress-circular ng-if=\"vm.showCircular\" md-diameter=\"30\" class=\"md-primary\" md-mode=\"indeterminate\"></md-progress-circular></div></md-dialog-content><md-dialog-actions ng-if=\"vm.ok || vm.cancel\"><md-button ng-if=\"vm.cancel\" ng-click=\"vm.abort()\" class=\"md-primary\">{{ vm.cancel }}</md-button><md-button ng-if=\"vm.ok\" ng-click=\"vm.hide()\" class=\"md-primary\">{{ vm.ok }}</md-button></md-dialog-actions></md-dialog>");
$templateCache.put("services/modal/modal.tmpl.html","<div class=\"modal-header\"><h3>{{ modalOptions.headerText }}</h3></div><div class=\"modal-body\"><p>{{ modalOptions.bodyText }}</p></div><div class=\"modal-footer\"><button ng-if=\"modalOptions.okText\" type=\"button\" class=\"btn btn-{{ modalOptions.okType }}\" data-ng-click=\"ok()\">{{ modalOptions.okText }}</button> <button ng-if=\"modalOptions.closeText\" type=\"button\" class=\"btn btn-{{ modalOptions.closeType }}\" data-ng-click=\"close()\">{{ modalOptions.closeText }}</button></div>");
$templateCache.put("components/seen/seen-entry/seen-entry.tmpl.html","<md-card><md-card-header><md-card-header-text><span class=\"md-title\">{{vm.entry.title}}</span> <span class=\"md-subhead\" ng-if=\"vm.entry.local\">Local to <b>{{vm.entry.task}}</b></span> <span class=\"md-subhead\" ng-if=\"!vm.entry.local\">Global</span></md-card-header-text></md-card-header><md-card-content><md-list><md-list-item ng-repeat=\"field in ::vm.entry.fields\"><div class=\"md-list-item-text\" layout=\"row\"><p><b>{{field.field_name}}:</b> {{field.value}}</p></div></md-list-item></md-list></md-card-content><md-card-actions></md-card-actions></md-card>");
$templateCache.put("components/seen/seen-field/seen-field.tmpl.html","");}]);