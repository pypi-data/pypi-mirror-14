function resolveTemplate(tElement, tAttrs){
	
	if (tAttrs.type == "MapChart"){
		    	return '<div style="height:100%; width: 100%;"></div>';
    }
	if (tAttrs.typeselect == 'am'){
        return '<md-input-container class="chart-select"><md-select ng-model="chart.type"><md-option ng-repeat="type in chartTypes" value="{{type}}">{{type}}</md-option></md-select></md-input-container><div google-chart chart="chart" style="height:100%; width: 100%;"></div>';
    }
    else if(tAttrs.typeselect == 'bs'){        
        return '<div class="col-xs-3"><select ng-model="chart.type" class="wrapper form-control chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>';
    }
    else if(tAttrs.typeselect == 'true' ){
 	   
        return '<div ><select ng-model="chart.type" class="chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>'
    }
    else {
        return '<div google-chart chart="chart" "></div>';
    }
}
angular.module('hidash', ['googlechart'])
.directive('hiDash', ['$http', function($http) { 
	return {
        scope : { 
        	chart: '@chart',
            query: '@query',
            params: '@params',
            chart_type : '@type',
            update: '@update',
            options : '=options',
            typeSelect : '=typeSelect' 


 
        },
            
controller : function($scope, $element){
	$scope.chartUrl = "/api/charts/" + $scope.chart + ".json/?query=" + $scope.query; 
	if($scope.params) {
		$scope.params = $scope.params.replace(/\s*(,|^|$)\s*/g, "$1");
		$scope.params = $scope.params.split(',');
		for(var index=0; index < $scope.params.length; index++) {
			$scope.chartUrl = $scope.chartUrl + "&" + $scope.params[index];
		}
	}
	var updateChartData = function(){
	    $http.get($scope.chartUrl).success(function(data){
	    	       $scope.chart.data = data;
	    });
   }
    
    var createChart = function() {
        $http.get($scope.chartUrl).success(function(data){
        	console.log(data);
        	   if ($scope.chart_type == 'MapChart'){        	
	        	   createMap(data);
	        	   return;
        	   }
	          
        	   $scope.chart={};
        	   $scope.chart.data = data;
        	  
	       
       if ($scope.chart_type) {
            $scope.chart.type = $scope.chart_type;
        }
        else if (data.chart_type) {
            $scope.chart.type = data.chart_type;
        }
        else {
            $scope.chart.type = "ColumnChart";
        }

        $scope.chart.options=$scope.options || {};
	   //$scope.chart.options.animation = {duration: 500, easing: 'in'}	
	   //$scope.chart.options.legend = 'none'	
        $scope.chartTypes = ["LineChart", "BarChart", "ColumnChart", "AreaChart", "PieChart", "ScatterChart", "SteppedAreaChart", "ComboChart"]
    });
    };
    
    
    
    var createMap = function(data){
    	google.load("visualization", "1", { "packages": [ "map"], "callback" : drawMap }); 
        function drawMap() {
        	var options = $scope.options || {};
        	options['showTip'] = true;
        	console.log($element[0].firstChild);
        	var map = new google.visualization.Map($element[0].firstChild);
        	map.draw(new google.visualization.DataTable(data), options);
        	};
    	
    };
    
    createChart();
    if($scope.update) {
 	               setInterval(updateChartData, $scope.update);
    }
    
	    }, 
        
template: resolveTemplate 
      };
    }])

.directive('highDash', ['$http', function($http) {
	return {
		scope : {
			chart: '@chart',
            query: '@query',
            params: '@params',
            chart_type : '@type',
            update: '@update',
		},
		
		controller : function($scope, $element) {
			$scope.chartUrl = "/api/charts/" + $scope.chart + ".json/?query=" + $scope.query; 
        	if($scope.params) {
        		$scope.params = $scope.params.replace(/\s*(,|^|$)\s*/g, "$1");
        		$scope.params = $scope.params.split(',');
        		for(var index=0; index < $scope.params.length; index++) {
        			$scope.chartUrl = $scope.chartUrl + "&" + $scope.params[index];
        		}
        	}
        	$http.get($scope.chartUrl).success(function(data){
    			var chartData = new Object();
    			chartData.chart = {
    					renderTo : $element[0].id,
    					type: 'column'
    			}
    			chartData.xAxis =  {
    					type: 'category'
    			} 
    			chartData.series = data;
    			if($scope.chart_type) {
    				chartData.chart.type = $scope.chart_type;
    			}
    			var newChart = new Highcharts.Chart(chartData);
    			var createChart = function() {
    				$http.get($scope.chartUrl).success(function(data){
       					newChart.series[0].setData(data[0].data);
       				});
    			}
    			if($scope.update) {
    				setInterval(createChart, $scope.update);
    			}
    		});	
		}
	}
}]);