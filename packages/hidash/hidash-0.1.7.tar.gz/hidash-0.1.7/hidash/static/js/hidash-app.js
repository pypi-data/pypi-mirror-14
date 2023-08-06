angular.module('dashboard', ['googlechart','ngMaterial','hidash'])
.controller('ReportsController',function($scope, $http, $window, $location){
	$scope.charts=[];
	$scope.absUrl = $location.absUrl().split("?")[1];
	if (!$scope.absUrl) {
			$scope.absUrl="group=default";
		}
 
});
