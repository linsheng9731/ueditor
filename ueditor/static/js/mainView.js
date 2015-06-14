///**
// * 专利显示页的js代码
// * Created by abnerzheng on 15/4/21.
// */
//
angular.module('ui.bootstrap.demo', ['ui.bootstrap', 'ng.httpLoader']); //依赖注入，前端用了angular+bootstrap UI
angular.module('ui.bootstrap.demo').config(['httpMethodInterceptorProvider',
        function (httpMethodInterceptorProvider) {
            httpMethodInterceptorProvider.whitelistDomain('get_record_detail');
            httpMethodInterceptorProvider.whitelistDomain('get_infoAndArticle');
        }]
).controller('AccordionDemoCtrl', function ($scope, $http) {
        $scope.userName = "";
        $http.get('/getArticles').success(function(msg){
            console.log(msg)
            $scope.userName = msg.name
            $scope.articles = msg.articles;
            $scope.totalItems = msg.articles.length;
        });
        function get_infoAndArticle(){

        }

        $scope.modify = function(id){
            window.location.href = '/editor?article_id=' + id;
        }

    })

//angular.module('ui.bootstrap.demo').controller('AccordionDemoCtrl', function ($scope, $log) {
//  $scope.totalItems = 64;
//  $scope.currentPage = 4;
//
//  $scope.setPage = function (pageNo) {
//    $scope.currentPage = pageNo;
//  };
//
//  $scope.pageChanged = function() {
//    $log.log('Page changed to: ' + $scope.currentPage);
//  };
//
//  $scope.maxSize = 5;
//  $scope.bigTotalItems = 175;
//  $scope.bigCurrentPage = 1;
//});
