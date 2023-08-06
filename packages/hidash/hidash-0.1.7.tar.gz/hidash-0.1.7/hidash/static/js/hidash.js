"use strict";
angular.module('hidash', ['googlechart'])
    .directive('hiDash', ['$http', 'resolveTemplate', 'urlProcessor',
        function($http, resolveTemplate, urlProcessor) {
            return {
                scope: {
                    host: '@host',
                    chart_name: '@chart',
                    query: '@query',
                    params: '@params',
                    chart_type: '@type',
                    update: '@update',
                    options: '=options',
                    typeSelect: '=typeSelect',
                    container: '@container'
                },

                controller: function($scope, $element) {

                    $scope.chartUrl = urlProcessor.generateUrl($scope.chart_name,
                        $scope.query, $scope.host);

                    if ($scope.params) {
                        $scope.chartUrl = urlProcessor.addParams($scope.params, $scope.chartUrl);
                    }

                    var updateChartData = function() {
                        $http.get($scope.chartUrl).success(function(data) {
                            $scope.chart.data = data;
                        });
                    };
                    var createChart = function() {
                        $http.get($scope.chartUrl).success(function(data) {
                            if ($scope.chart_type == 'MapChart') {
                                createMap(data);
                                return;
                            }
                            $scope.chart = {};
                            $scope.chart.data = data;
                            if ($scope.chart_type) {
                                $scope.chart.type = $scope.chart_type;
                            } else if (data.chart_type) {
                                $scope.chart.type = data.chart_type;
                            } else {
                                $scope.chart.type = "ColumnChart";
                            }
                            $scope.chart.options = $scope.options || {};
                            $scope.chartTypes = ["LineChart", "BarChart",
                                "ColumnChart", "AreaChart",
                                "PieChart", "ScatterChart",
                                "SteppedAreaChart", "ComboChart"
                            ];
                        }).error(function(data) {
                            if ($scope.container) {
                                if (document.getElementById($scope.container)) {
                                    document.getElementById($scope.container).remove();
                                }
                            }
                        });
                    };

                    var createMap = function(data) {
                        google.load("visualization", "1", {
                            "packages": ["map"],
                            "callback": drawMap
                        });

                        function drawMap() {
                            var options = $scope.options || {};
                            options.showTip = true;
                            var map = new google.visualization.Map($element[0].firstChild);
                            map.draw(new google.visualization.DataTable(data), options);
                        }

                    };
                    if ($scope.update) {
                        setInterval(updateChartData, $scope.update);
                    }

                    $scope.$watchGroup(['params', 'chart_name', 'query', 'host',
                            'options', 'chart_type', 'typeSelect'
                        ],
                        function(newValue, oldValue) {
                            $scope.chartUrl = urlProcessor.generateUrl(newValue[1],
                                newValue[2], newValue[3]);
                            if (newValue[0]) {
                                $scope.chartUrl = urlProcessor.addParams(newValue[0],
                                    $scope.chartUrl);
                            }
                            createChart();
                        });
                    
                    
                },
                template: resolveTemplate

            };
        }
    ])
    .directive('highDash', ['$http', function($http) {
        return {
            scope: {
                host: '@host',
                chart_name: '@chart',
                query: '@query',
                params: '@params',
                chart_type: '@type',
                update: '@update',
            },

            controller: function($scope, $element) {
                // create a factory for generating url
                $scope.chartUrl = "/api/charts/" + $scope.chart_name +
                    ".json/?query=" + $scope.query;
                if (typeof CONFIG !== 'undefined') {
                    $scope.chartUrl = CONFIG.hidashApiBase + "/charts/" +
                        $scope.chart_name + ".json/?query=" +
                        $scope.query;
                } else if ($scope.host !== undefined) {
                    $scope.chartUrl = $scope.host + "/api/charts/" +
                        $scope.chart_name + ".json/?query=" +
                        $scope.query;
                }
                if ($scope.params) {
                    $scope.params = $scope.params.replace(/\s*(,|^|$)\s*/g, "$1");
                    $scope.params = $scope.params.split(',');
                    for (var index = 0; index < $scope.params.length; index++) {
                        $scope.chartUrl = $scope.chartUrl + "&" +
                            $scope.params[index];
                    }
                }
                $http.get($scope.chartUrl).success(function(data) {
                    var chartData = {};
                    chartData.chart = {
                        renderTo: $element[0].id,
                        type: 'column'
                    };
                    chartData.xAxis = {
                        type: 'category'
                    };
                    chartData.series = data;
                    chartData.credits = {
                        enabled: false
                    };
                    if ($scope.chart_type) {
                        chartData.chart.type = $scope.chart_type;
                    }
                    var newChart = new Highcharts.Chart(chartData);
                    var createChart = function() {
                        $http.get($scope.chartUrl).success(function(data) {
                            var current_data_length = newChart.series.length;
                            var new_data_length = data.length;

                            if (current_data_length >= new_data_length) {

                                for (var i = 0; i < new_data_length; i++) {
                                    newChart.series[i].update({
                                        name: data[i].name
                                    });
                                    newChart.series[i].setData(data[i].data);
                                }
                                while (i < current_data_length) {
                                    newChart.series[i].remove();
                                    i++;
                                }
                            } else {
                                for (var i = 0; i < current_data_length; i++) {
                                    newChart.series[i].update({
                                        name: data[i].name
                                    });
                                    newChart.series[i].setData(data[i].data);
                                }

                                while (i < new_data_length) {
                                    newChart.addSeries(data[i]);
                                    i++;
                                }
                            }
                        });
                    };
                    if ($scope.update) {
                        setInterval(createChart, $scope.update);
                    }
                });
            }
        };
    }])
    .directive('hiDashReports', ['$http', function($http) {
        return {
            scope: {
                host: '@host',
                group: '@group'
            },
            controller: function($scope) {
                $scope.startDate = new Date();
                $scope.startDate.setDate(1);
                $scope.endDate = new Date();
                $scope.endDate.setMonth($scope.endDate.getMonth() + 1);
                $scope.endDate.setDate(1);
                $scope.chartUrl = "/api/show_reports.json/"; // put it in
                // constants
                if (CONFIG.hidashApiBase !== undefined) {
                    $scope.chartUrl = CONFIG.hidashApiBase + "/show_reports.json/";
                } else if ($scope.host !== undefined) {
                    $scope.chartUrl = $scope.host + "/show_reports.json/";
                }
                if ($scope.group !== undefined) {
                    $scope.chartUrl = $scope.chartUrl + "?group=" + $scope.group;
                }
                $http.get($scope.chartUrl).success(function(data) {
                    $scope.data = data;
                });
            },
            template: `
					<div flex="100" layout="row" layout-align="center" layout-margin>
					<md-datepicker flex="15" ng-model="startDate" md-placeholder="Enter Start date"></md-datepicker>
					<md-datepicker flex="15" ng-model="endDate" md-placeholder="Enter End date"></md-datepicker>
					</div>
					<section layout="row"  layout-sm="column" layout-xs="column" layout-align="center" layout-wrap layout-margin class="report-area">
					<md-whiteframe ng-repeat="chart in data" class="card md-whiteframe-4dp" flex="45" flex-sm="100" flex-xs="100" layout="column" layout-wrap>
					<md-toolbar class="toolbar" layout="column" layout-padding>
						<span flex >{{chart.chart_id}}</span>
					</md-toolbar>
					<hi-dash update="5000" chart = "{{chart.chart_id}}" query = "{{chart.query_id}}" params="start_date={{startDate|date:'yyyy-MM-dd'}}, end_date={{endDate |date:'yyyy-MM-dd'}}" options="{width: '100%', height: 300, is3D: true, margin: 2}"></hi-dash>
						</md-whiteframe>
					</section> `
        };
    }])
    .service('resolveTemplate', function() {
        return function(tElement, tAttrs) {

            if (tAttrs.type == "MapChart") {
                return '<div style="height:100%; width: 100%;"></div>';
            }
            if (tAttrs.typeselect == 'am') {
                return '<md-input-container class="chart-select"><md-select ng-model="chart.type"><md-option ng-repeat="type in chartTypes" value="{{type}}">{{type}}</md-option></md-select></md-input-container><div google-chart chart="chart" style="height:100%; width: 100%;"></div>';
            } else if (tAttrs.typeselect == 'bs') {
                return '<div class="col-xs-3"><select ng-model="chart.type" class="wrapper form-control chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>';
            } else if (tAttrs.typeselect == 'true') {

                return '<div ><select ng-model="chart.type" class="chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>';
            } else {
                return '<div google-chart chart="chart" "></div>';
            }
        };
    })
    .service('urlProcessor', function() {
        var _addParams = function(params, url) {
            var processed_params = params.replace(/\s*(,|^|$)\s*/g, "$1").split(',');
            for (var index = 0; index < processed_params.length; index++) {
                url += "&" + processed_params[index];
            }
            return url;
        };
        var _generateUrl = function(name, query, host) {
            var url = "/api/charts/" + name + ".json/?query=" + query;
            if (typeof CONFIG !== 'undefined') {
                url = CONFIG.hidashApiBase + "/charts/" + name + ".json/?query=" +
                    query;
            } else if (host !== undefined) {
                url = host + "/api/charts/" + name + ".json/?query=" + query;
            }
            return url;
        };

        return {
            addParams: _addParams,
            generateUrl: _generateUrl
        };

    });