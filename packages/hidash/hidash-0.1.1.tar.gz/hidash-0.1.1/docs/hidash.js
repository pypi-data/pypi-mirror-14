angular.module('hidash', ['googlechart'])
.controller('ChartController', ['$scope', function($scope) {
	  	 
	
	}])
	.directive('hiDash', ['$http', function($http) {
		return {
		scope : {
			ChartUrl : '=url',
			chart_type : '=type',
			options : '=options'			
			
		},
		
	
		
controller : function($scope){	
	
		$http.get($scope.ChartUrl).success(function(data){

		$scope.chart={};
		$scope.chart.data = data[0];
		
		if ($scope.chart_type != undefined)
			{
			$scope.chart.type = $scope.chart_type;
			}
		else{
			$scope.chart.type = data[0].chart_type;
		}
		$scope.chart.options=$scope.options;
		
		
	});
	
}, 
	  
	    template: '<div google-chart chart="chart" style="height:100%; width: 100%"></div>'
	  
	  
	  
	  
	  };
	}]);