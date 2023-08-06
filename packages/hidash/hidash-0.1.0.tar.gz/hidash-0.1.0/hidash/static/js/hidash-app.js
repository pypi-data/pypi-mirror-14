angular.module('dashboard', ['googlechart','ngMaterial','hidash'])
.controller('ReportsController',function($scope, $http, $window, $location){
	$scope.charts=[];
	$scope.absUrl = $location.absUrl().split("?")[1];
	if (!$scope.absUrl) {
			$scope.absUrl="group=default";
		}
    $http.get("/api/group_reports/?" + $scope.absUrl).success(function(data){
    	for (var i=0;i<data.length;i++){
    		$scope.charts[i]={};
    		$scope.charts[i].data=data[i].data;
    		$scope.charts[i].type=data[i].data.chart_type;
    		$scope.charts[i].chart_id=data[i].chart_id;
    		$scope.charts[i].query_id=data[i].query_id;
    		var options = {
    				  width: '100%',
    				  height: 300,
    				  is3D: true,
    				  margin: 2
    				};
    		$scope.charts[i].options = options;
    	}
    });
});
